# Admin Metadata CRUD — Design Spec

**Date:** 2026-04-09
**Package:** `pymetadataeditor`
**Target version:** `0.4.0`
**Status:** Draft — pending review

---

## 1. Context & motivation

`pymetadataeditor` is a Python client library for the [Metadata Editor](https://github.com/mah0001/metadata-editor) REST API. It is intended to be a **general-purpose** client — clean of any organisation- or workflow-specific logic — usable by any institution running a Metadata Editor instance.

A gap analysis of [`docs/publishing.py`](../../publishing.py) (a Data360 publishing workflow script) against the current `pymetadataeditor` public surface identified **administrative metadata** as the most urgent missing capability. Admin metadata is an entirely separate concern from project metadata: it has its own template namespace, its own CRUD endpoints, and is keyed by `(project_id, template_uid)` pairs rather than by numeric project ID alone.

Today the only way to work with admin metadata through `pymetadataeditor` is `generic_api_request()` — i.e. callers must hand-craft URLs and bodies, completely bypassing the class's validation, error handling, and type conventions. A commented-out stub of `log_project_admin_metadata` already exists in [`pymetadataeditor/interface.py:1084-1113`](../../../pymetadataeditor/interface.py#L1084-L1113), indicating that earlier work began in this direction but was abandoned.

This spec defines a minimal, dict-only CRUD surface for admin metadata that:

- Uses the same HTTP layer, error types, and conventions as the rest of `MetadataEditor`
- Stays **general-purpose** — no Data360/World Bank/SDMX concerns leak in
- Ships as round 1 of a broader package of gaps identified in [`docs/publishing.py`](../../publishing.py)
- Defers Pydantic/Excel support, admin-template Pydantic class generation, and edit history to a round 2

Out of scope (deferred from the initial gap analysis):

- PDF export, by-idno lookups, attribute-filtered listing, bulk parallel export, `exclude_private_fields` flag, `list_projects_in_collection` type filter — all Bucket 2 items for later rounds.
- All Bucket 3 items (SDMX parsing, Data360 payload shaping, DDH triggers). These belong in a future sibling package; see §7.

---

## 2. Scope

### 2.1 In scope

Seven new public methods on `pymetadataeditor.interface.MetadataEditor`:

1. `list_admin_metadata_templates()`
2. `get_admin_metadata_template_by_uid(uid)`
3. `list_admin_metadata(...)` — query with filters and pagination
4. `get_admin_metadata(project_id, template_uid)`
5. `upsert_admin_metadata(project_id, template_uid, metadata)`
6. `patch_admin_metadata(project_id, template_uid, patches)` — multi-op JSON Patch
7. `delete_admin_metadata(project_id, template_uid)`

All seven return/accept `dict`, `pd.DataFrame`, or `pd.Series`. No `output_mode` parameter, no Pydantic, no Excel.

### 2.2 Out of scope for this round

- `output_mode="pydantic" | "excel"` on any admin-metadata method.
- `get_admin_metadata_class(uid)` / `make_admin_metadata_outline(uid, ...)`. No Pydantic class generation from admin templates. No admin template caching on `self._templates`.
- `get_admin_metadata_edit_history()` (the endpoint `/admin-metadata/edit_history/{projectId}/{templateUid}` exists but is not exposed in this round).
- No changes to `list_templates()` — admin templates remain in their own discovery namespace.
- No changes to `patch_update_project_log_by_id()`. The project-side patch remains single-op. A future round may generalise it to multi-op to match `patch_admin_metadata` — explicitly noted as a follow-up.
- No convenience helpers for response shaping (e.g. the `clean_admin_metadata()` helper in `publishing.py` that flattens the list response into `{template_uid: metadata}` — that belongs in a downstream Data360 package, not in a general-purpose client).

### 2.3 Non-goals

- This spec does **not** introduce a Data360/SDMX/World Bank sibling package. A sibling package for those workflow-specific helpers has been agreed strategically (see §7) but its design is a separate spec.

---

## 3. Admin metadata API surface (ground truth)

Sourced from [`docs/metadata-editor-api.yaml`](../../metadata-editor-api.yaml) (the Metadata Editor OpenAPI spec).

| Endpoint | Verb | Purpose | Body / params |
|---|---|---|---|
| `/admin-metadata/templates` | GET | List admin templates | — |
| `/admin-metadata/templates/{templateUid}` | GET | Get one admin template | — |
| `/admin-metadata/data_query` | GET | Query records | `project_id?`, `template?` (comma-separated), `date_from?` (YYYY-MM-DD), `date_to?`, `limit?` (default 50), `offset?` (default 0) |
| `/admin-metadata/data/{projectId}/{templateUid}` | GET | Read one record | `projectId` accepts **ID or IDNO** |
| `/admin-metadata/data/` | POST | **Upsert** (add/update) | `{project_id, template_uid, metadata}` |
| `/admin-metadata/data_patch/` | POST | **Multi-op** JSON Patch | `{project_id, template_uid, patches[]}` |
| `/admin-metadata/data_remove/` | POST | Delete | `{project_id, template_uid}` |
| `/admin-metadata/edit_history/{projectId}/{templateUid}` | GET | Edit history | *(out of scope)* |

Three properties shape the design:

1. **Admin metadata is keyed by `(project_id, template_uid)` pairs.** A single project can have multiple admin-metadata records — one per template. Every method except `list_admin_metadata` and the two template-discovery methods takes both keys.
2. **Admin templates live in their own namespace.** `/admin-metadata/templates` is disjoint from `/templates`. `list_templates()` today does not surface admin templates, and this spec does not change that.
3. **`POST /admin-metadata/data/` is upsert, not insert.** There is no separate create vs update endpoint. Method naming reflects this: `upsert_admin_metadata`, not `create_admin_metadata` / `update_admin_metadata`.

The patch endpoint natively supports a `patches[]` array of JSON Patch operations (RFC 6902) in a single request — unlike the project-side `/editor/patch/...` endpoint as it is currently exposed. `patch_admin_metadata` takes advantage of this.

---

## 4. Design

### 4.1 Method signatures

```python
# ─── Admin metadata templates (discovery) ───────────────────────────────────

def list_admin_metadata_templates(self) -> pd.DataFrame:
    """Retrieves all administrative metadata templates.

    Returns:
        pd.DataFrame: DataFrame of admin metadata templates. Empty DataFrame
            (with the expected columns) if none are found.
    """

def get_admin_metadata_template_by_uid(self, uid: str) -> pd.Series:
    """Retrieves a single administrative metadata template by UID.

    Args:
        uid (str): Admin metadata template UID.

    Returns:
        pd.Series: The template record.

    Raises:
        TemplateError: If the UID is not found.
    """

# ─── Admin metadata data (CRUD) ─────────────────────────────────────────────

def list_admin_metadata(
    self,
    project_id: Optional[Union[int, str]] = None,
    template_uid: Optional[Union[str, List[str]]] = None,
    date_from: Optional[str] = None,   # "YYYY-MM-DD"
    date_to: Optional[str] = None,     # "YYYY-MM-DD"
    limit: Union[int, str] = "All",
    offset: int = 0,
) -> pd.DataFrame:
    """Query administrative metadata records across projects and templates.

    Paginates internally in batches of 500 when `limit="All"` (same convention
    as `list_projects`).

    Args:
        project_id: Filter by a single project ID or IDNO.
        template_uid: Filter by one template UID, or a list of UIDs
            (list values are joined with commas before being sent to the API).
        date_from: Inclusive lower bound on the `changed` field (YYYY-MM-DD).
        date_to: Inclusive upper bound on the `changed` field (YYYY-MM-DD).
        limit: Max records to return, or "All" to fetch every page.
        offset: Starting offset. Ignored when `limit="All"`.

    Returns:
        pd.DataFrame: One row per (project, template_uid) record. Empty
            DataFrame if none match.
    """

def get_admin_metadata(
    self,
    project_id: Union[int, str],
    template_uid: str,
) -> Dict:
    """Retrieves a single administrative metadata record.

    Args:
        project_id: Project ID (int) or IDNO (str). Passed through verbatim
            — the endpoint accepts either.
        template_uid: Admin metadata template UID.

    Returns:
        Dict: The admin metadata record as returned by the API.

    Raises:
        ValueError: If the record does not exist for this (project, template) pair.
    """

def upsert_admin_metadata(
    self,
    project_id: Union[int, str],
    template_uid: str,
    metadata: Dict,
) -> Dict:
    """Creates or updates (upserts) an administrative metadata record.

    The Metadata Editor API uses a single upsert endpoint — there is no
    separate create vs update. If a record already exists for the
    (project_id, template_uid) pair, it is overwritten; otherwise a new one
    is created.

    Empty values in `metadata` are stripped before the request is sent via
    `remove_empty_from_dict`, matching the convention used by
    `create_project_log` and `update_project_log_by_id`.

    Args:
        project_id: Project ID or IDNO.
        template_uid: Admin metadata template UID.
        metadata: Admin metadata payload as a dict.

    Returns:
        Dict: The server response.

    Raises:
        ValueError: If `metadata` is not a dict, or if `template_uid` is empty.
    """

def patch_admin_metadata(
    self,
    project_id: Union[int, str],
    template_uid: str,
    patches: List[Dict],
) -> Dict:
    """Applies JSON Patch (RFC 6902) operations to an admin metadata record.

    Unlike `patch_update_project_log_by_id`, this method accepts a list of
    patch operations and applies them atomically — the underlying admin
    metadata patch endpoint natively supports multi-op patches.

    Each patch operation is a dict with `op`, `path`, and optionally `value`
    and `from` keys. Paths that do not start with `/` are auto-corrected
    (matching `patch_update_project_log_by_id`).

    Args:
        project_id: Project ID or IDNO.
        template_uid: Admin metadata template UID.
        patches: List of JSON Patch operations, e.g.
            `[{"op": "replace", "path": "/foo", "value": "bar"}, ...]`.

    Returns:
        Dict: The server response.

    Raises:
        ValueError: If `patches` is empty, or any op is not a valid RFC 6902
            verb (`add`, `remove`, `replace`, `move`, `copy`, `test`), or
            required fields are missing for the given op. Validation is
            delegated to the existing `validate_json_patches()` helper.
    """

def delete_admin_metadata(
    self,
    project_id: Union[int, str],
    template_uid: str,
):
    """Deletes an administrative metadata record.

    Args:
        project_id: Project ID or IDNO.
        template_uid: Admin metadata template UID.

    Raises:
        DeleteNotAppliedError: If the API does not confirm the delete
            (i.e. a subsequent `get_admin_metadata` call still succeeds).
    """
```

### 4.2 Typing notes

- `project_id: Union[int, str]` in every signature where it appears. The API's `{projectId}` path slot and `project_id` JSON body field both accept numeric IDs and string IDNOs; `pymetadataeditor` passes the value through verbatim without attempting client-side resolution. This intentionally sidesteps the broader "by-idno helpers" question that was left out of scope in §2.2.
- `template_uid: str` — always a string, always required (except in the filter position on `list_admin_metadata`).
- `patches: List[Dict]` — raw JSON Patch op dicts. We deliberately do **not** introduce a wrapper type. This matches the style of the rest of the package, keeps the signature close to the API, and allows a future round to generalise `patch_update_project_log_by_id` to multi-op with the same shape.

### 4.3 Endpoint path mapping

The existing `RequestsWithSpecificErrors` helper in `pymetadataeditor/requester.py` takes a path template with a single `{}` placeholder for interpolation via the `id=` keyword argument. For paths with multiple dynamic segments, f-string interpolation is used directly.

| Method | `pth` argument to `_apinterface` | HTTP verb | Body |
|---|---|---|---|
| `list_admin_metadata_templates` | `admin-metadata/templates` | GET | — |
| `get_admin_metadata_template_by_uid` | `admin-metadata/templates/{}` (via `id=uid`) | GET | — |
| `list_admin_metadata` | `admin-metadata/data_query` | GET | — (query params passed as `params=`) |
| `get_admin_metadata` | `f"admin-metadata/data/{project_id}/"` + `{}` (via `id=template_uid`) | GET | — |
| `upsert_admin_metadata` | `admin-metadata/data/` | POST | `{project_id, template_uid, metadata}` |
| `patch_admin_metadata` | `admin-metadata/data_patch/` | POST | `{project_id, template_uid, patches}` |
| `delete_admin_metadata` | `admin-metadata/data_remove/` | POST | `{project_id, template_uid}` |

**Open verification item during implementation:** confirm that `RequestsWithSpecificErrors` accepts f-string-interpolated path prefixes alongside the `id=` slot. If not, the implementer must either (a) extend `RequestsWithSpecificErrors` to support multi-segment interpolation, or (b) build the full path as a string in `interface.py` and pass it without the `id=` kwarg. Option (b) is preferred to avoid widening an internal API in this round. The plan-writing phase will select the exact approach after reading `requester.py`.

### 4.4 Validation, empty-value cleaning, and error handling

| Concern | Approach |
|---|---|
| Stripping empty/None values from the POST body | `upsert_admin_metadata` calls `remove_empty_from_dict(metadata)` from `pymetadataeditor/utils.py` before sending, matching `create_project_log`. |
| JSON Patch op validation | `patch_admin_metadata` passes `patches` through `validate_json_patches()` from `pymetadataeditor/utils.py` — the same helper `patch_update_project_log_by_id` uses. Path auto-`/` prefix normalisation happens inside that helper. |
| `template_uid` not empty | `upsert_admin_metadata` raises `ValueError("template_uid must be a non-empty string")` before sending. |
| `metadata` must be a dict | `upsert_admin_metadata` raises `ValueError` if `not isinstance(metadata, dict)`. Pydantic models / Excel paths are **not** accepted in this round (deferred). |
| Delete confirmation | `delete_admin_metadata` follows the pattern of `delete_resource_by_id`: after the POST it calls `get_admin_metadata(project_id, template_uid)` and expects an error. If the record still exists it raises `DeleteNotAppliedError`. It does **not** reuse `_delete_by_id` because the delete endpoint shape is `POST /data_remove/` with a body, not `.../delete/{id}`. |
| HTTP errors (4xx/5xx) | Propagated from `self._apinterface` unchanged. The existing error-translation layer in `requester.py` handles 403 → `PermissionError`, 404 → `HTTPError`/`ValueError`, SSL errors, etc. |
| "Not found" on `get_admin_metadata` | Catches the underlying 404 and re-raises as `ValueError(f"No admin metadata found for project_id={project_id}, template_uid={template_uid}")`. Matches the UX of `get_project_by_id`-style lookups. |
| "Not found" on `get_admin_metadata_template_by_uid` | Re-raised as `TemplateError`, matching the existing `get_template_by_uid` convention. |

### 4.5 Pagination semantics for `list_admin_metadata`

- `limit="All"` (default): fetch in batches of 500, stopping when the returned page has fewer rows than the batch size, or when the API's reported `total` is exhausted. This mirrors `list_projects`.
- `limit=<int>`: single page, honours `offset`. Returns at most `limit` rows.
- Empty result → empty `DataFrame` (not `None`).
- `template_uid=["a", "b"]` → the query parameter sent is `template=a,b`. Single-string values are passed through as-is.
- No client-side date validation — `date_from` / `date_to` are passed through as strings. The server rejects malformed dates with a 400 which propagates.

---

## 5. Changes by file

### 5.1 `pymetadataeditor/interface.py`

- Add a new section-marker comment block (`# ADMIN METADATA`) after the existing `# TEMPLATES` block.
- Add the 7 new public methods with full Google-style docstrings.
- Remove the commented-out stub of `log_project_admin_metadata` at lines 1084-1113 — it is superseded by this design.
- No changes to existing public methods.

### 5.2 `pymetadataeditor/utils.py`

- No changes. `validate_json_patches()` and `remove_empty_from_dict()` are reused as-is.

### 5.3 `pymetadataeditor/requester.py`

- No changes **expected**. If the verification item in §4.3 reveals that multi-segment path interpolation is impossible through the current helper, the implementer builds the path in `interface.py` without widening `requester.py` (option (b) above).

### 5.4 `pymetadataeditor/templates.py`, `pymetadataeditor/llm_helpers.py`, `pymetadataeditor/__init__.py`

- No changes. No new exports — the 7 methods are accessed via `MetadataEditor`, which is already exported.

### 5.5 `tests/test_interface.py`

- Add a new `# ADMIN METADATA` section.
- Add ~20 test functions covering the methods. Detailed list in §6.1.
- Reuses the existing `MockResponse`, `metadata_editor` fixture, and `itertools.chain`-based mocking for multi-call scenarios (delete + post-delete checker).

### 5.6 `tests/integration_test.py`

- Add one `test_admin_metadata_lifecycle` end-to-end test, guarded by the existing `API_KEY` / `API_URL` env vars. Detailed in §6.2.

### 5.7 Documentation

| File | Change |
|---|---|
| [`docs/skill.md`](../../skill.md) | Add an **"Admin Metadata"** capability group under "Key Capabilities" listing the 7 methods. Add one new short entry in "Common Workflows" (upsert → get → patch → delete). |
| [`docs/modules/interface.md`](../../modules/interface.md) | Add an **"Admin Metadata"** method-reference section with the same depth as existing sections (signature + args table + example). |
| [`docs/API_Reference.md`](../../API_Reference.md) | Regenerated via `python make_docs.py` — not hand-edited. |
| [`CLAUDE.md`](../../../CLAUDE.md) | Add a short note under "Architecture & Key Conventions": *"Admin metadata is a separate namespace with its own template registry (`/admin-metadata/templates`) and its own CRUD endpoints. It is not hooked into `list_templates()` or `self._templates`. Multi-op JSON Patch is supported on admin metadata but not (yet) on project metadata."* |
| `CHANGELOG.md` | If a changelog file exists, add a `## [0.4.0]` entry. Do **not** create one if it does not exist — out of scope. |

### 5.8 `pyproject.toml`

- Version bump: `0.3.2` → `0.4.0`. This is a minor bump because the change is purely additive (no breaking changes to existing methods, no signature changes).

---

## 6. Test plan

### 6.1 Unit tests — `tests/test_interface.py`

All tests use the existing `monkeypatch` + `MockResponse` pattern. No live HTTP. Added under a new `# ADMIN METADATA` section marker.

| Test | What it verifies |
|---|---|
| `test_list_admin_metadata_templates_empty` | Empty API response → empty DataFrame with expected columns. |
| `test_list_admin_metadata_templates_populated` | Populated response → one DataFrame row per template. |
| `test_get_admin_metadata_template_by_uid_success` | Happy path returns `pd.Series`. |
| `test_get_admin_metadata_template_by_uid_not_found` | 404 → `TemplateError`. |
| `test_list_admin_metadata_no_filters` | Fetches all pages when `limit="All"` (mock returns 2 pages, second page short). |
| `test_list_admin_metadata_with_filters` | `project_id`, `template_uid` (str), `date_from`, `date_to` correctly appear in the query params. |
| `test_list_admin_metadata_template_uid_list_joined_with_commas` | `template_uid=["a","b"]` → `?template=a,b`. |
| `test_list_admin_metadata_empty_result` | Empty result → empty DataFrame (not `None`). |
| `test_get_admin_metadata_success` | Returns dict as-is. |
| `test_get_admin_metadata_with_idno_string_project_id` | `project_id="MY_IDNO"` passed through verbatim into the path. |
| `test_get_admin_metadata_not_found` | 404 → `ValueError`. |
| `test_upsert_admin_metadata_success` | POST body is `{project_id, template_uid, metadata}` exactly. |
| `test_upsert_admin_metadata_strips_empty_values` | Nested empty strings / None values removed before send. |
| `test_upsert_admin_metadata_rejects_non_dict` | `metadata="foo"` → `ValueError`. |
| `test_upsert_admin_metadata_rejects_empty_template_uid` | `template_uid=""` → `ValueError`. |
| `test_patch_admin_metadata_multi_op_success` | Multi-op list lands in the body untouched apart from path normalisation. |
| `test_patch_admin_metadata_normalises_paths` | `path="foo/bar"` → `/foo/bar`. |
| `test_patch_admin_metadata_rejects_empty_list` | `patches=[]` → `ValueError`. |
| `test_patch_admin_metadata_rejects_invalid_op` | `op="upsert"` → `ValueError` via `validate_json_patches`. |
| `test_delete_admin_metadata_success` | POST to `data_remove/`, checker sees 404 → no exception. |
| `test_delete_admin_metadata_not_applied` | Checker still finds the record → `DeleteNotAppliedError`. |

**Mocking strategy for multi-call tests (`test_delete_admin_metadata_*`):** the existing test file already imports `itertools` for `itertools.chain` to queue multiple sequential `MockResponse` objects — same pattern is reused here.

### 6.2 Integration test — `tests/integration_test.py`

One end-to-end lifecycle test, guarded by the existing `API_KEY` / `API_URL` env var requirement. If no admin templates are available on the test instance the test is skipped with a clear message.

```python
def test_admin_metadata_lifecycle(live_me, temp_project):
    # 1. list_admin_metadata_templates — assert at least one template exists
    # 2. upsert_admin_metadata against (temp_project.id, first_template.uid)
    # 3. get_admin_metadata — assert round-trip payload matches
    # 4. patch_admin_metadata — one replace op on a single field
    # 5. get_admin_metadata again — assert the patched field is updated
    # 6. list_admin_metadata(project_id=temp_project.id) — assert the record is present
    # 7. delete_admin_metadata — then get_admin_metadata must raise
```

### 6.3 What the tests don't cover

- PDF generation, bulk export — out of scope.
- Admin-metadata Pydantic class generation — out of scope.
- `get_admin_metadata_edit_history` — out of scope.
- Live behaviour against older Metadata Editor versions that predate the admin metadata endpoints — out of scope; the package targets the current documented API.

---

## 7. Relationship to other work

### 7.1 Data360 sibling package (future, separate spec)

Strategic decision: the Data360-specific helpers in [`docs/publishing.py`](../../publishing.py) (SDMX schema parsing, indicator/database metadata summary building, Data360 payload shaping, `create_edit_metadata_project_indicator/database`, `trigger_update` DDH integration) will move into a **new sibling package** — tentatively `wb-data360-publishing` — that depends on `pymetadataeditor`. That package is out of scope for this spec and will be designed separately.

Implication for the current design: the admin-metadata API must be **ergonomic enough to use directly** from the sibling package without workaround helpers. In particular:

- `upsert_admin_metadata(project_id, template_uid, metadata)` replaces `add_data360_admin_metadata` cleanly.
- `list_admin_metadata(project_id=..., template_uid=...)` + `get_admin_metadata(...)` replaces the bespoke pagination + filtering in `export_admin_metadata_*`.
- The `clean_admin_metadata()` response-flattening helper stays in the sibling package — it is Data360-specific response shaping, not a general concern.

### 7.2 Future rounds in `pymetadataeditor`

Identified in the gap analysis, explicitly deferred:

- **Round 2a** — Pydantic/Excel parity for admin metadata: `get_admin_metadata_class`, `make_admin_metadata_outline`, `output_mode` on get/upsert.
- **Round 2b** — PDF export primitive: `get_project_pdf_by_id(id) -> bytes`.
- **Round 2c** — By-IDNO lookups: choice deferred between `id_format` param, parallel `*_by_idno` methods, or `resolve_idno_to_id` helper.
- **Round 2d** — `list_projects_in_collection(metadata_type=...)` filter.
- **Round 2e** — Filter projects by a custom attribute (generalisation of `get_meta_by_dataset_db`).
- **Round 3** — Generalise `patch_update_project_log_by_id` to accept `List[Dict]` multi-op patches, mirroring `patch_admin_metadata`.

### 7.3 Things this spec explicitly does **not** promise

- Backwards-compatibility shims for `publishing.py` — callers must update to the new methods; no alias layer.
- A `create_admin_metadata` / `update_admin_metadata` split. The underlying endpoint is one upsert and the public API reflects that.
- Any convenience around the `{status, data: [...]}` envelope the API returns for admin metadata. `get_admin_metadata` returns the body as-is. Response shaping is the caller's responsibility.

---

## 8. Risks & open questions

| Risk / question | Mitigation |
|---|---|
| `RequestsWithSpecificErrors` may not support multi-segment path interpolation for `GET /admin-metadata/data/{projectId}/{templateUid}`. | Verified during plan-writing by reading `requester.py`. If unsupported, build the path string directly in `interface.py` (see §4.3, option (b)). No widening of `requester.py` in this round. |
| The OpenAPI spec documents a response for `list_admin_metadata_templates` but does not pin a schema (`"200": description only`). Unknown exact column names. | `list_admin_metadata_templates` will handle whatever columns the API returns and normalise into a DataFrame. Tests use a representative mocked shape; integration test verifies against a real instance. |
| `get_admin_metadata` may return the record wrapped in a list (`data: [{...}]`) rather than a bare object, consistent with the publishing.py observations. | `get_admin_metadata` documentation says "returns the admin metadata record as returned by the API" — intentionally unopinionated. If real-world testing shows the wrapped-list shape, that is what gets returned. Response shaping is explicitly a caller responsibility (§7.3). The integration test will lock in the real shape. |
| `list_admin_metadata` pagination semantics are inferred from `list_projects`. The API's `data_query` endpoint may or may not return a `total` field. | Pagination logic uses page-length (`len(page) < 500` → stop) as the primary termination signal, with `total` as a secondary check if present. Matches the defensive strategy already used in `list_projects`. |
| Integration test requires admin templates to exist on the target instance. | Test is skipped with a clear message if `list_admin_metadata_templates()` returns an empty DataFrame. |
| Deleting admin metadata on a project the user no longer has read access to will leave the `delete_admin_metadata` checker unable to confirm. | The checker treats a "not found" response as success (delete confirmed). A permissions change mid-call would manifest as a 403 from the checker, which propagates — the delete itself may still have succeeded. This is an existing quirk of the `_delete_by_id` pattern and is not introduced by this spec. |

---

## 9. Rollout

1. Implement the 7 methods + unit tests.
2. Regenerate [`docs/API_Reference.md`](../../API_Reference.md) via `python make_docs.py`.
3. Update [`docs/skill.md`](../../skill.md), [`docs/modules/interface.md`](../../modules/interface.md), [`CLAUDE.md`](../../../CLAUDE.md).
4. Bump version to `0.4.0` in [`pyproject.toml`](../../../pyproject.toml).
5. Run the full unit test suite + ruff + pre-commit locally.
6. If a live test instance is available, run the integration lifecycle test.
7. PR to `main` with a clear changelog in the PR description.
8. Tag `v0.4.0` after merge.

No migration steps are required for existing users — the change is purely additive.
