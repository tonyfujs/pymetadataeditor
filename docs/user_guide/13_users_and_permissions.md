# Managing Users & Collection Permissions

pyMetadataEditor lets you look up users by email or username and grant them two independent kinds of access to a collection:

| Tier | What it controls | Methods |
|------|------------------|---------|
| **Project access** | Who can see / edit the projects *inside* a collection | `list_collection_project_access` · `assign_collection_project_access` · `remove_collection_project_access` |
| **ACL (Access Control List)** | Who can administer the collection itself (edit its metadata, change membership, …) | `list_collection_acl` · `check_collection_acl` · `assign_collection_acl` · `update_collection_acl` · `remove_collection_acl` |
| **Permission summary** | What the *current* API key can do across every collection on the instance | `get_collection_permissions` |

The two tiers are separate: granting project access does **not** grant ACL access, and vice versa. Grant both if a user needs to both work on projects and administer the collection.

---

## Find a user

Most permission methods take an integer `user_id`. Resolve a user from their email address (preferred) or username:

```python
from pymetadataeditor import MetadataEditor

me = MetadataEditor(api_url=api_url, api_key=api_key)

# All registered users on the instance (indexed by id; columns: email, username)
users = me.list_users()

# Look up a single user id — email match takes priority
user_id = me.find_user_by_email("alice@example.com")

# Fall back to username when you don't know the email
user_id = me.find_user_by_email("", name="alice")

# Pass both and email wins if it resolves to a user
user_id = me.find_user_by_email("alice@example.com", name="alice")
```

`find_user_by_email` raises `ValueError` if:

- both `email` and `name` are empty,
- the supplied `email` is not a syntactically valid address (validated via the Rust-backed [`emval`](https://github.com/bnkc/emval) library), or
- no user matches the supplied email/username.

!!! tip
    `list_users()` is the best way to discover a user's exact stored email/username before calling the lookup — matches are case-insensitive, but spaces and accents must match exactly.

---

## Project access (tier 1)

Project access controls which projects inside a collection a user can see or edit. Start by listing who has what:

```python
access_df = me.list_collection_project_access(collection_id=5)
#   user_id  email                permissions
#   42       alice@example.com    view
#   99       bob@example.com      edit
```

### Grant project access

```python
me.assign_collection_project_access(
    collection_id=5,
    user_id=42,
    permissions="view",          # or a list: ["view", "download"]
)
```

- `permissions` can be a string or list of strings.
- `recursive=True` is reserved for a future release and will raise `NotImplementedError`.

### Revoke project access

```python
me.remove_collection_project_access(collection_id=5, user_id=42)
```

---

## Collection ACL (tier 2)

ACL controls administrative rights over the collection itself. The workflow mirrors project access but the methods take a single `permissions` string and add an explicit *update* step:

```python
# Who has ACL access today?
me.list_collection_acl(collection_id=5)

# Does a specific user?
me.check_collection_acl(collection_id=5, user_id=42)

# Grant it
me.assign_collection_acl(collection_id=5, user_id=42, permissions="edit")

# Later, promote them to admin
me.update_collection_acl(collection_id=5, user_id=42, permissions="admin")

# Or remove their ACL access entirely
me.remove_collection_acl(collection_id=5, user_id=42)
```

Parameter notes:

- `permissions` is a single string. Passing a list raises `TypeError`; passing `""` raises `ValueError`.
- `recursive=True` is not yet implemented and raises `NotImplementedError`.
- `assign_collection_acl` will fail if the user already has ACL access — use `update_collection_acl` to change an existing assignment.

---

## Inspect your own permissions

`get_collection_permissions()` returns the permission summary for the API key currently in use — useful for validating a deployment or showing a capability banner in an app:

```python
me.get_collection_permissions()
# {
#   "user_id": 42,
#   "is_admin": False,
#   "admin_type": None,
#   "collections": {
#       5: {"project_access": "edit", "acl": "admin"},
#       8: {"project_access": "view", "acl": None},
#   },
# }
```

---

## End-to-end: onboard a new collaborator

```python
# 1. Resolve the colleague's user id
user_id = me.find_user_by_email("alice@example.com")

# 2. Let them work on projects in the collection
me.assign_collection_project_access(
    collection_id=5, user_id=user_id, permissions="edit"
)

# 3. Let them administer the collection itself
me.assign_collection_acl(
    collection_id=5, user_id=user_id, permissions="edit"
)

# 4. Verify
assert me.check_collection_acl(collection_id=5, user_id=user_id)
print(me.list_collection_project_access(collection_id=5))
print(me.list_collection_acl(collection_id=5))
```

---

## Error handling

Permission methods raise the [standard exception hierarchy](../reference/error_handling.md):

- `AuthenticationError` — the API key is missing or rejected
- `ProjectAccessError` — the key is valid but doesn't allow administering the target collection
- `ResourceNotFoundError` — the `collection_id` or `user_id` doesn't exist
- `BadRequestError` — the server rejected the `permissions` value (e.g. not recognised on that instance)

All inherit from `MetadataEditorAPIError` (and ultimately `requests.exceptions.HTTPError`), so existing error handlers keep working.

```python
from pymetadataeditor import ProjectAccessError, ResourceNotFoundError

try:
    me.assign_collection_acl(collection_id=5, user_id=42, permissions="admin")
except ResourceNotFoundError:
    print("No such collection or user")
except ProjectAccessError:
    print("Your API key can't administer collection 5")
```
