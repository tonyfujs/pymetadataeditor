# User & Permission Management — Design Spec

**Date:** 2026-04-15
**Status:** Approved
**Scope:** Add user lookup and collection permission management methods to `MetadataEditor`

---

## Problem

`pymetadataeditor` wraps the Metadata Editor REST API but has no methods for user lookup or permission management. The API provides endpoints for:

- Listing users
- Managing collection project access (who can work on projects within a collection)
- Managing collection ACL (who can manage the collection itself)
- Inspecting a user's permissions across collections

These are needed for workflows where data owners/requesters are automatically granted access to collections when datasets are created, and the internal data team needs default project access and ACL edit access.

---

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture | Flat methods on `MetadataEditor` | CLAUDE.md mandates monolithic class; matches existing patterns |
| Recursive permissions | `recursive=False` parameter on each method | Discoverable, no method proliferation |
| Recursive implementation | Deferred (`NotImplementedError` when `True`) | Collection hierarchy response structure not yet available |
| User lookup | `list_users()` + `find_user_by_email()` convenience | Full CRUD client needs the raw list; convenience method covers the common workflow |
| Return types | DataFrame for list endpoints, dict for single-item/action endpoints | Matches existing conventions (`list_collections()` returns DataFrame, action methods return dict) |
| Permission inspection | Returns raw dict (not DataFrame) | Nested structure doesn't flatten cleanly into tabular form |
| Admin metadata template permissions | Deferred | API endpoints not confirmed |

---

## New Methods

### User Methods

New section `# USER METHODS` in `interface.py`, placed before collection methods.

#### `list_users() -> pd.DataFrame`

- **Requester path:** `"users"` (resolves to `GET {api_url}/users`)
- **Returns:** DataFrame with columns including `id`, `email`, `username`
- **Pattern:** Mirrors `list_collections()`
- **Note:** The `/users` endpoint is not documented in the OpenAPI spec (`metadata-editor-api.yaml`) but is used in the reference implementation (`docs/user_permissions.py`). Needs verification against the live API.

#### `find_user_by_email(email: str, name: str = "") -> int`

- Convenience wrapper around `list_users()`
- Fetches all users, normalizes email/name to lowercase, matches against `email` (primary) or `username` (fallback)
- Returns the user's integer `id`
- Raises `ValueError` when: both `email` and `name` are empty, the email is syntactically invalid, or no user matches the supplied email/name. Email syntax is checked via the Rust-backed `emval` library rather than a handwritten rule — it handles RFC 5321/5322 edge cases (IDN domains, quoted local parts, etc.) and is substantially faster than the pure-Python `email-validator`. `emval` raises Python's builtin `SyntaxError` on bad input; we wrap that in a `ValueError` whose message names the offending value so callers can surface it to the end user.
- **Design note:** Named `find_user_by_email` (vs `lookup_user_id` in the reference implementation) to better describe the primary lookup path. The `name` parameter is a fallback, not an independent search path.

---

### Collection Project Access Methods

Wrap endpoints that control which users can work on projects within a collection.

**Note:** The API does not provide a separate update endpoint for project access (unlike ACL). To change project permissions, remove and re-assign.

#### `list_collection_project_access(collection_id: int) -> pd.DataFrame`

- **Requester path:** `"collections/user_project_access/{}"` (with `id=collection_id`)
- **Returns:** DataFrame of users with project access in the collection

#### `assign_collection_project_access(collection_id: int, user_id: int, permissions: list[str] | str, recursive: bool = False) -> dict | None`

- **Requester path:** `"collections/user_project_access"`
- **Payload:** `{"collection_id": int, "user_id": int, "permissions": [...]}`
- If `permissions` is a string, wraps it in a list
- Returns parsed response JSON on success, `None` on failure
- `recursive=True`: raises `NotImplementedError` until hierarchy support is implemented

#### `remove_collection_project_access(collection_id: int, user_id: int, recursive: bool = False) -> dict | None`

- **Requester path:** `"collections/remove_user_project_access"`
- **Payload:** `{"collection_id": int, "user_id": int}`
- Same recursive behavior

---

### Collection ACL Methods

Wrap endpoints that control who can manage the collection itself (edit properties, manage access).

#### `list_collection_acl(collection_id: int) -> pd.DataFrame`

- **Requester path:** `"collections/user_acl/{}"` (with `id=collection_id`)
- **Returns:** DataFrame of users with ACL access to the collection

#### `check_collection_acl(collection_id: int, user_id: int) -> dict`

- **Requester path:** `"collections/user_acl_check/{collectionId}/{userId}"` — note: this endpoint takes two path params, so the requester's single `id` substitution won't work. Construct the path manually: `f"collections/user_acl_check/{collection_id}/{user_id}"`
- **Returns:** Parsed response JSON indicating whether the user has ACL access

#### `assign_collection_acl(collection_id: int, user_id: int, permissions: str, recursive: bool = False) -> dict | None`

- **Requester path:** `"collections/user_acl"`
- **Payload:** `{"collection_id": int, "user_id": int, "permissions": "<level>"}`
- `permissions` is a single string (e.g. `"view"`, `"edit"`, `"admin"`) — the API expects a scalar, not a list
- Raises `TypeError` if `permissions` is not a string, `ValueError` if it is empty, and `NotImplementedError` if `recursive=True`

#### `update_collection_acl(collection_id: int, user_id: int, permissions: str, recursive: bool = False) -> dict | None`

- **Requester path:** `"collections/user_acl_update"`
- **Payload:** same shape as assign (scalar `permissions` string)
- The API has an explicit update endpoint for ACL (unlike project access)

#### `remove_collection_acl(collection_id: int, user_id: int, recursive: bool = False) -> dict | None`

- **Requester path:** `"collections/user_acl_remove"`
- **Payload:** `{"collection_id": int, "user_id": int}`

---

### Permission Inspection

#### `get_collection_permissions() -> dict`

- **Requester path:** `"collections/permissions"`
- **Returns:** Dict containing the authenticated user's permission summary (subset of key fields shown; full response passed through):
  - `user_id: int`
  - `is_admin: bool`
  - `admin_type: str` (one of `"global"`, `"collection"`, `"none"`)
  - `collections: dict` keyed by collection ID, each containing:
    - `id`, `title`, `description`, `pid` (parent collection ID), `permission_level` (`"view"`, `"edit"`, `"admin"`)
    - `can_edit`, `can_admin`, `can_delete`, `can_manage_access`, `can_add_projects`, `can_remove_projects` (all bool)
    - Plus `created_by`, `created`, `changed`, `owner_username`
- **Note:** The `pid` field in each collection entry represents the parent collection ID — this is the key to implementing recursive permissions in the future.

---

## Recursive Permissions (Deferred Implementation)

### Design

- All assign/remove/update permission methods accept `recursive: bool = False`
- When `recursive=True`, the method resolves child collections and applies the operation to the target plus all children
- Initial release raises `NotImplementedError("Recursive permissions require collection hierarchy support — not yet implemented")` when `recursive=True`

### Internal helper (to be implemented)

```python
def _get_child_collection_ids(self, collection_id: int) -> list[int]:
    """Return IDs of all child collections under the given collection."""
    ...
```

- Single place for hierarchy resolution logic
- The `CollectionPermission` schema includes a `pid` (parent ID) field that may provide the hierarchy data needed. Implementation depends on confirming this field is reliably populated in list responses.

---

## Deferred Items

| Item | Reason | Unblocks when |
|------|--------|---------------|
| Recursive permission implementation | Collection hierarchy response structure not yet confirmed (`pid` field in `CollectionPermission` is a likely path) | User confirms `pid` field behavior or provides response structure |
| Admin metadata template permissions | API endpoints not confirmed | API team confirms endpoints |
| Team-based permissions | Future addition mentioned in requirements | API support available |

---

## Error Handling

- Input validation at method level: type coercion for `collection_id`/`user_id` to `int`, `permissions` must be a non-empty string, valid email format where applicable
- HTTP errors surfaced via `raise_for_status()` through `requester.py`, following existing patterns
- `find_user_by_email` raises `ValueError` when the email is syntactically invalid or no user matches — callers can surface the message verbatim. It never returns `None`.

---

## Testing

- Unit tests in `tests/test_interface.py` using `MockResponse`
- One test per method minimum, plus edge cases:
  - `find_user_by_email`: user found by email, found by name, not found raises `ValueError`, malformed email raises `ValueError`, empty input raises `ValueError`
  - Permission methods: success, HTTP error handling
  - `recursive=True`: raises `NotImplementedError`
- No integration tests in this iteration (require live API with permission to modify access)

---

## Documentation Updates

1. Add methods to `docs/modules/interface.md` under new "Users" and "Collection Permissions" sections
2. Add capability groups to `docs/skill.md`
3. Regenerate `docs/API_Reference.md` via `python make_docs.py`

---

## API Endpoint Summary

| Method | HTTP | Requester path | Payload |
|--------|------|----------------|---------|
| `list_users` | GET | `"users"` | — |
| `find_user_by_email` | — | (wraps `list_users`) | — |
| `list_collection_project_access` | GET | `"collections/user_project_access/{}"` | — |
| `assign_collection_project_access` | POST | `"collections/user_project_access"` | `{collection_id, user_id, permissions}` |
| `remove_collection_project_access` | POST | `"collections/remove_user_project_access"` | `{collection_id, user_id}` |
| `list_collection_acl` | GET | `"collections/user_acl/{}"` | — |
| `check_collection_acl` | GET | `f"collections/user_acl_check/{cid}/{uid}"` | — |
| `assign_collection_acl` | POST | `"collections/user_acl"` | `{collection_id, user_id, permissions}` |
| `update_collection_acl` | POST | `"collections/user_acl_update"` | `{collection_id, user_id, permissions}` |
| `remove_collection_acl` | POST | `"collections/user_acl_remove"` | `{collection_id, user_id}` |
| `get_collection_permissions` | GET | `"collections/permissions"` | — |

## Permissions Values

The `UserCollectionAccess` schema in the OpenAPI spec defines permissions as an array of strings with only `"view"` in the enum. This appears incomplete — the actual valid values likely include `"view"`, `"edit"`, `"admin"` based on the `CollectionPermission` response schema's `permission_level` field. Project-access methods continue to accept a list or a single string (normalized to a list before POSTing). ACL methods (`assign_collection_acl`, `update_collection_acl`) accept a single string only — the ACL API endpoints expect a scalar. No client-side validation of permission values will be added; the API will reject invalid values.
