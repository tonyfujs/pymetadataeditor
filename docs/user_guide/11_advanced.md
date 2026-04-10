# Advanced Usage

This section covers lower-level capabilities for users who need to go beyond the standard methods.

---

## Generic API requests

`generic_api_request()` lets you make raw HTTP requests to any endpoint on the Metadata Editor API. Use this to access endpoints that aren't yet wrapped by a dedicated method, or to experiment with new API features.

```python
# GET request with query parameters
response = me.generic_api_request(
    method="GET",
    endpoint="/editor",
    params={"limit": 5, "offset": 0},
)

# POST request with JSON body
response = me.generic_api_request(
    method="POST",
    endpoint="/editor/my-endpoint",
    json={"key": "value"},
)

# POST request with file upload
with open("document.pdf", "rb") as f:
    response = me.generic_api_request(
        method="POST",
        endpoint="/editor/1042/resources",
        files={"file": f},
        data={"title": "My Document"},
    )
```

The response is always returned as a Python dictionary.

!!! tip
    Check the Metadata Editor's own API documentation for available endpoints and their expected parameters.

---

## Working with Pydantic model classes directly

`get_metadata_class()` returns the Pydantic class for a metadata type. This is useful for custom validation, building metadata objects from scratch without an API call, or introspecting the schema programmatically:

```python
IndicatorClass = me.get_metadata_class("indicator")

# Build an instance directly
instance = IndicatorClass()

# Inspect available fields at any level
import inspect
print(list(IndicatorClass.model_fields.keys()))
```

---

## JSON Patch path reference

`patch_update_project_log_by_id()` uses [RFC 6902 JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901) paths. Key rules:

- Paths are `/`-separated, starting from the root of the metadata document
- Array indices are integers: `/series_description/topics/0/name` = first topic's name
- The leading `/` is added automatically if you omit it
- To reference a key that contains `/`, escape it as `~1`; to reference a key containing `~`, escape it as `~0`

```python
# Navigate deep into nested structures
me.patch_update_project_log_by_id(
    id=1042,
    op="replace",
    path="/series_description/topics/0/vocabulary",
    value="JEL",
)
```

---

## Custom exceptions

pyMetadataEditor raises two custom exceptions:

**`DeleteNotAppliedError`** — Raised when a delete request is sent but the API does not confirm the deletion (typically due to administrator-level restrictions).

**`TemplateError`** — Raised when a template UID is not found, the template is incompatible with the requested operation, or there is another template-related validation failure.

Both are importable directly from the package:

```python
from pymetadataeditor import MetadataEditor, DeleteNotAppliedError, TemplateError
```

See [Error Handling](../reference/error_handling.md) for full detail.

---

## Using an LLM to write pyMetadataEditor code

You can ask an LLM like ChatGPT or Claude to write Python code that uses pyMetadataEditor. For best results, upload the [API Reference](../reference/api.md) to give the LLM the full method signatures and docstrings. For example:

> "Here is the API reference for pyMetadataEditor [paste reference]. Write code to retrieve all indicator projects from collection 17 and export each one to Excel."

The LLM will generate working code using the correct method names and parameters.
