# pyMetadataEditor — Agent Skill Reference

This document gives an AI agent everything needed to understand and work with the `pymetadataeditor` Python package. For deep details on each module, see the [Module Reference](#module-reference) section.

---

## Package Overview

`pymetadataeditor` (v0.3.2) is a Python client library for managing metadata in a [Metadata Editor](https://github.com/mah0001/metadata-editor) database via its REST API.

It supports:
- Creating, reading, updating, and deleting metadata projects
- Managing collections (groups of projects) and file resources
- Converting metadata between Python dicts, Pydantic models, and Excel spreadsheets
- Automatically generating metadata from source documents using an LLM (OpenAI GPT-4o or compatible)
- Working with customizable metadata templates

**Target users:** Data managers, researchers, and developers who need to programmatically manage structured metadata for datasets.

---

## Installation

```bash
pip install poetry
poetry install
```

For development (tests, linting):
```bash
poetry install --with dev
poetry run pre-commit install
```

---

## Quick Start

```python
from pymetadataeditor import MetadataEditor
import os

me = MetadataEditor(
    api_url=os.getenv("METADATA_API_URL"),  # e.g. "https://mydb.org/index.php/api"
    api_key=os.getenv("METADATA_API_KEY"),
)

# List projects
df = me.list_projects(limit=10)

# Create a metadata skeleton and populate it
outline = me.make_metadata_outline("indicator", "pydantic")
outline.series_description.name = "GDP per capita"
outline.series_description.idno = "GDP_PC_001"

# Upload to the database
project_id = me.create_project_log(outline)

# Download existing project metadata
metadata = me.get_project_metadata_by_id(project_id, "pydantic")
```

---

## Architecture

```
User Code
    │
    ▼
MetadataEditor          (pymetadataeditor/interface.py)
    ├──► RequestsWithSpecificErrors  (requester.py)  ──► Metadata Editor API
    ├──► pydantic_from_template      (templates.py)  ◄── templates from API
    ├──► llm_helpers functions       (llm_helpers.py) ──► OpenAI / LLM API
    └──► utils functions             (utils.py)
              │
              ▼
    Returns: Dict | Pydantic Model | Excel file path
              │
              ▼
    metadataschemas library (external dependency — provides base Pydantic schemas)
```

The `MetadataEditor` class is the single entry point for all operations. It delegates HTTP communication to `RequestsWithSpecificErrors`, template-to-Pydantic conversion to `templates.py`, LLM operations to `llm_helpers.py`, and uses `utils.py` for shared helpers.

---

## Key Capabilities

### Project Management
- **List projects** — paginated, filterable by keyword, type, sort order
- **Get project** — retrieve a single project's summary as a pandas Series
- **Create project** — upload metadata (dict, Pydantic, or Excel) and receive an integer project ID
- **Update project** — replace all metadata for an existing project
- **Patch update** — apply a single JSON Patch (RFC 6902) operation to partially modify metadata
- **Delete project** — remove a project from the database

### Metadata Conversion
- **Make outline** — generate a skeleton with all fields initialized to `None` (dict, Pydantic, or Excel)
- **Get project metadata** — download existing metadata in any output format
- **Save to Excel** — export any metadata object to a formatted Excel file
- **Read from Excel** — import metadata from a previously exported Excel file

### Automated Metadata (LLM)
- **Draft from files** — generate a complete first-draft metadata record from one or more source files using an LLM
- **Augment from files** — use LLM to fill in empty fields in existing metadata, optionally marking LLM-added content with a prefix

### Templates
- **List templates** — view all standard and custom templates available in the database
- **Get template** — retrieve a specific template by UID
- **Change template** — reassign a different template to an existing project
- **Delete template** — remove a custom template

### User Management
- **List users** — retrieve a DataFrame of all registered users (id, email, username)
- **Find user by email** — look up a user's integer ID by email address or username

### Collections
- **List / get collections** — browse available project collections
- **Create / update collections** — manage collection metadata
- **Copy / move collections** — bulk-move or copy projects between collections
- **Add / remove projects** — manage collection membership
- **Set template for collection** — apply a template to all projects in a collection

### Collection Permissions
- **List project access** — view which users have project access in a collection
- **Assign project access** — grant a user project-level access to a collection
- **Remove project access** — revoke a user's project-level access from a collection
- **List ACL** — view which users have ACL (administrative) access to a collection
- **Check ACL** — verify whether a specific user has ACL access to a collection
- **Assign ACL** — grant a user ACL access to a collection
- **Update ACL** — modify an existing user's ACL permissions on a collection
- **Remove ACL** — revoke a user's ACL access from a collection
- **Get collection permissions** — retrieve the authenticated user's permission summary across all collections

### Resources (File Attachments)
- **Get resources** — list files attached to a project
- **Upload resource** — attach a file to a project
- **Update resource** — update resource metadata
- **Delete resource** — remove a file attachment

### Admin Metadata
- **List admin metadata templates** — discover available administrative metadata template UIDs
- **Get admin metadata template** — retrieve a single admin template by UID
- **List admin metadata** — query admin metadata records, filterable by project, template, date range
- **Get admin metadata** — retrieve a single admin metadata record by (project_id, template_uid)
- **Upsert admin metadata** — create or update an admin metadata record (dict only in this version)
- **Patch admin metadata** — apply multi-op JSON Patch (RFC 6902) to an admin metadata record
- **Delete admin metadata** — remove an admin metadata record

### Low-Level Access
- **Generic API request** — direct GET/POST to the API for edge cases not covered by other methods

---

## Supported Metadata Types

| User-facing name | API alias | Description |
|-----------------|-----------|-------------|
| `microdata` | `survey` | Household surveys, census |
| `indicator` | `timeseries` | Time series / indicator data |
| `indicators_db` | `timeseries_db` | Database of indicators |
| `geospatial` | `geospatial` | Spatial datasets |
| `document` | `document` | Reports, papers |
| `script` | `script` | Data processing code |
| `image` | `image` | Photos and images |
| `video` | `video` | Video files |
| `resource` | `resource` | Generic resources |
| `table` | `table` | Tabular data |

---

## Output Formats

All methods that return metadata support three `output_mode` values:

| `output_mode` | Return type | Notes |
|--------------|-------------|-------|
| `"dict"` | `dict` | Plain Python dict; `simplify=True` (default) removes empty/null values |
| `"pydantic"` | `BaseModel` | Dot-notation field access, `pretty_print()` method available |
| `"excel"` | `str` (file path) | Saves to `.xlsx` and returns the file path |

Aliases: `"dictionary"` = `"dict"`, `"model"` / `"basemodel"` / `"object"` = `"pydantic"`.

---

## Module Reference

| Module | File | Purpose |
|--------|------|---------|
| [interface.md](modules/interface.md) | `pymetadataeditor/interface.py` | `MetadataEditor` class — all public operations |
| [requester.md](modules/requester.md) | `pymetadataeditor/requester.py` | HTTP layer — authenticated GET/POST, error handling, SSL |
| [templates.md](modules/templates.md) | `pymetadataeditor/templates.py` | Converts API template dicts into Pydantic model classes |
| [llm_helpers.md](modules/llm_helpers.md) | `pymetadataeditor/llm_helpers.py` | LLM integration — field-by-field querying, validation, file conversion |
| [utils.md](modules/utils.md) | `pymetadataeditor/utils.py` | Shared utilities — JSON patch validation, empty-value cleaning, constraint stripping |

---

## Common Workflows

### 1. Create a new indicator project

```python
me = MetadataEditor(api_url=..., api_key=...)

# Start with a skeleton outline
metadata = me.make_metadata_outline("indicator", "pydantic")

# Fill in required fields
metadata.series_description.idno = "MY_INDICATOR_001"
metadata.series_description.name = "Poverty headcount ratio"
metadata.series_description.definition_long = "Percentage of population below poverty line."

# Upload to the database
project_id = me.create_project_log(metadata)
print(f"Created project ID: {project_id}")
```

---

### 2. Auto-generate metadata from source documents

```python
import os

metadata = me.draft_metadata_from_files(
    llm_api_key=os.getenv("OPENAI_API_KEY"),
    files=["survey_report.pdf", "technical_manual.docx"],
    output_mode="pydantic",
    metadata_type_or_template_uid="microdata",
    metadata_producer_organization="The World Bank Group",
)
metadata.pretty_print()

# Save to database
project_id = me.create_project_log(metadata)
```

---

### 3. Batch upload from a custom Excel spreadsheet

```python
import pandas as pd

df = pd.read_excel("indicators_list.xlsx")

for _, row in df.iterrows():
    metadata = me.make_metadata_outline("indicator", "pydantic")
    metadata.series_description.idno = row["idno"]
    metadata.series_description.name = row["name"]
    metadata.series_description.definition_long = row["definition_long"]
    me.create_project_log(metadata)
```

---

### 4. Move projects between collections

```python
# Create target collection
new_collection_id = me.create_collection("New Collection", "Migrated from old collection")

# Get projects from source collection
projects_df = me.list_projects_in_collection(collection=17, limit="All")

# Filter and move
indicator_ids = projects_df[projects_df["type"] == "indicator"]["id"].tolist()
me.add_projects_to_collection(collection=new_collection_id, id_format="id", projects=indicator_ids)
me.remove_projects_from_collection(collection=17, id_format="id", projects=indicator_ids)
```

---

### 5. Migrate projects between MetadataEditor instances

```python
# Connect to both instances
me_dev = MetadataEditor(api_url=dev_url, api_key=dev_key)
me_prod = MetadataEditor(api_url=prod_url, api_key=prod_key)

# Copy all projects from a dev collection to prod
projects = me_dev.list_projects_in_collection(collection=1, limit="All")
for _, row in projects.iterrows():
    metadata = me_dev.get_project_metadata_by_id(row["id"], "dict")
    me_prod.create_project_log(metadata, row["type"])
```

---

### 6. Partially update metadata with JSON Patch

```python
# Update a single field without re-uploading everything
me.patch_update_project_log_by_id(
    id=123,
    op="replace",
    path="/series_description/name",
    value="Updated Indicator Name"
)

# Remove a field
me.patch_update_project_log_by_id(id=123, op="remove", path="/series_description/definition_short")
```

---

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
```

---

## Existing Documentation

| Document | Description |
|----------|-------------|
| [README.md](../README.md) | Installation, basic usage examples |
| [docs/API_Reference.md](API_Reference.md) | Auto-generated full API reference from docstrings |
| [docs/examples.md](examples.md) | Practical worked examples (batch upload, migration, collection management) |
| [docs/using_automated_metadata_creation.md](using_automated_metadata_creation.md) | Detailed guide to LLM-powered metadata generation |
| [docs/demo.md](demo.md) | End-to-end demonstration workflow |

---

## Notes for LLM Code Generation

When an LLM (e.g., ChatGPT) is being asked to write `pymetadataeditor` code, providing `docs/API_Reference.md` as context alongside this skill file gives it full method signatures and docstrings. The examples in `docs/examples.md` also serve as good few-shot examples.

Key things to get right:
- Always instantiate `MetadataEditor` first with `api_url` and `api_key`
- `create_project_log()` returns an `int` (the project ID)
- `list_projects()` and `list_projects_in_collection()` return `pd.DataFrame`
- `make_metadata_outline()` with `"pydantic"` mode returns a live Pydantic object that can be modified with dot notation before uploading
- Template UIDs are strings (e.g., `"IHSN_INDICATOR_1-0_Template_v01_EN"`), not integers
- `metadata_type_or_template_uid` accepts either a type name (e.g., `"indicator"`) or a template UID
