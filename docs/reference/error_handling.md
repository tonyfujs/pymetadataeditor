# Error Handling

pyMetadataEditor translates every non-success response from the Metadata Editor API into a semantic, catchable Python exception. The goal is twofold:

- you see a readable, actionable message by default (no bare `HTTPError: 403` tracebacks), and
- you can still catch errors programmatically at whatever level of specificity you need.

All API-layer exceptions inherit from [`requests.exceptions.HTTPError`](https://requests.readthedocs.io/en/latest/api/#requests.exceptions.HTTPError), so existing `except HTTPError` handlers continue to fire.

---

## Exception hierarchy

```
requests.exceptions.HTTPError
└── MetadataEditorAPIError              # base class — catch this for "any API error"
    ├── AuthenticationError              # 401 / 403 or key-level denial
    ├── ProjectAccessError               # 4xx with "permission denied" / "unauthorized" wording
    ├── ResourceNotFoundError            # 404, or connection failure reaching the API
    ├── BadRequestError                  # other 4xx (validation, malformed payload, …)
    └── ServerError                      # 5xx — transient server-side failure
```

Import them from the package root:

```python
from pymetadataeditor import (
    MetadataEditorAPIError,
    AuthenticationError,
    ProjectAccessError,
    ResourceNotFoundError,
    BadRequestError,
    ServerError,
)
```

Every instance exposes structured context so you can branch on the underlying cause without string-matching the message:

| Attribute | Type | Description |
|-----------|------|-------------|
| `status_code` | `int \| None` | HTTP status code returned by the API |
| `api_message` | `str \| None` | The `message` field from the API's JSON error body |
| `url` | `str \| None` | The full URL that was requested |
| `response` | `requests.Response \| None` | The raw response, for deep inspection |

---

## How responses are mapped

| Situation | HTTP status | Exception raised |
|-----------|-------------|------------------|
| Missing / invalid / revoked API key | `401`, `403` | `AuthenticationError` |
| API key OK but forbidden for this project or collection | `4xx` with "permission", "forbidden", "unauthorized", … | `ProjectAccessError` |
| Project, template, collection, or endpoint does not exist | `404`, or 4xx with "not found" / "does not exist" | `ResourceNotFoundError` |
| Network unreachable (no response at all) | — | `ResourceNotFoundError` |
| Malformed payload, validation error, other client errors | other `4xx` | `BadRequestError` |
| Metadata Editor server error | `5xx` | `ServerError` |
| Anything unrecognised | any | `MetadataEditorAPIError` (the base) |

The mapping uses the HTTP status code first, then the API's `message` field to distinguish permission-denied from not-found on generic 4xx responses.

---

## Handling errors

### Catch-all pattern

```python
from pymetadataeditor import MetadataEditorAPIError

try:
    me.create_project_log(metadata)
except MetadataEditorAPIError as e:
    print(f"Request to {e.url} failed with status {e.status_code}: {e.api_message}")
```

### Branching on cause

```python
from pymetadataeditor import (
    AuthenticationError,
    ProjectAccessError,
    ResourceNotFoundError,
    ServerError,
)

try:
    me.get_project_metadata_by_id(project_id, "dict")
except AuthenticationError:
    # Prompt the user to re-enter or refresh their API key
    ...
except ProjectAccessError:
    # Grant access via assign_collection_project_access / assign_collection_acl
    ...
except ResourceNotFoundError:
    # The id doesn't exist (or network can't reach the API)
    ...
except ServerError:
    # Retry with backoff — the server is temporarily unhealthy
    ...
```

### Retrying server errors

Only `ServerError` (5xx) is safe to retry blindly. Everything else indicates a bad request or missing resource and should bubble up.

```python
import time
from pymetadataeditor import ServerError

for attempt in range(3):
    try:
        me.list_projects()
        break
    except ServerError:
        if attempt == 2:
            raise
        time.sleep(2 ** attempt)
```

---

## Package-level exceptions

In addition to the HTTP hierarchy above, two conditions raise their own exceptions:

### `DeleteNotAppliedError`

The API accepted the delete request but the record still exists on a follow-up check — usually the signing API key has been restricted from deletions.

```python
from pymetadataeditor.interface import DeleteNotAppliedError

try:
    me.delete_project_by_id(id=1042)
except DeleteNotAppliedError as e:
    print(f"Deletion blocked: {e}")
```

Raised by:

- `delete_project_by_id()`
- `delete_collection_by_id()`
- `delete_resource_by_id()`
- `delete_template()`
- `delete_admin_metadata()`

### `TemplateError`

A template UID was not found, or the template is incompatible with the requested metadata type.

```python
from pymetadataeditor.interface import TemplateError

try:
    me.make_metadata_outline("NOT_A_REAL_UID", output_mode="pydantic")
except TemplateError as e:
    print(f"Template error: {e}")
    print(me.list_templates())
```

Common causes:

- A template UID that does not exist in the instance (verify with `me.list_templates()`)
- Using a template from one metadata type against a project of a different type
- Referencing a template that was later deleted

---

## SSL & network

### SSL certificate failures

If the API's SSL certificate cannot be verified, `requests.exceptions.SSLError` is re-raised with a pointer toward the workaround:

```python
me = MetadataEditor(api_url=api_url, api_key=api_key, verify_ssl=False)
```

### Connection failures

If the server is unreachable (DNS failure, timeout, refused connection), a `ResourceNotFoundError` is raised with a message explaining the URL could not be reached.

### SSL warnings

With `verify_ssl=False`, `urllib3` emits `InsecureRequestWarning` once per unique URL. This is expected for instances with self-signed certificates; filter it with the standard `warnings` module if noisy, but only in trusted deployments.

---

## Backwards compatibility

- All new exceptions subclass `requests.exceptions.HTTPError`, so existing `except HTTPError` blocks keep working.
- Code that inspected `response.status_code` on a raised `HTTPError` still works: the same attribute is available on every `MetadataEditorAPIError`.
- The previous `DeleteNotAppliedError` and `TemplateError` behaviours are unchanged.
