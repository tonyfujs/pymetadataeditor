# User & Permission Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add user lookup and collection permission management methods to `MetadataEditor`, wrapping all user and permission-related API endpoints.

**Architecture:** All new methods go directly on the `MetadataEditor` class in `interface.py`, following existing patterns. User methods are placed in a new `# USER METHODS` section before collection methods. Permission methods go in a new `# COLLECTION PERMISSION METHODS` section after the existing collection methods and before `# RESOURCE METHODS`. Tests use `MockResponse` with `monkeypatch` in `test_interface.py`.

**Tech Stack:** Python 3.11+, pandas, requests, pytest

**Spec:** [docs/superpowers/specs/2026-04-15-user-and-permission-management-design.md](../specs/2026-04-15-user-and-permission-management-design.md)

---

## File Map

| Action | File | Responsibility |
|--------|------|----------------|
| Modify | `pymetadataeditor/interface.py:1706` | Add `# USER METHODS` section before `# COLLECTION METHODS` |
| Modify | `pymetadataeditor/interface.py:1985` | Add `# COLLECTION PERMISSION METHODS` section after `set_template_for_collection` and before `# RESOURCE METHODS` |
| Modify | `tests/test_interface.py:1223` | Add tests for all new methods at end of file |
| Modify | `docs/modules/interface.md` | Add "Users" and "Collection Permissions" sections |
| Modify | `docs/skill.md` | Add capability groups for new methods |

---

### Task 1: `list_users` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py:1706` (insert before `# COLLECTION METHODS`)

- [ ] **Step 1: Write the failing test**

Add to the end of `tests/test_interface.py`:

```python
def test_list_users(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(
            http_status_code=200,
            json_data={"status": "success", "users": [{"id": 1, "email": "alice@example.com", "username": "alice"}]},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    users = metadata_editor.list_users()
    assert isinstance(users, pd.DataFrame)
    assert len(users) == 1
    assert users.loc[1, "email"] == "alice@example.com"

    # empty users list
    def mock_response_empty(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"status": "success", "users": []})

    monkeypatch.setattr(requests, "request", mock_response_empty)
    users = metadata_editor.list_users()
    assert isinstance(users, pd.DataFrame)
    assert len(users) == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_list_users -v`
Expected: FAIL with `AttributeError: 'MetadataEditor' object has no attribute 'list_users'`

- [ ] **Step 3: Write minimal implementation**

Insert before the `# COLLECTION METHODS` line (line 1706) in `pymetadataeditor/interface.py`:

```python
    ####################################################################################################################
    # USER METHODS
    ####################################################################################################################

    def list_users(self) -> pd.DataFrame:
        """List all users registered in the Metadata Editor instance.

        Returns:
            pd.DataFrame: User information including id, email, and username.
        """
        response = self._apinterface.get_request("users")
        if "users" not in response or len(response["users"]) == 0:
            return pd.DataFrame([], columns=["id", "email", "username"]).set_index("id")
        df = pd.DataFrame(response["users"]).set_index("id")
        try:
            new_index = df.index.astype(int)
        except ValueError:
            pass
        else:
            df.index = new_index
        return df

```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_list_users -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add list_users method"
```

---

### Task 2: `find_user_by_email` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (after `list_users`)

- [ ] **Step 1: Write the failing tests**

Add to the end of `tests/test_interface.py`:

```python
def test_find_user_by_email(monkeypatch, metadata_editor):
    users_data = {
        "status": "success",
        "users": [
            {"id": 1, "email": "alice@example.com", "username": "alice"},
            {"id": 2, "email": "bob@example.com", "username": "bob"},
        ],
    }

    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data=users_data)

    monkeypatch.setattr(requests, "request", mock_response)

    # find by email
    assert metadata_editor.find_user_by_email(email="alice@example.com") == 1

    # find by email case-insensitive
    assert metadata_editor.find_user_by_email(email="ALICE@EXAMPLE.COM") == 1

    # find by name fallback
    assert metadata_editor.find_user_by_email(email="", name="bob") == 2

    # not found
    assert metadata_editor.find_user_by_email(email="nobody@example.com") is None

    # email takes priority over name when both provided
    assert metadata_editor.find_user_by_email(email="alice@example.com", name="bob") == 1

    # empty inputs raise ValueError
    with pytest.raises(ValueError):
        metadata_editor.find_user_by_email(email="", name="")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_find_user_by_email -v`
Expected: FAIL with `AttributeError: 'MetadataEditor' object has no attribute 'find_user_by_email'`

- [ ] **Step 3: Write minimal implementation**

Add after `list_users` in `pymetadataeditor/interface.py`:

```python
    def find_user_by_email(self, email: str, name: str = "") -> Optional[int]:
        """Look up a user's ID by email (primary) or username (fallback).

        Args:
            email (str): The user's email address to search for.
            name (str): Optional username to match against if email is not sufficient.

        Returns:
            Optional[int]: The user's integer ID if found, otherwise None.

        Raises:
            ValueError: If both email and name are empty.
        """
        email_lower = email.strip().lower() if email else ""
        name_lower = name.strip().lower() if name else ""

        if not email_lower and not name_lower:
            raise ValueError("At least one of email or name must be provided")

        users_df = self.list_users()
        if users_df.empty:
            return None

        for _, user in users_df.iterrows():
            user_email = str(user.get("email", "")).lower()
            user_name = str(user.get("username", "")).lower()

            email_match = bool(email_lower and user_email == email_lower)
            name_match = bool(name_lower and user_name == name_lower)

            if email_match or name_match:
                return int(user.name)  # .name is the pandas Series index, which is the user's id

        return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_find_user_by_email -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add find_user_by_email method"
```

---

### Task 3: `list_collection_project_access` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (insert after `set_template_for_collection`, before `# RESOURCE METHODS`)

- [ ] **Step 1: Write the failing test**

Add to the end of `tests/test_interface.py`:

```python
def test_list_collection_project_access(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(
            http_status_code=200,
            json_data={"users": [{"user_id": 1, "email": "alice@example.com", "permissions": ["view"]}]},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.list_collection_project_access(collection_id=10)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]["email"] == "alice@example.com"

    # empty result
    def mock_response_empty(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"users": []})

    monkeypatch.setattr(requests, "request", mock_response_empty)
    result = metadata_editor.list_collection_project_access(collection_id=10)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_list_collection_project_access -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Write minimal implementation**

Insert after `set_template_for_collection` (line 1985) and before `# RESOURCE METHODS` in `pymetadataeditor/interface.py`:

```python
    ####################################################################################################################
    # COLLECTION PERMISSION METHODS
    ####################################################################################################################

    def list_collection_project_access(self, collection_id: int) -> pd.DataFrame:
        """List users with project access in a collection.

        Args:
            collection_id (int): The ID of the collection.

        Returns:
            pd.DataFrame: Users with project access in the collection.
        """
        response = self._apinterface.get_request("collections/user_project_access/{}", id=collection_id)
        users = response.get("users", [])
        if not users:
            return pd.DataFrame([], columns=["user_id", "email", "permissions"])
        return pd.DataFrame(users)

```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_list_collection_project_access -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add list_collection_project_access method"
```

---

### Task 4: `assign_collection_project_access` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (after `list_collection_project_access`)

- [ ] **Step 1: Write the failing tests**

Add to the end of `tests/test_interface.py`:

```python
def test_assign_collection_project_access(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"status": "success"})

    monkeypatch.setattr(requests, "request", mock_response)

    # basic assign with list of permissions
    result = metadata_editor.assign_collection_project_access(collection_id=10, user_id=1, permissions=["view"])
    assert result == {"status": "success"}

    # string permission gets wrapped in list
    result = metadata_editor.assign_collection_project_access(collection_id=10, user_id=1, permissions="view")
    assert result == {"status": "success"}

    # recursive raises NotImplementedError
    with pytest.raises(NotImplementedError):
        metadata_editor.assign_collection_project_access(collection_id=10, user_id=1, permissions=["view"], recursive=True)

    # empty permissions raises ValueError
    with pytest.raises(ValueError):
        metadata_editor.assign_collection_project_access(collection_id=10, user_id=1, permissions=[])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_assign_collection_project_access -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Write minimal implementation**

Add after `list_collection_project_access` in `pymetadataeditor/interface.py`:

```python
    def assign_collection_project_access(
        self,
        collection_id: int,
        user_id: int,
        permissions: Union[List[str], str],
        recursive: bool = False,
    ) -> Optional[dict]:
        """Assign project access permissions for a user within a collection.

        Args:
            collection_id (int): The collection to grant access to.
            user_id (int): The target user's ID.
            permissions (Union[List[str], str]): Permission level(s) to assign (e.g. "view").
            recursive (bool): If True, apply to child collections as well. Not yet implemented.

        Returns:
            Optional[dict]: Parsed response JSON on success, None on failure.

        Raises:
            NotImplementedError: If recursive=True (not yet implemented).
            ValueError: If permissions is empty.
        """
        if recursive:
            raise NotImplementedError("Recursive permissions require collection hierarchy support — not yet implemented")

        if isinstance(permissions, str):
            permissions = [permissions]

        if not permissions:
            raise ValueError("permissions must not be empty")

        collection_id = int(collection_id)
        user_id = int(user_id)

        response = self._apinterface.post_request(
            "collections/user_project_access",
            json={"collection_id": collection_id, "user_id": user_id, "permissions": permissions},
        )
        return response
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_assign_collection_project_access -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add assign_collection_project_access method"
```

---

### Task 5: `remove_collection_project_access` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (after `assign_collection_project_access`)

- [ ] **Step 1: Write the failing tests**

Add to the end of `tests/test_interface.py`:

```python
def test_remove_collection_project_access(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"status": "success"})

    monkeypatch.setattr(requests, "request", mock_response)

    result = metadata_editor.remove_collection_project_access(collection_id=10, user_id=1)
    assert result == {"status": "success"}

    # recursive raises NotImplementedError
    with pytest.raises(NotImplementedError):
        metadata_editor.remove_collection_project_access(collection_id=10, user_id=1, recursive=True)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_remove_collection_project_access -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Write minimal implementation**

Add after `assign_collection_project_access` in `pymetadataeditor/interface.py`:

```python
    def remove_collection_project_access(
        self, collection_id: int, user_id: int, recursive: bool = False
    ) -> Optional[dict]:
        """Remove project access permissions for a user within a collection.

        Args:
            collection_id (int): The collection to revoke access from.
            user_id (int): The target user's ID.
            recursive (bool): If True, apply to child collections as well. Not yet implemented.

        Returns:
            Optional[dict]: Parsed response JSON on success, None on failure.

        Raises:
            NotImplementedError: If recursive=True (not yet implemented).
        """
        if recursive:
            raise NotImplementedError("Recursive permissions require collection hierarchy support — not yet implemented")

        collection_id = int(collection_id)
        user_id = int(user_id)

        response = self._apinterface.post_request(
            "collections/remove_user_project_access",
            json={"collection_id": collection_id, "user_id": user_id},
        )
        return response
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_remove_collection_project_access -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add remove_collection_project_access method"
```

---

### Task 6: `list_collection_acl` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (after `remove_collection_project_access`)

- [ ] **Step 1: Write the failing test**

Add to the end of `tests/test_interface.py`:

```python
def test_list_collection_acl(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(
            http_status_code=200,
            json_data={"users": [{"user_id": 1, "email": "alice@example.com", "permissions": ["edit"]}]},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.list_collection_acl(collection_id=10)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]["email"] == "alice@example.com"

    # empty result
    def mock_response_empty(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"users": []})

    monkeypatch.setattr(requests, "request", mock_response_empty)
    result = metadata_editor.list_collection_acl(collection_id=10)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_list_collection_acl -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Write minimal implementation**

Add after `remove_collection_project_access` in `pymetadataeditor/interface.py`:

```python
    def list_collection_acl(self, collection_id: int) -> pd.DataFrame:
        """List users with ACL access to a collection.

        Args:
            collection_id (int): The ID of the collection.

        Returns:
            pd.DataFrame: Users with ACL access to the collection.
        """
        response = self._apinterface.get_request("collections/user_acl/{}", id=collection_id)
        users = response.get("users", [])
        if not users:
            return pd.DataFrame([], columns=["user_id", "email", "permissions"])
        return pd.DataFrame(users)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_list_collection_acl -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add list_collection_acl method"
```

---

### Task 7: `check_collection_acl` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (after `list_collection_acl`)

- [ ] **Step 1: Write the failing test**

Add to the end of `tests/test_interface.py`:

```python
def test_check_collection_acl(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(
            http_status_code=200,
            json_data={"status": "success", "has_access": True},
        )

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.check_collection_acl(collection_id=10, user_id=1)
    assert result == {"status": "success", "has_access": True}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_check_collection_acl -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Write minimal implementation**

Add after `list_collection_acl` in `pymetadataeditor/interface.py`:

```python
    def check_collection_acl(self, collection_id: int, user_id: int) -> dict:
        """Check if a user has ACL access to a collection.

        Args:
            collection_id (int): The ID of the collection.
            user_id (int): The ID of the user to check.

        Returns:
            dict: Parsed response JSON indicating whether the user has ACL access.
        """
        pth = f"collections/user_acl_check/{int(collection_id)}/{int(user_id)}"
        response = self._apinterface.get_request(pth)
        return response
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_check_collection_acl -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add check_collection_acl method"
```

---

### Task 8: `assign_collection_acl` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (after `check_collection_acl`)

- [ ] **Step 1: Write the failing tests**

Add to the end of `tests/test_interface.py`:

```python
def test_assign_collection_acl(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"status": "success"})

    monkeypatch.setattr(requests, "request", mock_response)

    result = metadata_editor.assign_collection_acl(collection_id=10, user_id=1, permissions=["edit"])
    assert result == {"status": "success"}

    # string permission gets wrapped in list
    result = metadata_editor.assign_collection_acl(collection_id=10, user_id=1, permissions="edit")
    assert result == {"status": "success"}

    # recursive raises NotImplementedError
    with pytest.raises(NotImplementedError):
        metadata_editor.assign_collection_acl(collection_id=10, user_id=1, permissions=["edit"], recursive=True)

    # empty permissions raises ValueError
    with pytest.raises(ValueError):
        metadata_editor.assign_collection_acl(collection_id=10, user_id=1, permissions=[])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_assign_collection_acl -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Write minimal implementation**

Add after `check_collection_acl` in `pymetadataeditor/interface.py`:

```python
    def assign_collection_acl(
        self,
        collection_id: int,
        user_id: int,
        permissions: Union[List[str], str],
        recursive: bool = False,
    ) -> Optional[dict]:
        """Assign ACL access to a collection for a user.

        Args:
            collection_id (int): The collection to grant ACL access to.
            user_id (int): The target user's ID.
            permissions (Union[List[str], str]): Permission level(s) to assign.
            recursive (bool): If True, apply to child collections as well. Not yet implemented.

        Returns:
            Optional[dict]: Parsed response JSON on success, None on failure.

        Raises:
            NotImplementedError: If recursive=True (not yet implemented).
            ValueError: If permissions is empty.
        """
        if recursive:
            raise NotImplementedError("Recursive permissions require collection hierarchy support — not yet implemented")

        if isinstance(permissions, str):
            permissions = [permissions]

        if not permissions:
            raise ValueError("permissions must not be empty")

        collection_id = int(collection_id)
        user_id = int(user_id)

        response = self._apinterface.post_request(
            "collections/user_acl",
            json={"collection_id": collection_id, "user_id": user_id, "permissions": permissions},
        )
        return response
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_assign_collection_acl -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add assign_collection_acl method"
```

---

### Task 9: `update_collection_acl` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (after `assign_collection_acl`)

- [ ] **Step 1: Write the failing tests**

Add to the end of `tests/test_interface.py`:

```python
def test_update_collection_acl(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"status": "success"})

    monkeypatch.setattr(requests, "request", mock_response)

    result = metadata_editor.update_collection_acl(collection_id=10, user_id=1, permissions=["admin"])
    assert result == {"status": "success"}

    # string permission gets wrapped in list
    result = metadata_editor.update_collection_acl(collection_id=10, user_id=1, permissions="admin")
    assert result == {"status": "success"}

    # recursive raises NotImplementedError
    with pytest.raises(NotImplementedError):
        metadata_editor.update_collection_acl(collection_id=10, user_id=1, permissions=["admin"], recursive=True)

    # empty permissions raises ValueError
    with pytest.raises(ValueError):
        metadata_editor.update_collection_acl(collection_id=10, user_id=1, permissions=[])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_update_collection_acl -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Write minimal implementation**

Add after `assign_collection_acl` in `pymetadataeditor/interface.py`:

```python
    def update_collection_acl(
        self,
        collection_id: int,
        user_id: int,
        permissions: Union[List[str], str],
        recursive: bool = False,
    ) -> Optional[dict]:
        """Update ACL permissions for a user on a collection.

        Args:
            collection_id (int): The collection to update ACL access for.
            user_id (int): The target user's ID.
            permissions (Union[List[str], str]): New permission level(s) to set.
            recursive (bool): If True, apply to child collections as well. Not yet implemented.

        Returns:
            Optional[dict]: Parsed response JSON on success, None on failure.

        Raises:
            NotImplementedError: If recursive=True (not yet implemented).
            ValueError: If permissions is empty.
        """
        if recursive:
            raise NotImplementedError("Recursive permissions require collection hierarchy support — not yet implemented")

        if isinstance(permissions, str):
            permissions = [permissions]

        if not permissions:
            raise ValueError("permissions must not be empty")

        collection_id = int(collection_id)
        user_id = int(user_id)

        response = self._apinterface.post_request(
            "collections/user_acl_update",
            json={"collection_id": collection_id, "user_id": user_id, "permissions": permissions},
        )
        return response
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_update_collection_acl -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add update_collection_acl method"
```

---

### Task 10: `remove_collection_acl` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (after `update_collection_acl`)

- [ ] **Step 1: Write the failing tests**

Add to the end of `tests/test_interface.py`:

```python
def test_remove_collection_acl(monkeypatch, metadata_editor):
    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data={"status": "success"})

    monkeypatch.setattr(requests, "request", mock_response)

    result = metadata_editor.remove_collection_acl(collection_id=10, user_id=1)
    assert result == {"status": "success"}

    # recursive raises NotImplementedError
    with pytest.raises(NotImplementedError):
        metadata_editor.remove_collection_acl(collection_id=10, user_id=1, recursive=True)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_remove_collection_acl -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Write minimal implementation**

Add after `update_collection_acl` in `pymetadataeditor/interface.py`:

```python
    def remove_collection_acl(self, collection_id: int, user_id: int, recursive: bool = False) -> Optional[dict]:
        """Remove ACL access from a collection for a user.

        Args:
            collection_id (int): The collection to revoke ACL access from.
            user_id (int): The target user's ID.
            recursive (bool): If True, apply to child collections as well. Not yet implemented.

        Returns:
            Optional[dict]: Parsed response JSON on success, None on failure.

        Raises:
            NotImplementedError: If recursive=True (not yet implemented).
        """
        if recursive:
            raise NotImplementedError("Recursive permissions require collection hierarchy support — not yet implemented")

        collection_id = int(collection_id)
        user_id = int(user_id)

        response = self._apinterface.post_request(
            "collections/user_acl_remove",
            json={"collection_id": collection_id, "user_id": user_id},
        )
        return response
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_remove_collection_acl -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add remove_collection_acl method"
```

---

### Task 11: `get_collection_permissions` — test and implement

**Files:**
- Modify: `tests/test_interface.py` (append at end)
- Modify: `pymetadataeditor/interface.py` (after `remove_collection_acl`)

- [ ] **Step 1: Write the failing test**

Add to the end of `tests/test_interface.py`:

```python
def test_get_collection_permissions(monkeypatch, metadata_editor):
    permissions_data = {
        "status": "success",
        "user_id": 5,
        "is_admin": False,
        "admin_type": "none",
        "collections": {
            "10": {
                "id": 10,
                "title": "Test Collection",
                "permission_level": "edit",
                "can_edit": True,
                "can_admin": False,
                "can_delete": False,
                "can_manage_access": False,
                "can_add_projects": True,
                "can_remove_projects": True,
            }
        },
    }

    def mock_response(*args, **kwargs):
        return MockResponse(http_status_code=200, json_data=permissions_data)

    monkeypatch.setattr(requests, "request", mock_response)
    result = metadata_editor.get_collection_permissions()
    assert result["user_id"] == 5
    assert result["is_admin"] is False
    assert "10" in result["collections"]
    assert result["collections"]["10"]["permission_level"] == "edit"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run pytest tests/test_interface.py::test_get_collection_permissions -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Write minimal implementation**

Add after `remove_collection_acl` in `pymetadataeditor/interface.py`:

```python
    def get_collection_permissions(self) -> dict:
        """Get the authenticated user's permission summary across all collections.

        Returns:
            dict: Permission summary including user_id, is_admin, admin_type,
                and a collections dict keyed by collection ID with permission details.
        """
        response = self._apinterface.get_request("collections/permissions")
        return response
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run pytest tests/test_interface.py::test_get_collection_permissions -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "feat: add get_collection_permissions method"
```

---

### Task 12: Run full test suite

- [ ] **Step 1: Run all tests to ensure nothing is broken**

Run: `poetry run pytest tests/test_interface.py -v`
Expected: All tests PASS (existing + new)

- [ ] **Step 2: Run ruff lint and format**

Run: `poetry run ruff check pymetadataeditor/ && poetry run ruff format pymetadataeditor/`
Expected: No errors

- [ ] **Step 3: Fix any issues found, then commit**

```bash
git add pymetadataeditor/interface.py tests/test_interface.py
git commit -m "chore: fix lint issues from permission methods"
```

(Skip this commit if no fixes were needed.)

---

### Task 13: Update documentation

**Files:**
- Modify: `docs/modules/interface.md`
- Modify: `docs/skill.md`

- [ ] **Step 1: Add Users section to `docs/modules/interface.md`**

Add a new `## Users` section with method documentation for `list_users` and `find_user_by_email`, following the existing format in the file.

- [ ] **Step 2: Add Collection Permissions section to `docs/modules/interface.md`**

Add a new `## Collection Permissions` section with method documentation for all 8 permission methods:
- `list_collection_project_access`
- `assign_collection_project_access`
- `remove_collection_project_access`
- `list_collection_acl`
- `check_collection_acl`
- `assign_collection_acl`
- `update_collection_acl`
- `remove_collection_acl`
- `get_collection_permissions`

- [ ] **Step 3: Add capability groups to `docs/skill.md`**

Add entries for "User Management" and "Collection Permissions" capability groups in the appropriate section of `docs/skill.md`.

- [ ] **Step 4: Regenerate API Reference**

Run: `python make_docs.py`

- [ ] **Step 5: Commit**

```bash
git add docs/
git commit -m "docs: add user and permission management documentation"
```
