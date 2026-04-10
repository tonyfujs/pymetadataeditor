# Error Handling

pyMetadataEditor raises two custom exceptions in addition to standard Python and HTTP errors.

---

## `DeleteNotAppliedError`

**When it occurs:** A delete request was accepted by the API but the deletion was not confirmed. This typically means that a system administrator has restricted deletion rights for your API key.

```python
from pymetadataeditor import DeleteNotAppliedError

try:
    me.delete_project_by_id(id=1042)
except DeleteNotAppliedError as e:
    print(f"Deletion blocked: {e}")
    # Contact your system administrator to adjust permissions
```

This exception is raised by:
- `delete_project_by_id()`
- `delete_collection_by_id()`
- `delete_resource_by_id()`
- `delete_template()`

---

## `TemplateError`

**When it occurs:** A template UID was not found, the template is incompatible with the requested operation, or the metadata type doesn't match the template.

```python
from pymetadataeditor import TemplateError

try:
    me.make_metadata_outline("INVALID_TEMPLATE_UID", output_mode="pydantic")
except TemplateError as e:
    print(f"Template error: {e}")
    # Check available templates with me.list_templates()
```

Common causes:
- Passing a template UID that doesn't exist in your instance (verify with `me.list_templates()`)
- Trying to use a template from one metadata type with a project of a different type
- Referencing a template that was deleted

---

## HTTP errors

Network and API errors are raised as `requests.exceptions.HTTPError` with descriptive messages that include the HTTP status code and response body. Common cases:

| Situation | HTTP status | Likely cause |
|-----------|------------|-------------|
| Wrong API key | `403 Forbidden` | API key is invalid or revoked |
| Project not found | `404 Not Found` | The `id` doesn't exist or you don't have access |
| Invalid request | `400 Bad Request` | Malformed metadata or missing required fields |
| Server error | `500 Internal Server Error` | Metadata Editor instance issue — contact administrator |

---

## SSL warnings

If `verify_ssl=False`, an `InsecureRequestWarning` is shown once per unique warning message. This is expected behavior when connecting to instances with self-signed certificates.

To suppress the warning entirely, you can filter it with Python's `warnings` module — but this is not recommended, as it may hide legitimate security issues.
