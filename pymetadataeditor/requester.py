"""A module to handle HTTP requests with specific error handling for SSL and JSON decoding errors.

This module defines a class `RequestsWithSpecificErrors` that provides methods for making GET and POST requests
to a specified API URL. It includes error handling for SSL errors, HTTP errors, and JSON decoding errors, and
translates API responses into the package's custom exception hierarchy (see `MetadataEditorAPIError` and its
subclasses) so that end users see helpful, actionable error messages instead of raw HTTP tracebacks.
"""

from io import BufferedReader
from json import JSONDecodeError
from ssl import SSLError as ssl_SSLError
from typing import Any, Dict, List, Optional, Union

import requests
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, SecretStr, model_validator
from requests.exceptions import HTTPError, SSLError

__all__ = [
    "RequestsWithSpecificErrors",
    "MetadataEditorAPIError",
    "AuthenticationError",
    "ProjectAccessError",
    "ResourceNotFoundError",
    "BadRequestError",
    "ServerError",
]


class MetadataEditorAPIError(HTTPError):
    """Base class for all errors raised when the Metadata Editor API returns a non-success response.

    Inherits from `requests.exceptions.HTTPError`, so code that already catches `HTTPError` continues
    to work. Carries the API-provided message and the raw response for programmatic inspection.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        api_message: Optional[str] = None,
        url: Optional[str] = None,
        response: Optional[requests.Response] = None,
    ):
        """Initialize the error with a user-facing message and structured context."""
        super().__init__(message, response=response)
        self.status_code = status_code
        self.api_message = api_message
        self.url = url


class AuthenticationError(MetadataEditorAPIError):
    """Raised when the API rejects the supplied credentials (HTTP 401 or 403)."""


class ProjectAccessError(MetadataEditorAPIError):
    """Raised when the API accepts the credentials but denies access to a specific project or resource."""


class ResourceNotFoundError(MetadataEditorAPIError):
    """Raised when the requested project, template, collection, or endpoint does not exist (HTTP 404)."""


class BadRequestError(MetadataEditorAPIError):
    """Raised for other 4xx client errors that do not fall into a more specific category."""


class ServerError(MetadataEditorAPIError):
    """Raised when the Metadata Editor server returns a 5xx error."""


_ACCESS_DENIED_PATTERNS = (
    "don't have permission",
    "do not have permission",
    "permission to access",
    "access is denied",
    "access denied",
    "not authorized",
    "unauthorized",
    "forbidden",
)

_NOT_FOUND_PATTERNS = (
    "not found",
    "does not exist",
    "no such",
)


def _extract_api_message(response: requests.Response) -> Optional[str]:
    """Return the `message` field from a JSON error body, or None if not present/parseable."""
    try:
        body = response.json()
    except (ValueError, JSONDecodeError, requests.exceptions.JSONDecodeError):
        return None
    if isinstance(body, dict):
        msg = body.get("message")
        if isinstance(msg, str) and msg.strip():
            return msg.strip()
    return None


def _translate_http_error(
    response: Optional[requests.Response],
    url: str,
    api_url: str,
) -> MetadataEditorAPIError:
    """Map a failed `requests.Response` to the most specific `MetadataEditorAPIError` subclass.

    Falls back to a generic `MetadataEditorAPIError` with the raw API message if classification fails,
    so the caller always sees a readable message even when we cannot classify it precisely.
    """
    if response is None:
        return ResourceNotFoundError(
            f"Could not reach the Metadata Editor API at {api_url}. "
            "Check that the URL is correct and the server is reachable.",
            url=url,
        )

    status = response.status_code
    api_message = _extract_api_message(response)
    message_lower = (api_message or "").lower()

    def _kwargs():
        return {
            "status_code": status,
            "api_message": api_message,
            "url": url,
            "response": response,
        }

    if status == 404:
        if api_message:
            return ResourceNotFoundError(api_message, **_kwargs())
        return ResourceNotFoundError(
            f"Page not found at {url}. Check that the API URL is correct. "
            "Generally the required URL looks like "
            "'https://<name_of_your_metadata_database>.org/index.php/api', but "
            f"the URL that was passed was '{api_url}'.",
            **_kwargs(),
        )

    if status in (401, 403):
        default = (
            f"Access to {url} was denied by the Metadata Editor API. "
            "Check that the API key is correct and has the required permissions."
        )
        return AuthenticationError(api_message or default, **_kwargs())

    if 400 <= status < 500:
        if any(pattern in message_lower for pattern in _ACCESS_DENIED_PATTERNS):
            return ProjectAccessError(api_message, **_kwargs())
        if any(pattern in message_lower for pattern in _NOT_FOUND_PATTERNS):
            return ResourceNotFoundError(api_message, **_kwargs())
        if api_message:
            return BadRequestError(api_message, **_kwargs())
        return BadRequestError(
            f"The Metadata Editor API rejected the request to {url} (status {status}).",
            **_kwargs(),
        )

    if 500 <= status < 600:
        default = (
            f"The Metadata Editor server returned an error (status {status}) for {url}. "
            "This usually indicates a temporary problem on the server — try again shortly."
        )
        return ServerError(api_message or default, **_kwargs())

    return MetadataEditorAPIError(
        api_message or f"Unexpected response from the Metadata Editor API (status {status}) for {url}.",
        **_kwargs(),
    )


class RequestsWithSpecificErrors(BaseModel):
    """A class to handle HTTP requests with specific error handling for SSL and JSON decoding errors."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    api_url: AnyHttpUrl
    api_key: SecretStr = Field(repr=False)
    allow_http: bool = Field(
        default=False,
        description="API urls that begin HTTPS are favoured. Set allow_http=True to use of the less secure HTTP",
    )
    verify_ssl: bool = Field(
        default=True,
        description="Calls to the API are authenticated with an SSL certificate. "
        "Set verify_ssl=False to remove this requirement",
    )

    @model_validator(mode="after")
    def _check_https(self) -> Any:
        if str(self.api_url).startswith("https") or self.allow_http:
            return self
        else:
            raise ValueError(
                f"URL scheme should be 'https' but got {self.api_url}"
                "To allow the less secure use of 'http', set allow_http=True"
            )

    def _request(
        self,
        method: str,
        pth: str,
        json: Optional[Dict] = None,
        params: Optional[Dict[str, Union[str, List[str]]]] = None,
        id: Optional[Union[int, str]] = None,
        data: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, BufferedReader]] = None,
    ) -> Dict:
        """Perform a GET or POST request to the specified URL with the API key in the headers.

        Args:
            method (str): Either post or get
            pth (str): The path appended to the API_URL to which the GET or POST request is sent.
            json (optional dict): The JSON data to send with the POST request.
            params (optional dict): additional parameters to send with the get request such as 'keywords'
            id (optional int or str): The id of a specific collection or project.
                                        If not none, then pth should contain '{}' where the id ought to go.
            data (optional dict): The data to send with the POST request.
            files (optional dict): The files to send with the POST request.

        Returns:
            Dict[str, str]: The JSON response from the server, parsed into a dictionary.

        Raises:
            ValueError: If the URL does not start with 'https'.
            SSLError: If the server's SSL certificate cannot be verified.
            AuthenticationError: If the API key is rejected (HTTP 401/403).
            ProjectAccessError: If the API denies access to a specific project or resource.
            ResourceNotFoundError: If the requested project, template, or endpoint does not exist.
            BadRequestError: For other 4xx client errors.
            ServerError: For 5xx server errors.
            MetadataEditorAPIError: Base class for all of the above; catch this to handle any API error.
            JSONDecodeError: If the response body is not valid JSON.
        """
        method = method.lower()
        assert method in ["get", "post"], f"unknown method {method}"
        request_kwargs = {}
        if method == "post":
            assert params is None, "when using post, pass json not params"
            request_kwargs["json"] = json
            if data is not None:
                request_kwargs["data"] = data
            if files is not None:
                request_kwargs["files"] = files
        if method == "get" and params is not None:
            assert json is None, "when using get, pass params not json"
            request_kwargs["params"] = params

        if "{" in pth:
            assert id is not None, "If passing a url format, an id must be passed"
            pth = pth.format(id)
        url = str(self.api_url).strip("/") + "/" + pth.strip("/")
        try:
            response = None
            response = requests.request(
                method,
                url,
                verify=self.verify_ssl,
                headers={"x-api-key": self.api_key.get_secret_value()},
                **request_kwargs,
            )
            response.raise_for_status()
        except (SSLError, ssl_SSLError) as e:
            raise SSLError(
                f"Usually this means the admin of {self.api_url} has not verified an SSL certificate.\n"
                f"You can bypass the requirement by setting MetadataEditor.verify_ssl=False.\n{e}"
            ) from None
        except HTTPError:
            raise _translate_http_error(response, url=url, api_url=str(self.api_url)) from None
        try:
            json_response = response.json()
        except (JSONDecodeError, requests.exceptions.JSONDecodeError) as e:
            raise JSONDecodeError(
                f"Error decoding JSON response: {e.msg}\n{response.text}\nFull Response: {response}", e.doc, e.pos
            ) from e
        return json_response

    def get_request(
        self, pth: str, id: Optional[Union[int, str]] = None, params: Optional[Dict[str, Union[str, List[str]]]] = None
    ) -> Dict:
        """Performs a GET request to the specified URL with the API key in the headers and returns the JSON response.

        Args:
            pth (str): The path appended to the API_URL to which the GET request is sent.
            id (optional int or str): The id of a specific collection or project.
                                        If not none, then pth should contain '{}' where the id ought to go.
            params (optional dict): additional parameters to send with the get request such as 'keywords'

        Returns:
            Dict[str, str]: The JSON response from the server, parsed into a dictionary.
        """
        return self._request("get", pth=pth, id=id, params=params)

    def post_request(
        self,
        pth: str,
        json: Optional[Dict] = None,
        id: Optional[Union[int, str]] = None,
        data: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, BufferedReader]] = None,
    ):
        """Performs a POST request to the specified URL with the API key in the headers and returns the JSON response.

        Args:
            pth (str): The path appended to the API_URL to which the POST request is sent.
            json (optional dict): The JSON data to send with the POST request.
            id (optional int or str): The id of a specific project, collection or template etc.
                                        If not none, then pth should contain '{}' where the id ought to go.
            data (optional dict): The data to send with the POST request.
            files (optional dict): The files to send with the POST request.

        Returns:
            Dict[str, str]: The JSON response from the server, parsed into a dictionary.
        """
        return self._request("post", pth=pth, id=id, json=json, data=data, files=files)
