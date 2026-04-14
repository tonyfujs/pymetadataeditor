# Admin Metadata CRUD Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 7 dict-only CRUD methods for administrative metadata to `MetadataEditor`, covering template discovery, query, get, upsert, patch, and delete.

**Architecture:** All 7 methods are added to `pymetadataeditor/interface.py` inside a new `# ADMIN METADATA` section. They delegate HTTP to the existing `self._apinterface` (`RequestsWithSpecificErrors`). No changes to `requester.py`, `templates.py`, `llm_helpers.py`. Reuses `validate_json_patches()` and `remove_empty_from_dict()` from `utils.py`.

**Tech Stack:** Python 3.11+, pandas, pydantic, requests (mocked in tests), pytest, ruff

**Spec:** [`docs/superpowers/specs/2026-04-09-admin-metadata-crud-design.md`](../specs/2026-04-09-admin-metadata-crud-design.md)

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `pymetadataeditor/interface.py` | Modify (lines ~1084-1113: delete stub; insert new section after line ~1270) | 7 new public methods |
| `tests/test_interface.py` | Modify (append new section at end, after line 929) | ~22 unit tests |
| `tests/integration_test.py` | Modify (append one lifecycle test) | 1 integration test |
| `docs/skill.md` | Modify | Add Admin Metadata capability group + workflow |
| `docs/modules/interface.md` | Modify | Add Admin Metadata method reference section |
| `CLAUDE.md` | Modify | Add architecture note about admin metadata namespace |
| `pyproject.toml` | Modify (line 3) | Version bump 0.3.2 -> 0.4.0 |

No new files are created inside the package source.

---

## Task 1: Clean up commented-out stub

**Files:**
- Modify: `pymetadataeditor/interface.py:1084-1113`

- [ ] **Step 1: Remove the commented-out `log_project_admin_metadata` stub**

Delete lines 1084-1113 in `pymetadataeditor/interface.py`. These lines contain a commented-out method that is superseded by this work.

The block to remove starts with `# def log_project_admin_metadata(` and ends with `#     return ret`. After removal, there should be a blank line between the end of `create_project_log` (the `return ret["id"]` at the former line 1082) and the `def update_project_log_by_id` method.

- [ ] **Step 2: Run ruff to confirm no lint issues**

Run: `poetry run ruff check pymetadataeditor/interface.py`
Expected: No errors (or only pre-existing warnings unrelated to this change).

- [ ] **Step 3: Commit**

```bash
git add pymetadataeditor/interface.py
git commit -m "refactor: remove commented-out log_project_admin_metadata stub

Superseded by the admin metadata CRUD design (see docs/superpowers/specs/2026-04-09-admin-metadata-crud-design.md)."
```

---

## Task 2: Add `list_admin_metadata_templates` and `get_admin_metadata_template_by_uid`

**Files:**
- Test: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (insert new section after the `# TEMPLATES` block, around line ~1270 after stub removal)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_interface.py`:

```python
####################################################################################################################
# ADMIN METADATA
####################################################################################################################


def test_list_admin_metadata_templates_populated(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(
            http_status_code=200,
            json_data={
                "templates": [
                    {"uid": "tpl_1", "name": "Template One", "type": "admin"},
                    {"uid": "tpl_2", "name": "Template Two", "type": "admin"},
                ]
            },
        )

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.list_admin_metadata_templates()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert "uid" in result.columns


def test_list_admin_metadata_templates_empty(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"templates": []})

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.list_admin_metadata_templates()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0


def test_get_admin_metadata_template_by_uid_success(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(
            http_status_code=200,
            json_data={"template": {"uid": "tpl_1", "name": "Template One", "type": "admin"}},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.get_admin_metadata_template_by_uid("tpl_1")
    assert isinstance(result, pd.Series)
    assert result["uid"] == "tpl_1"


def test_get_admin_metadata_template_by_uid_not_found(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=404)

    monkeypatch.setattr(requests, "request", mock_response)
    with pytest.raises(TemplateError):
        metadata_editor.get_admin_metadata_template_by_uid("nonexistent")
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `poetry run pytest tests/test_interface.py::test_list_admin_metadata_templates_populated tests/test_interface.py::test_list_admin_metadata_templates_empty tests/test_interface.py::test_get_admin_metadata_template_by_uid_success tests/test_interface.py::test_get_admin_metadata_template_by_uid_not_found -v`
Expected: FAIL — `AttributeError: 'MetadataEditor' object has no attribute 'list_admin_metadata_templates'`

- [ ] **Step 3: Implement the two methods**

In `pymetadataeditor/interface.py`, insert a new section after the `# TEMPLATES` section block (after line ~1270, the area containing `list_templates`, `get_template_by_uid`, `change_mode_or_template`, `delete_template`). Find the next section marker (`# EXCEL INTERFACE`) and insert before it.

```python
    ####################################################################################################################
    # ADMIN METADATA
    ####################################################################################################################

    def list_admin_metadata_templates(self) -> pd.DataFrame:
        """Retrieves all administrative metadata templates.

        Admin metadata templates are separate from project templates. They define the schema for
        administrative metadata that can be attached to projects.

        Returns:
            pd.DataFrame: A DataFrame of admin metadata templates. If none are found, an empty DataFrame is returned.

        Example:
            ```python
            me = MetadataEditor(api_url=api_url, api_key=api_key)
            templates = me.list_admin_metadata_templates()
            print(templates)
            ```
        """
        response = self._apinterface.get_request("admin-metadata/templates")
        templates = response.get("templates", [])
        if not templates:
            return pd.DataFrame()
        return pd.DataFrame(templates)

    def get_admin_metadata_template_by_uid(self, uid: str) -> pd.Series:
        """Retrieves a single administrative metadata template by UID.

        Args:
            uid (str): The unique identifier of the admin metadata template.

        Returns:
            pd.Series: The template record.

        Raises:
            TemplateError: If the template UID is not found.

        Example:
            ```python
            me = MetadataEditor(api_url=api_url, api_key=api_key)
            template = me.get_admin_metadata_template_by_uid("my_admin_template")
            print(template)
            ```
        """
        try:
            response = self._apinterface.get_request("admin-metadata/templates/{}", id=uid)
        except (HTTPError, PermissionError) as e:
            raise TemplateError(f"Admin metadata template '{uid}' not found.") from e
        return pd.Series(response.get("template", response))
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `poetry run pytest tests/test_interface.py::test_list_admin_metadata_templates_populated tests/test_interface.py::test_list_admin_metadata_templates_empty tests/test_interface.py::test_get_admin_metadata_template_by_uid_success tests/test_interface.py::test_get_admin_metadata_template_by_uid_not_found -v`
Expected: All 4 PASS.

- [ ] **Step 5: Run ruff**

Run: `poetry run ruff check pymetadataeditor/interface.py tests/test_interface.py`
Expected: No new errors.

- [ ] **Step 6: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add list_admin_metadata_templates and get_admin_metadata_template_by_uid"
```

---

## Task 3: Add `get_admin_metadata`

**Files:**
- Test: `tests/test_interface.py` (append)
- Modify: `pymetadataeditor/interface.py` (append to `# ADMIN METADATA` section)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_interface.py`:

```python
def test_get_admin_metadata_success(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(
            http_status_code=200,
            json_data={"template_uid": "tpl_1", "metadata": {"key": "value"}},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.get_admin_metadata(project_id=123, template_uid="tpl_1")
    assert isinstance(result, dict)
    assert result["metadata"]["key"] == "value"


def test_get_admin_metadata_with_idno_string_project_id(monkeypatch, metadata_editor):
    """project_id can be a string IDNO — it should be passed through verbatim."""
    captured_urls = []

    def mock_response(*args, **kwargs):
        captured_urls.append(args[1] if len(args) > 1 else kwargs.get("url", ""))
        return MockResponse(
            http_status_code=200,
            json_data={"template_uid": "tpl_1", "metadata": {}},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    metadata_editor.get_admin_metadata(project_id="MY_IDNO_123", template_uid="tpl_1")
    # The URL should contain the string IDNO, not a numeric conversion
    assert any("MY_IDNO_123" in str(url) for url in captured_urls)


def test_get_admin_metadata_not_found(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=404)

    monkeypatch.setattr(requests, "request", mock_response)
    with pytest.raises(ValueError, match="No admin metadata found"):
        metadata_editor.get_admin_metadata(project_id=999, template_uid="tpl_1")
```

- [ ] **Step 2: Run to verify they fail**

Run: `poetry run pytest tests/test_interface.py::test_get_admin_metadata_success tests/test_interface.py::test_get_admin_metadata_with_idno_string_project_id tests/test_interface.py::test_get_admin_metadata_not_found -v`
Expected: FAIL — `AttributeError: 'MetadataEditor' object has no attribute 'get_admin_metadata'`

- [ ] **Step 3: Implement**

Append to the `# ADMIN METADATA` section in `pymetadataeditor/interface.py`:

```python
    def get_admin_metadata(self, project_id: Union[int, str], template_uid: str) -> Dict:
        """Retrieves a single administrative metadata record.

        Admin metadata is keyed by (project_id, template_uid) pairs. A project can have multiple
        admin metadata records, one per template.

        Args:
            project_id (int or str): The project's numeric ID or string IDNO. Passed through verbatim
                to the API, which accepts either.
            template_uid (str): The admin metadata template UID.

        Returns:
            Dict: The admin metadata record as returned by the API.

        Raises:
            ValueError: If no admin metadata record exists for this (project_id, template_uid) pair.

        Example:
            ```python
            me = MetadataEditor(api_url=api_url, api_key=api_key)
            admin_meta = me.get_admin_metadata(project_id=123, template_uid="my_template")
            print(admin_meta)
            ```
        """
        pth = f"admin-metadata/data/{project_id}/" + "{}"
        try:
            response = self._apinterface.get_request(pth, id=template_uid)
        except (HTTPError, PermissionError) as e:
            raise ValueError(
                f"No admin metadata found for project_id={project_id}, template_uid={template_uid}"
            ) from e
        return response
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `poetry run pytest tests/test_interface.py::test_get_admin_metadata_success tests/test_interface.py::test_get_admin_metadata_with_idno_string_project_id tests/test_interface.py::test_get_admin_metadata_not_found -v`
Expected: All 3 PASS.

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add get_admin_metadata method"
```

---

## Task 4: Add `list_admin_metadata`

**Files:**
- Test: `tests/test_interface.py` (append)
- Modify: `pymetadataeditor/interface.py` (append to `# ADMIN METADATA` section)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_interface.py`:

```python
def test_list_admin_metadata_no_filters(monkeypatch, metadata_editor):
    """When limit='All', paginates internally. Mock two pages: first full (500), second short (2)."""
    call_count = [0]

    def mock_response(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            # First page: 500 rows
            return MockResponse(
                http_status_code=200,
                json_data={
                    "total": 502,
                    "data": [{"project_id": str(i), "template_uid": "tpl"} for i in range(500)],
                },
            )
        else:
            # Second page: 2 rows (short page → stop)
            return MockResponse(
                http_status_code=200,
                json_data={
                    "total": 502,
                    "data": [{"project_id": "500", "template_uid": "tpl"}, {"project_id": "501", "template_uid": "tpl"}],
                },
            )

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.list_admin_metadata()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 502


def test_list_admin_metadata_with_filters(monkeypatch, metadata_editor):
    captured_params = {}

    def mock_response(*args, **kwargs):
        # Capture the params from the URL query string
        url = args[1] if len(args) > 1 else kwargs.get("url", "")
        if "params" in kwargs:
            captured_params.update(kwargs["params"])
        return MockResponse(
            http_status_code=200,
            json_data={"data": [{"project_id": "1", "template_uid": "tpl_1"}], "total": 1},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    metadata_editor.list_admin_metadata(
        project_id="PROJ_1", template_uid="tpl_1", date_from="2026-01-01", date_to="2026-12-31", limit=50
    )
    assert captured_params.get("project_id") == "PROJ_1"
    assert captured_params.get("template") == "tpl_1"
    assert captured_params.get("date_from") == "2026-01-01"
    assert captured_params.get("date_to") == "2026-12-31"


def test_list_admin_metadata_template_uid_list_joined_with_commas(monkeypatch, metadata_editor):
    captured_params = {}

    def mock_response(*args, **kwargs):
        if "params" in kwargs:
            captured_params.update(kwargs["params"])
        return MockResponse(
            http_status_code=200,
            json_data={"data": [], "total": 0},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    metadata_editor.list_admin_metadata(template_uid=["tpl_a", "tpl_b"])
    assert captured_params.get("template") == "tpl_a,tpl_b"


def test_list_admin_metadata_passes_dates_verbatim(monkeypatch, metadata_editor):
    """Malformed dates are forwarded to the API unchanged — no client-side validation."""
    captured_params = {}

    def mock_response(*args, **kwargs):
        if "params" in kwargs:
            captured_params.update(kwargs["params"])
        return MockResponse(
            http_status_code=200,
            json_data={"data": [], "total": 0},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    metadata_editor.list_admin_metadata(date_from="not-a-date", limit=10)
    assert captured_params.get("date_from") == "not-a-date"


def test_list_admin_metadata_empty_result(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"data": [], "total": 0})

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.list_admin_metadata(limit=10)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
```

- [ ] **Step 2: Run to verify they fail**

Run: `poetry run pytest tests/test_interface.py -k "test_list_admin_metadata" -v`
Expected: FAIL — `AttributeError: 'MetadataEditor' object has no attribute 'list_admin_metadata'`

- [ ] **Step 3: Implement**

Append to the `# ADMIN METADATA` section in `pymetadataeditor/interface.py`:

```python
    def list_admin_metadata(
        self,
        project_id: Optional[Union[int, str]] = None,
        template_uid: Optional[Union[str, List[str]]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: Union[int, str] = "All",
        offset: int = 0,
    ) -> pd.DataFrame:
        """Query administrative metadata records across projects and templates.

        Paginates internally in batches of 500 when ``limit="All"`` (same convention as
        ``list_projects``).

        Args:
            project_id (int or str, optional): Filter by a single project ID or IDNO.
            template_uid (str or list of str, optional): Filter by one template UID, or a list of UIDs.
                List values are joined with commas before being sent to the API.
            date_from (str, optional): Inclusive lower bound on the ``changed`` field (YYYY-MM-DD).
                Passed through to the API without client-side validation.
            date_to (str, optional): Inclusive upper bound on the ``changed`` field (YYYY-MM-DD).
                Passed through to the API without client-side validation.
            limit (int or str): Max records to return, or ``"All"`` to fetch every page. Default is ``"All"``.
            offset (int): Starting offset. Ignored when ``limit="All"``. Default is 0.

        Returns:
            pd.DataFrame: One row per (project, template_uid) record. Empty DataFrame if none match.

        Example:
            ```python
            me = MetadataEditor(api_url=api_url, api_key=api_key)

            # Get all admin metadata
            all_admin = me.list_admin_metadata()

            # Filter by project and template
            filtered = me.list_admin_metadata(project_id=123, template_uid="my_template")

            # Filter by multiple templates
            multi = me.list_admin_metadata(template_uid=["tpl_a", "tpl_b"])
            ```
        """
        if isinstance(limit, str):
            assert limit.lower() == "all", f"Expected limit to be 'All' or a positive integer but got '{limit}'"
            new_offset = offset
            new_limit = 500
            dfs = []
            while True:
                df = self.list_admin_metadata(
                    project_id=project_id,
                    template_uid=template_uid,
                    date_from=date_from,
                    date_to=date_to,
                    offset=new_offset,
                    limit=new_limit,
                )
                dfs.append(df)
                if len(df) < new_limit:
                    break
                new_offset += new_limit
            return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

        params: Dict[str, Union[str, int]] = {"offset": offset, "limit": limit}
        if project_id is not None:
            params["project_id"] = str(project_id)
        if template_uid is not None:
            if isinstance(template_uid, list):
                params["template"] = ",".join(template_uid)
            else:
                params["template"] = template_uid
        if date_from is not None:
            params["date_from"] = date_from
        if date_to is not None:
            params["date_to"] = date_to

        response = self._apinterface.get_request("admin-metadata/data_query", params=params)
        data = response.get("data", [])
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `poetry run pytest tests/test_interface.py -k "test_list_admin_metadata" -v`
Expected: All 5 PASS.

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add list_admin_metadata with pagination and filters"
```

---

## Task 5: Add `upsert_admin_metadata`

**Files:**
- Test: `tests/test_interface.py` (append)
- Modify: `pymetadataeditor/interface.py` (append to `# ADMIN METADATA` section)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_interface.py`:

```python
def test_upsert_admin_metadata_success(monkeypatch, metadata_editor):
    captured_json = {}

    def mock_response(*args, **kwargs):
        if "json" in kwargs and kwargs["json"] is not None:
            captured_json.update(kwargs["json"])
        return MockResponse(http_status_code=200, json_data={"status": "ok"})

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.upsert_admin_metadata(
        project_id=123, template_uid="tpl_1", metadata={"key": "value"}
    )
    assert isinstance(result, dict)
    assert captured_json["project_id"] == 123
    assert captured_json["template_uid"] == "tpl_1"
    assert captured_json["metadata"] == {"key": "value"}


def test_upsert_admin_metadata_strips_empty_values(monkeypatch, metadata_editor):
    captured_json = {}

    def mock_response(*args, **kwargs):
        if "json" in kwargs and kwargs["json"] is not None:
            captured_json.update(kwargs["json"])
        return MockResponse(http_status_code=200, json_data={"status": "ok"})

    monkeypatch.setattr(requests, "request", mock_response)
    metadata_editor.upsert_admin_metadata(
        project_id=123, template_uid="tpl_1", metadata={"key": "value", "empty_key": "", "none_key": None}
    )
    # empty_key and none_key should be stripped by remove_empty_from_dict
    assert "empty_key" not in captured_json["metadata"]
    assert "none_key" not in captured_json["metadata"]
    assert captured_json["metadata"]["key"] == "value"


def test_upsert_admin_metadata_rejects_non_dict(metadata_editor):
    with pytest.raises(ValueError, match="metadata must be a dict"):
        metadata_editor.upsert_admin_metadata(project_id=123, template_uid="tpl_1", metadata="not a dict")


def test_upsert_admin_metadata_rejects_empty_template_uid(metadata_editor):
    with pytest.raises(ValueError, match="template_uid must be a non-empty string"):
        metadata_editor.upsert_admin_metadata(project_id=123, template_uid="", metadata={"key": "value"})
```

- [ ] **Step 2: Run to verify they fail**

Run: `poetry run pytest tests/test_interface.py -k "test_upsert_admin_metadata" -v`
Expected: FAIL — `AttributeError: 'MetadataEditor' object has no attribute 'upsert_admin_metadata'`

- [ ] **Step 3: Implement**

Append to the `# ADMIN METADATA` section in `pymetadataeditor/interface.py`:

```python
    def upsert_admin_metadata(
        self,
        project_id: Union[int, str],
        template_uid: str,
        metadata: Dict,
    ) -> Dict:
        """Creates or updates (upserts) an administrative metadata record.

        The Metadata Editor API uses a single upsert endpoint for admin metadata. If a record
        already exists for the (project_id, template_uid) pair, it is overwritten; otherwise a
        new one is created.

        Empty values in ``metadata`` are stripped before the request is sent (via
        ``remove_empty_from_dict``), matching the convention used by ``create_project_log``
        and ``update_project_log_by_id``.

        Args:
            project_id (int or str): The project's numeric ID or string IDNO.
            template_uid (str): The admin metadata template UID.
            metadata (dict): Admin metadata payload as a dict.

        Returns:
            Dict: The server response.

        Raises:
            ValueError: If ``metadata`` is not a dict, or if ``template_uid`` is empty.

        Example:
            ```python
            me = MetadataEditor(api_url=api_url, api_key=api_key)
            me.upsert_admin_metadata(
                project_id=123,
                template_uid="my_template",
                metadata={"section": {"field": "value"}},
            )
            ```
        """
        if not isinstance(metadata, dict):
            raise ValueError("metadata must be a dict")
        if not template_uid:
            raise ValueError("template_uid must be a non-empty string")

        post_json = {
            "project_id": project_id,
            "template_uid": template_uid,
            "metadata": remove_empty_from_dict(metadata),
        }
        return self._apinterface.post_request(pth="admin-metadata/data/", json=post_json)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `poetry run pytest tests/test_interface.py -k "test_upsert_admin_metadata" -v`
Expected: All 4 PASS.

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add upsert_admin_metadata method"
```

---

## Task 6: Add `patch_admin_metadata`

**Files:**
- Test: `tests/test_interface.py` (append)
- Modify: `pymetadataeditor/interface.py` (append to `# ADMIN METADATA` section)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_interface.py`:

```python
def test_patch_admin_metadata_multi_op_success(monkeypatch, metadata_editor):
    captured_json = {}

    def mock_response(*args, **kwargs):
        if "json" in kwargs and kwargs["json"] is not None:
            captured_json.update(kwargs["json"])
        return MockResponse(http_status_code=200, json_data={"status": "ok"})

    monkeypatch.setattr(requests, "request", mock_response)
    patches = [
        {"op": "replace", "path": "/section/field1", "value": "new_value"},
        {"op": "add", "path": "/section/field2", "value": "added"},
    ]
    result = metadata_editor.patch_admin_metadata(project_id=123, template_uid="tpl_1", patches=patches)
    assert isinstance(result, dict)
    assert captured_json["project_id"] == 123
    assert captured_json["template_uid"] == "tpl_1"
    assert len(captured_json["patches"]) == 2
    assert captured_json["patches"][0]["op"] == "replace"


def test_patch_admin_metadata_normalises_paths(monkeypatch, metadata_editor):
    captured_json = {}

    def mock_response(*args, **kwargs):
        if "json" in kwargs and kwargs["json"] is not None:
            captured_json.update(kwargs["json"])
        return MockResponse(http_status_code=200, json_data={"status": "ok"})

    monkeypatch.setattr(requests, "request", mock_response)
    # Path without leading / should get / prepended by validate_json_patches
    metadata_editor.patch_admin_metadata(
        project_id=123, template_uid="tpl_1", patches=[{"op": "replace", "path": "foo/bar", "value": "baz"}]
    )
    assert captured_json["patches"][0]["path"] == "/foo/bar"


def test_patch_admin_metadata_rejects_empty_list(metadata_editor):
    with pytest.raises(ValueError):
        metadata_editor.patch_admin_metadata(project_id=123, template_uid="tpl_1", patches=[])


def test_patch_admin_metadata_rejects_invalid_op(metadata_editor):
    with pytest.raises(ValueError, match="Invalid operation"):
        metadata_editor.patch_admin_metadata(
            project_id=123, template_uid="tpl_1", patches=[{"op": "upsert", "path": "/foo", "value": "bar"}]
        )
```

- [ ] **Step 2: Run to verify they fail**

Run: `poetry run pytest tests/test_interface.py -k "test_patch_admin_metadata" -v`
Expected: FAIL — `AttributeError: 'MetadataEditor' object has no attribute 'patch_admin_metadata'`

- [ ] **Step 3: Implement**

Append to the `# ADMIN METADATA` section in `pymetadataeditor/interface.py`:

```python
    def patch_admin_metadata(
        self,
        project_id: Union[int, str],
        template_uid: str,
        patches: List[Dict],
    ) -> Dict:
        """Applies JSON Patch (RFC 6902) operations to an admin metadata record.

        Unlike ``patch_update_project_log_by_id``, this method accepts a list of patch operations
        and applies them atomically. The underlying admin metadata patch endpoint natively supports
        multi-op patches.

        Each patch operation is a dict with ``op``, ``path``, and optionally ``value`` and ``from``
        keys. Paths that do not start with ``/`` are auto-corrected.

        Args:
            project_id (int or str): The project's numeric ID or string IDNO.
            template_uid (str): The admin metadata template UID.
            patches (list of dict): List of JSON Patch operations, e.g.
                ``[{"op": "replace", "path": "/foo", "value": "bar"}, ...]``.

        Returns:
            Dict: The server response.

        Raises:
            ValueError: If ``patches`` is empty, or any op is not a valid RFC 6902 verb, or
                required fields are missing for the given op.

        Example:
            ```python
            me = MetadataEditor(api_url=api_url, api_key=api_key)
            me.patch_admin_metadata(
                project_id=123,
                template_uid="my_template",
                patches=[
                    {"op": "replace", "path": "/section/field", "value": "new_value"},
                    {"op": "add", "path": "/section/new_field", "value": "added"},
                ],
            )
            ```
        """
        if not patches:
            raise ValueError("patches must be a non-empty list of JSON Patch operations")
        validated_patches = validate_json_patches(patches)
        post_json = {
            "project_id": project_id,
            "template_uid": template_uid,
            "patches": validated_patches,
        }
        return self._apinterface.post_request(pth="admin-metadata/data_patch/", json=post_json)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `poetry run pytest tests/test_interface.py -k "test_patch_admin_metadata" -v`
Expected: All 4 PASS.

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add patch_admin_metadata with multi-op JSON Patch support"
```

---

## Task 7: Add `delete_admin_metadata`

**Files:**
- Test: `tests/test_interface.py` (append)
- Modify: `pymetadataeditor/interface.py` (append to `# ADMIN METADATA` section)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_interface.py`:

```python
class MockGetAdminMetadata:
    """Mock for get_admin_metadata that either returns data or raises ValueError."""

    def __init__(self, exists: bool):
        self.exists = exists

    def __call__(self, *args, **kwargs):
        if self.exists:
            return {"template_uid": "tpl_1", "metadata": {"key": "value"}}
        else:
            raise ValueError("No admin metadata found")


def test_delete_admin_metadata_success(monkeypatch, metadata_editor):
    """Delete succeeds: POST returns OK, subsequent get raises ValueError (record gone)."""
    monkeypatch.setattr(metadata_editor, "get_admin_metadata", MockGetAdminMetadata(exists=False))

    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"status": "ok"})

    monkeypatch.setattr(RequestsWithSpecificErrors, "post_request", mock_response)
    # Should not raise
    metadata_editor.delete_admin_metadata(project_id=123, template_uid="tpl_1")


def test_delete_admin_metadata_not_applied(monkeypatch, metadata_editor):
    """Delete fails: POST returns OK, but subsequent get still finds the record."""
    monkeypatch.setattr(metadata_editor, "get_admin_metadata", MockGetAdminMetadata(exists=True))

    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"status": "ok"})

    monkeypatch.setattr(RequestsWithSpecificErrors, "post_request", mock_response)
    with pytest.raises(DeleteNotAppliedError):
        metadata_editor.delete_admin_metadata(project_id=123, template_uid="tpl_1")
```

- [ ] **Step 2: Run to verify they fail**

Run: `poetry run pytest tests/test_interface.py -k "test_delete_admin_metadata" -v`
Expected: FAIL — `AttributeError: 'MetadataEditor' object has no attribute 'delete_admin_metadata'`

- [ ] **Step 3: Implement**

Append to the `# ADMIN METADATA` section in `pymetadataeditor/interface.py`:

```python
    def delete_admin_metadata(self, project_id: Union[int, str], template_uid: str):
        """Deletes an administrative metadata record.

        After sending the delete request, verifies the record was actually removed by attempting
        to retrieve it. If the record still exists, raises ``DeleteNotAppliedError``.

        Args:
            project_id (int or str): The project's numeric ID or string IDNO.
            template_uid (str): The admin metadata template UID.

        Raises:
            DeleteNotAppliedError: If the API does not confirm the delete (the record still exists
                after the request).

        Example:
            ```python
            me = MetadataEditor(api_url=api_url, api_key=api_key)
            me.delete_admin_metadata(project_id=123, template_uid="my_template")
            ```
        """
        post_json = {
            "project_id": project_id,
            "template_uid": template_uid,
        }
        try:
            self._apinterface.post_request(pth="admin-metadata/data_remove/", json=post_json)
        except JSONDecodeError:
            pass

        # Verify the record was deleted
        try:
            self.get_admin_metadata(project_id, template_uid)
        except (ValueError, HTTPError, PermissionError, JSONDecodeError):
            pass  # Record is gone — delete confirmed
        else:
            raise DeleteNotAppliedError()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `poetry run pytest tests/test_interface.py -k "test_delete_admin_metadata" -v`
Expected: Both PASS.

- [ ] **Step 5: Run the full test suite**

Run: `poetry run pytest tests/test_interface.py -v`
Expected: All existing tests still pass, plus all ~22 new admin metadata tests pass.

- [ ] **Step 6: Run ruff on all changed files**

Run: `poetry run ruff check pymetadataeditor/interface.py tests/test_interface.py && poetry run ruff format --check pymetadataeditor/interface.py tests/test_interface.py`
Expected: No errors.

- [ ] **Step 7: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add delete_admin_metadata method

Completes the 7-method admin metadata CRUD surface."
```

---

## Task 8: Update documentation

**Files:**
- Modify: `docs/skill.md`
- Modify: `docs/modules/interface.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update `docs/skill.md`**

Under the `## Key Capabilities` section, after `### Resources (File Attachments)` and before `### Low-Level Access`, add:

```markdown
### Admin Metadata
- **List admin metadata templates** — discover available administrative metadata template UIDs
- **Get admin metadata template** — retrieve a single admin template by UID
- **List admin metadata** — query admin metadata records, filterable by project, template, date range
- **Get admin metadata** — retrieve a single admin metadata record by (project_id, template_uid)
- **Upsert admin metadata** — create or update an admin metadata record (dict only in this version)
- **Patch admin metadata** — apply multi-op JSON Patch (RFC 6902) to an admin metadata record
- **Delete admin metadata** — remove an admin metadata record
```

Under `## Common Workflows`, add a new subsection after the last numbered workflow:

```markdown
### 7. Manage admin metadata for a project

```python
me = MetadataEditor(api_url=..., api_key=...)

# Discover available admin templates
templates = me.list_admin_metadata_templates()
print(templates)

# Attach admin metadata to a project
me.upsert_admin_metadata(
    project_id=123,
    template_uid="my_admin_template",
    metadata={"section": {"field": "value"}},
)

# Read it back
admin_meta = me.get_admin_metadata(project_id=123, template_uid="my_admin_template")

# Patch a single field
me.patch_admin_metadata(
    project_id=123,
    template_uid="my_admin_template",
    patches=[{"op": "replace", "path": "/section/field", "value": "updated"}],
)

# Delete
me.delete_admin_metadata(project_id=123, template_uid="my_admin_template")
`` `
```

- [ ] **Step 2: Update `docs/modules/interface.md`**

After the `### Resources (File Attachments)` section and before `### Generic / Low-Level`, add a new section:

```markdown
### Admin Metadata

#### `list_admin_metadata_templates() -> pd.DataFrame`

Returns a DataFrame of all administrative metadata templates. Admin templates are separate from project templates.

---

#### `get_admin_metadata_template_by_uid(uid) -> pd.Series`

```python
def get_admin_metadata_template_by_uid(self, uid: str) -> pd.Series
```

Returns details of a single admin metadata template. Raises `TemplateError` if the UID is not found.

---

#### `list_admin_metadata(project_id, template_uid, date_from, date_to, limit, offset) -> pd.DataFrame`

```python
def list_admin_metadata(
    self,
    project_id: Optional[Union[int, str]] = None,
    template_uid: Optional[Union[str, List[str]]] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: Union[int, str] = "All",
    offset: int = 0,
) -> pd.DataFrame
```

Queries admin metadata records with optional filters. Paginates internally when `limit="All"`.

---

#### `get_admin_metadata(project_id, template_uid) -> Dict`

```python
def get_admin_metadata(self, project_id: Union[int, str], template_uid: str) -> Dict
```

Retrieves a single admin metadata record. Raises `ValueError` if not found. `project_id` accepts both numeric IDs and string IDNOs.

---

#### `upsert_admin_metadata(project_id, template_uid, metadata) -> Dict`

```python
def upsert_admin_metadata(
    self,
    project_id: Union[int, str],
    template_uid: str,
    metadata: Dict,
) -> Dict
```

Creates or updates an admin metadata record. The API uses a single upsert endpoint. Empty values are stripped from `metadata` before sending.

---

#### `patch_admin_metadata(project_id, template_uid, patches) -> Dict`

```python
def patch_admin_metadata(
    self,
    project_id: Union[int, str],
    template_uid: str,
    patches: List[Dict],
) -> Dict
```

Applies multi-op JSON Patch (RFC 6902) operations atomically. Paths without leading `/` are auto-corrected.

```python
me.patch_admin_metadata(
    project_id=123,
    template_uid="my_template",
    patches=[{"op": "replace", "path": "/field", "value": "new"}],
)
```

---

#### `delete_admin_metadata(project_id, template_uid)`

```python
def delete_admin_metadata(self, project_id: Union[int, str], template_uid: str)
```

Deletes an admin metadata record. Raises `DeleteNotAppliedError` if the record still exists after the request.
```

- [ ] **Step 3: Update `CLAUDE.md`**

Under `## Architecture & Key Conventions`, after the `### Empty value handling` subsection, add:

```markdown
### Admin metadata

Admin metadata is a separate namespace from project metadata, with its own template registry (`/admin-metadata/templates`) and its own CRUD endpoints. It is **not** hooked into `list_templates()` or `self._templates`. Multi-op JSON Patch is supported on admin metadata but not (yet) on project metadata. Admin metadata records are keyed by `(project_id, template_uid)` pairs — a single project can have multiple admin metadata records, one per template.
```

- [ ] **Step 4: Regenerate API docs**

Run: `python make_docs.py`
Expected: `docs/API_Reference.md` is updated with the 7 new method docstrings.

- [ ] **Step 5: Run ruff on all changed files**

Run: `poetry run ruff check pymetadataeditor/ && poetry run ruff format --check pymetadataeditor/`
Expected: No errors.

- [ ] **Step 6: Commit**

```bash
git add docs/skill.md docs/modules/interface.md CLAUDE.md docs/API_Reference.md
git commit -m "docs: add admin metadata CRUD to skill docs, interface reference, and CLAUDE.md"
```

---

## Task 9: Version bump and final validation

**Files:**
- Modify: `pyproject.toml` (line 3)

- [ ] **Step 1: Bump version**

In `pyproject.toml`, change line 3:

```
version = "0.3.2"
```

to:

```
version = "0.4.0"
```

- [ ] **Step 2: Run the full test suite**

Run: `poetry run pytest tests/test_interface.py -v`
Expected: All tests pass (existing + ~22 new).

- [ ] **Step 3: Run pre-commit hooks on all staged files**

Run: `poetry run pre-commit run --all-files`
Expected: All hooks pass (ruff lint, ruff format, detect-secrets).

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "chore: bump version to 0.4.0 for admin metadata CRUD release"
```

---

## Task 10: Integration test (optional — requires live API)

**Files:**
- Modify: `tests/integration_test.py` (append)

This task is only executable if a live Metadata Editor instance is available with admin templates configured. Skip if not.

- [ ] **Step 1: Add the lifecycle test**

Append to `tests/integration_test.py`:

```python
def test_admin_metadata_lifecycle(me):
    """End-to-end: upsert, get, patch, list, delete admin metadata."""
    # 1. List admin templates — need at least one
    templates = me.list_admin_metadata_templates()
    if templates.empty:
        pytest.skip("No admin metadata templates available on this instance")
    template_uid = templates.iloc[0]["uid"]

    # 2. Create a throwaway project to attach admin metadata to
    from pymetadataeditor import MetadataEditor

    outline = me.make_metadata_outline("indicator", "dict")
    outline["series_description"]["idno"] = "ADMIN_META_TEST_TEMP"
    outline["series_description"]["name"] = "Admin metadata lifecycle test"
    project_id = me.create_project_log(outline, "indicator")

    try:
        # 3. Upsert admin metadata
        me.upsert_admin_metadata(
            project_id=project_id, template_uid=template_uid, metadata={"test_field": "test_value"}
        )

        # 4. Get it back
        admin_meta = me.get_admin_metadata(project_id=project_id, template_uid=template_uid)
        assert isinstance(admin_meta, dict)

        # 5. Patch a field
        me.patch_admin_metadata(
            project_id=project_id,
            template_uid=template_uid,
            patches=[{"op": "replace", "path": "/test_field", "value": "patched_value"}],
        )

        # 6. Get again — verify patch applied
        admin_meta = me.get_admin_metadata(project_id=project_id, template_uid=template_uid)
        # Response shape depends on the API — we just verify it's a dict and didn't error

        # 7. List with project filter
        listed = me.list_admin_metadata(project_id=project_id)
        assert isinstance(listed, pd.DataFrame)
        assert len(listed) >= 1

        # 8. Delete
        me.delete_admin_metadata(project_id=project_id, template_uid=template_uid)

        # 9. Verify get raises after delete
        with pytest.raises(ValueError, match="No admin metadata found"):
            me.get_admin_metadata(project_id=project_id, template_uid=template_uid)

    finally:
        # Clean up the throwaway project
        me.delete_project_by_id(project_id)
```

- [ ] **Step 2: Run (only if live API is available)**

Run: `API_KEY=your_key API_URL=https://your-instance.org/index.php/api poetry run pytest tests/integration_test.py::test_admin_metadata_lifecycle -v`
Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/integration_test.py
git commit -m "test: add admin metadata lifecycle integration test"
```
