# Module: `interface.py`

**Location:** `pymetadataeditor/interface.py`

## Overview

The core module. Provides the `MetadataEditor` class which is the primary interface for all operations: managing projects, templates, collections, resources, metadata conversion, and LLM-powered metadata generation.

This is the only class users interact with directly.

**Exported via `__init__.py`:** `MetadataEditor`, `DeleteNotAppliedError`, `TemplateError`

---

## Custom Exceptions

### `DeleteNotAppliedError`

Raised when a delete request is sent to the API but the API did not confirm that the delete was applied.

```python
class DeleteNotAppliedError(Exception):
    def __init__(self, message="Delete request not accepted by system.", response=None)
```

### `TemplateError`

Raised when there is an error related to a template (e.g., template UID not found, template incompatibility).

```python
class TemplateError(Exception):
    def __init__(self, message="Error with template", response=None)
```

---

## Class: `MetadataEditor`

```python
class MetadataEditor:
    def __init__(
        self,
        api_url: str,
        api_key: str,
        allow_http: bool = False,
        verify_ssl: bool = True,
    )
```

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_url` | `str` | required | API endpoint, e.g. `"https://mydb.org/index.php/api"` |
| `api_key` | `str` | required | API key created via the Metadata Editor web interface |
| `allow_http` | `bool` | `False` | Allow HTTP (non-HTTPS) URLs; not recommended for production |
| `verify_ssl` | `bool` | `True` | Verify SSL certificates; set to `False` for self-signed certs |

### Quick Start

```python
from pymetadataeditor import MetadataEditor
import os

me = MetadataEditor(
    api_url=os.getenv("METADATA_API_URL"),
    api_key=os.getenv("METADATA_API_KEY"),
)
```

---

## Method Reference

### Project Management

#### `count_projects() -> int`

Returns the total number of projects accessible with the current API key.

---

#### `list_projects(limit, keywords, metadata_type, offset, sort_by) -> pd.DataFrame`

```python
def list_projects(
    self,
    limit: Union[int, str],                          # int or "All"
    keywords: Optional[Union[str, List[str]]] = None,
    metadata_type: Optional[str] = None,
    offset: int = 0,
    sort_by: Optional[str] = None,                   # "title_asc", "title_desc", "updated_asc", "updated_desc"
) -> pd.DataFrame
```

Returns a DataFrame of projects. Use `limit="All"` to retrieve every project (paginates internally in batches of 500).

---

#### `get_project_by_id(id) -> pd.Series`

```python
def get_project_by_id(self, id: int) -> pd.Series
```

Returns a Series with project metadata (type, idno, title, template_uid, etc.) for a single project.

---

#### `create_project_log(metadata, metadata_type_or_template_uid) -> int`

```python
def create_project_log(
    self,
    metadata: Union[BaseModel, Dict, str],           # dict, Pydantic model, or path to Excel file
    metadata_type_or_template_uid: Optional[str] = None,
) -> int
```

Creates a new project and returns its integer ID. The `metadata_type_or_template_uid` is required when passing a dict; otherwise the type is inferred from the Pydantic model or Excel file.

Supported type names: `document`, `geospatial`, `image`, `indicator`, `indicators_db`, `microdata`, `resource`, `script`, `table`, `video`

```python
project_id = me.create_project_log(
    {"idno": "MY_INDICATOR_001", "series_description": {"name": "GDP per capita"}},
    "indicator"
)
```

---

#### `update_project_log_by_id(id, new_metadata)`

```python
def update_project_log_by_id(
    self,
    id: int,
    new_metadata: Union[BaseModel, Dict, str],
)
```

Replaces the metadata for an existing project. The metadata type and template UID must match the existing project. Partial dicts are allowed — only the specified fields are updated.

---

#### `patch_update_project_log_by_id(id, op, path, value)`

```python
def patch_update_project_log_by_id(
    self,
    id: int,
    op: str,                         # "add", "remove", "replace", "test"
    path: str,                       # JSON Pointer, e.g. "/series_description/name"
    value: Optional[str] = None,     # Not needed for "remove"
)
```

Applies a single [JSON Patch](https://jsonpatch.com/) (RFC 6902) operation to a project's metadata. Useful for making targeted changes without fetching and re-uploading the full metadata.

```python
me.patch_update_project_log_by_id(id=123, op="replace", path="/series_description/name", value="New Name")
me.patch_update_project_log_by_id(id=123, op="remove", path="/series_description/definition_short")
```

---

#### `delete_project_by_id(id)`

```python
def delete_project_by_id(self, id: int)
```

Deletes a project. Raises `DeleteNotAppliedError` if the API does not confirm deletion.

---

### Metadata Retrieval & Conversion

#### `get_metadata_class(metadata_type_or_template_uid) -> Type[BaseModel]`

```python
def get_metadata_class(self, metadata_type_or_template_uid: str) -> Type[BaseModel]
```

Returns the Pydantic model class for a given metadata type or template UID. Useful for introspecting the schema programmatically.

---

#### `make_metadata_outline(metadata_type_or_template_uid, output_mode, filename, title)`

```python
def make_metadata_outline(
    self,
    metadata_type_or_template_uid: str,
    output_mode: str,                   # "dict", "pydantic", or "excel"
    filename: Optional[str] = None,     # Used when output_mode="excel"
    title: Optional[str] = None,        # Used when output_mode="excel"
) -> Union[Dict, BaseModel, Path]
```

Creates a skeleton outline of a metadata type with all fields initialized to their default values (typically `None`). Useful as a starting point for filling in metadata.

```python
# As a dict
outline_dict = me.make_metadata_outline("indicator", "dict")

# As a Pydantic model (supports dot-notation access)
outline = me.make_metadata_outline("indicator", "pydantic")
outline.series_description.name = "GDP per capita"

# As an Excel file
path = me.make_metadata_outline("indicator", "excel", "indicator_outline.xlsx")
```

---

#### `get_project_metadata_by_id(id, output_mode, template_uid, simplify, filename, title, debug)`

```python
def get_project_metadata_by_id(
    self,
    id: int,
    output_mode: str,                    # "dict", "pydantic", or "excel"
    template_uid: Optional[str] = None,  # Override the template; "default" uses the type default; "none" removes template (dict only)
    simplify: bool = True,               # If True (dict mode), only non-null/non-empty fields are returned
    filename: Optional[str] = None,
    title: Optional[str] = None,
    debug: bool = False,
) -> Union[BaseModel, Dict, str]
```

Downloads and returns the metadata for an existing project.

```python
metadata = me.get_project_metadata_by_id(123, "pydantic")
metadata_dict = me.get_project_metadata_by_id(123, "dict")
excel_path = me.get_project_metadata_by_id(123, "excel", filename="project_123.xlsx")
```

---

#### `save_metadata_to_excel(metadata_model, metadata_type_or_template_uid, filename, title) -> str`

```python
def save_metadata_to_excel(
    self,
    metadata_model: BaseModel | dict | str,
    metadata_type_or_template_uid: Optional[str] = None,
    filename: Optional[str] = None,
    title: Optional[str] = None,
) -> str
```

Exports a metadata object (Pydantic model, dict, or path to an existing Excel file) to an Excel file. Returns the filename. When passing a dict, `metadata_type_or_template_uid` is required to identify the schema.

---

#### `read_metadata_from_excel(filename, output_mode, exclude_unset) -> Union[BaseModel, Dict]`

```python
def read_metadata_from_excel(
    self,
    filename: str,
    output_mode: str = "pydantic",
    exclude_unset: bool = True,
) -> Union[BaseModel, Dict]
```

Reads metadata from an Excel file (previously created by `save_metadata_to_excel` or `make_metadata_outline`). Returns a Pydantic model by default; pass `output_mode="dict"` for a dictionary. When `output_mode="dict"`, `exclude_unset=True` omits fields with null or empty values.

---

### Automated Metadata (LLM)

#### `draft_metadata_from_files(...) -> Union[BaseModel, Dict, str]`

```python
def draft_metadata_from_files(
    self,
    llm_api_key: str,
    files: Union[List[str], str],               # File paths or URLs
    output_mode: str,                            # "dict", "pydantic", or "excel"
    metadata_type_or_template_uid: str,
    metadata_producer_organization: Optional[str] = None,
    filename: Optional[str] = None,
    title: Optional[str] = None,
    llm_model_name: str = "gpt-4o",
    tokenizer_model: str = "o200k_base",
    max_tokens: int = 128_000,
    llm_base_url: Optional[str] = None,          # For Azure OpenAI or local models
    azure_deployment_name: Optional[str] = None,
) -> Union[BaseModel, Dict, str]
```

Automatically generates a first draft of metadata from one or more source files or URLs, using an LLM. Files are converted to Markdown text using `markitdown`, then sent to the LLM for structured metadata extraction.

**Supported file types:** PDF, Word, Excel, PowerPoint, text, CSV, XML, ZIP, images, audio, HTML/URLs

```python
# Using OpenAI
metadata = me.draft_metadata_from_files(
    llm_api_key="sk-...",
    files=["report.pdf", "supplementary.docx"],
    output_mode="pydantic",
    metadata_type_or_template_uid="microdata",
    metadata_producer_organization="My Organization",
)

# Using a local Ollama model
metadata = me.draft_metadata_from_files(
    llm_api_key="ollama",
    files=["report.pdf"],
    output_mode="pydantic",
    metadata_type_or_template_uid="indicator",
    llm_base_url="http://localhost:11434/v1/",
    llm_model_name="llama3.1",
)

# Using Azure OpenAI
metadata = me.draft_metadata_from_files(
    llm_api_key="...",
    files=["report.pdf"],
    output_mode="pydantic",
    metadata_type_or_template_uid="indicator",
    llm_base_url="https://my-resource.openai.azure.com/",
    azure_deployment_name="my-deployment",
)
```

---

#### `augment_metadata_from_files(input_metadata, llm_api_key, files, output_mode, ...) -> Union[BaseModel, Dict, str]`

```python
def augment_metadata_from_files(
    self,
    input_metadata: Union[BaseModel, Dict, str],    # Existing metadata to augment
    llm_api_key: str,
    files: Union[List[str], str],
    output_mode: str,
    metadata_type_or_template_uid: Optional[str] = None,
    metadata_producer_organization: Optional[str] = None,
    prefix: Optional[str] = None,                  # e.g. "<AI>" to mark LLM-added fields
    filename: Optional[str] = None,
    title: Optional[str] = None,
    llm_model_name: str = "gpt-4o",
    tokenizer_model: str = "o200k_base",
    max_tokens: int = 128_000,
    llm_base_url: Optional[str] = None,
    azure_deployment_name: Optional[str] = None,
) -> Union[BaseModel, Dict, str]
```

Like `draft_metadata_from_files`, but starts from existing metadata and uses the LLM to fill in empty fields or enhance existing content. The `prefix` parameter marks which fields were added by the LLM.

```python
augmented = me.augment_metadata_from_files(
    input_metadata=existing_metadata,
    llm_api_key="sk-...",
    files=["new_report.pdf"],
    output_mode="pydantic",
    prefix="<AI> ",
)
```

---

### Templates

#### `list_templates() -> pd.DataFrame`

Returns a DataFrame of all available templates (both standard and custom), including columns `uid`, `template_type`, `name`.

---

#### `get_template_by_uid(uid) -> pd.Series`

```python
def get_template_by_uid(self, uid: str) -> pd.Series
```

Returns a Series with the details of a specific template identified by its UID.

---

#### `change_mode_or_template(metadata, output_mode, ...) -> Union[BaseModel, Dict, str]`

```python
def change_mode_or_template(
    self,
    metadata: Union[BaseModel, Dict, str],
    output_mode: str,
    output_template_uid: Optional[str] = None,
    input_template_uid: Optional[str] = None,
    filename: Optional[str] = None,
    title: Optional[str] = None,
    simplify: Optional[bool] = None,
) -> Union[BaseModel, Dict, str]
```

Converts a metadata object between output modes (`"pydantic"`, `"dict"`, `"excel"`) and/or between templates. `output_template_uid` specifies the target template; if omitted the existing template is preserved. `input_template_uid` is required when `metadata` is a raw dictionary. `filename` and `title` apply when `output_mode="excel"`.

---

#### `delete_template(uid)`

```python
def delete_template(self, uid: str)
```

Deletes a custom template. Standard templates cannot be deleted.

---

### Collections

#### `list_collections() -> pd.DataFrame`

Returns a DataFrame of all collections.

---

#### `get_collection_by_id(id) -> pd.Series`

```python
def get_collection_by_id(self, id: int) -> pd.Series
```

Returns details of a single collection.

---

#### `create_collection(title, description) -> int`

```python
def create_collection(self, title: str, description: str) -> int
```

Creates a new collection and returns its integer ID.

---

#### `update_collection(id, title, description)`

```python
def update_collection(
    self,
    id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
)
```

Updates the title and/or description of an existing collection.

---

#### `copy_collection(source_id, target_id)`

```python
def copy_collection(self, source_id: int, target_id: int)
```

Copies all projects from `source_id` collection into `target_id` collection (non-destructive).

---

#### `move_collection(source_id, target_id)`

```python
def move_collection(self, source_id: int, target_id: int)
```

Moves all projects from `source_id` to `target_id` (removes from source).

---

#### `count_projects_in_collection(collection) -> int`

```python
def count_projects_in_collection(self, collection: int) -> int
```

Returns the number of projects in a collection.

---

#### `list_projects_in_collection(collection, limit, offset, keywords, sort_by) -> pd.DataFrame`

```python
def list_projects_in_collection(
    self,
    collection: int,
    limit: Union[int, str] = "All",
    offset: int = 0,
    keywords: Optional[Union[str, List[str]]] = None,
    sort_by: Optional[str] = None,
) -> pd.DataFrame
```

Returns a DataFrame of projects in a collection. Use `limit="All"` for all projects.

---

#### `add_projects_to_collection(collection, id_format, projects)`

```python
def add_projects_to_collection(
    self,
    collection: int,
    id_format: str,        # "id" (integer IDs) or "idno" (string identifiers)
    projects: List,
)
```

Adds a list of projects to a collection.

---

#### `remove_projects_from_collection(collection, id_format, projects)`

```python
def remove_projects_from_collection(
    self,
    collection: int,
    id_format: str,
    projects: List,
)
```

Removes a list of projects from a collection.

---

#### `set_template_for_collection(collection_id, template_uid)`

```python
def set_template_for_collection(self, collection_id: int, template_uid: str)
```

Assigns a template to all projects in a collection.

---

#### `delete_collection_by_id(id)`

```python
def delete_collection_by_id(self, id: int)
```

Deletes the collection with the given `id` and verifies deletion. Raises `DeleteNotAppliedError` if the system blocks the deletion (e.g. due to admin restrictions).

---

### Resources (File Attachments)

#### `get_resources_by_id(id) -> pd.DataFrame`

```python
def get_resources_by_id(self, id: int) -> pd.DataFrame
```

Returns a DataFrame listing all file resources attached to a project.

---

#### `log_resource(project_id, filename, file_data)`

```python
def log_resource(
    self,
    project_id: int,
    filename: str,
    file_data: BufferedReader,   # Open file object, e.g. open("file.pdf", "rb")
)
```

Uploads a file as a resource attached to a project.

---

#### `update_resource(project_id, resource_id, new_data)`

```python
def update_resource(
    self,
    project_id: int,
    resource_id: int,
    new_data: dict,
)
```

Updates the metadata (not file content) of an existing resource.

---

#### `delete_resource_by_id(project_id, resource_id)`

```python
def delete_resource_by_id(self, project_id: int, resource_id: int)
```

Deletes a resource from a project. Raises `DeleteNotAppliedError` if the delete was not confirmed.

---

### Generic / Low-Level

#### `generic_api_request(method, endpoint, params, data, json, files) -> Dict`

```python
def generic_api_request(
    self,
    method: str,                                        # "GET" or "POST"
    endpoint: str,                                      # API path
    params: Optional[Dict] = None,
    data: Optional[Dict] = None,
    json: Optional[Dict] = None,
    files: Optional[Dict[str, BufferedReader]] = None,
) -> Dict
```

Low-level access to the API for operations not covered by other methods. Prefer using the specific methods when available.

---

## Internal Helper Methods

These are private (prefixed with `_`) and not part of the public API:

| Method | Purpose |
|--------|---------|
| `_process_metadata_input(metadata, type)` | Converts dict/Excel/Pydantic to a validated Pydantic model |
| `_process_metadata_output(obj, mode, ...)` | Converts a Pydantic model to dict/Excel/Pydantic based on `output_mode` |
| `_get_metadata_class_and_type_and_UID(type_or_uid, apply_rules)` | Resolves a type string or UID to a Pydantic class |
| `_get_template_class_and_type_and_UID(uid, apply_rules)` | Resolves a template UID to a Pydantic class via `pydantic_from_template()` |

---

## Output Mode Reference

All methods that return metadata accept an `output_mode` parameter:

| Mode strings | Return type | Notes |
|---|---|---|
| `"dict"`, `"dictionary"` | `Dict` | Plain Python dict; `simplify=True` removes empty/null values |
| `"pydantic"`, `"model"`, `"basemodel"`, `"object"` | `BaseModel` | Dot-notation access, `pretty_print()` available |
| `"excel"` | `str` (file path) | Saves to file and returns the path |

---

## Supported Metadata Types

| Type name | API alias | Description |
|-----------|-----------|-------------|
| `microdata` | `survey` | Household surveys, census data |
| `indicator` | `timeseries` | Time series / indicator data |
| `indicators_db` | `timeseries_db` | Database of indicators |
| `geospatial` | `geospatial` | Geospatial datasets |
| `document` | `document` | Reports, papers, documents |
| `script` | `script` | Data processing scripts |
| `image` | `image` | Images and photos |
| `video` | `video` | Video files |
| `resource` | `resource` | Generic resources |
| `table` | `table` | Tabular data |
