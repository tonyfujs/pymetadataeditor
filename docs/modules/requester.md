# Module: `requester.py`

**Location:** `pymetadataeditor/requester.py`

## Overview

This module provides the HTTP communication layer for the package. It wraps the `requests` library with API key authentication, SSL/HTTPS enforcement, and specific error handling for SSL errors, HTTP errors, and JSON decoding failures.

The class is a Pydantic `BaseModel` itself, which means its fields are validated on construction.

---

## Class: `RequestsWithSpecificErrors`

```python
class RequestsWithSpecificErrors(BaseModel):
```

A Pydantic model that handles authenticated HTTP GET and POST requests to the Metadata Editor API, with structured error handling.

**Instantiated internally by `MetadataEditor.__init__()`** — users do not create this directly.

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `api_url` | `AnyHttpUrl` | required | The base API URL (validated as a proper HTTP/HTTPS URL) |
| `api_key` | `SecretStr` | required | The API key, stored securely and never shown in repr |
| `allow_http` | `bool` | `False` | Allow HTTP (non-HTTPS) URLs; HTTPS is enforced by default |
| `verify_ssl` | `bool` | `True` | Verify SSL certificates; set to `False` for self-signed certs |

### Model Validator

A `@model_validator(mode="after")` named `_check_https` runs after construction. It raises `ValueError` if the URL starts with `http://` and `allow_http=False`.

---

## Methods

### `_request(method, pth, json, params, id, data, files) -> Dict`

The core internal request method. Builds the full URL, attaches the API key header, and dispatches a GET or POST request.

```python
def _request(
    self,
    method: str,                                        # "get" or "post"
    pth: str,                                           # API path, e.g. "/editor"
    json: Optional[Dict] = None,                        # POST body as JSON
    params: Optional[Dict[str, Union[str, List[str]]]] = None,  # GET query params
    id: Optional[Union[int, str]] = None,               # Interpolated into pth if pth contains "{}"
    data: Optional[Dict[str, str]] = None,              # POST form data
    files: Optional[Dict[str, BufferedReader]] = None,  # POST file uploads
) -> Dict
```

URL construction: `str(api_url).strip("/") + "/" + pth.strip("/")`

If `pth` contains `{}`, the `id` is interpolated via `pth.format(id)`.

The API key is passed via the `x-api-key` header.

---

### `get_request(pth, id, params) -> Dict`

```python
def get_request(
    self,
    pth: str,
    id: Optional[Union[int, str]] = None,
    params: Optional[Dict[str, Union[str, List[str]]]] = None,
) -> Dict
```

Convenience wrapper around `_request("get", ...)`. Pass query parameters via `params`, not `json`.

---

### `post_request(pth, json, id, data, files) -> Dict`

```python
def post_request(
    self,
    pth: str,
    json: Optional[Dict] = None,
    id: Optional[Union[int, str]] = None,
    data: Optional[Dict[str, str]] = None,
    files: Optional[Dict[str, BufferedReader]] = None,
)
```

Convenience wrapper around `_request("post", ...)`. Pass the request body via `json`, not `params`.

---

## Error Handling

| HTTP Scenario | Exception Raised |
|--------------|-----------------|
| SSL certificate error | `requests.exceptions.SSLError` with a helpful message suggesting `verify_ssl=False` |
| 404 Not Found | `requests.exceptions.HTTPError` with a message suggesting to check the URL format |
| 403 Forbidden | `PermissionError` suggesting the API key may be incorrect |
| Other HTTP errors | `requests.exceptions.HTTPError` with status code and response body |
| Invalid JSON response | `json.JSONDecodeError` with the raw response text |

---

## Security Features

- **API key protection**: Stored as Pydantic `SecretStr` — never appears in logs, repr, or error messages.
- **HTTPS enforcement**: The URL must start with `https://` unless `allow_http=True` is explicitly set.
- **SSL verification**: Certificate validation is on by default. Use `verify_ssl=False` only for development or trusted private systems.

---

## Configuration Notes

```python
# Standard secure usage
me = MetadataEditor(api_url="https://mydb.org/index.php/api", api_key="...")

# Self-signed SSL certificate (development)
me = MetadataEditor(..., verify_ssl=False)

# HTTP endpoint (not recommended for production)
me = MetadataEditor(..., allow_http=True)
```

The expected API URL format is: `https://<name_of_your_metadata_database>.org/index.php/api`
