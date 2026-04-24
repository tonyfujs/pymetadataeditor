# pyMetadataEditor

**pyMetadataEditor** is a Python client library for the [Metadata Editor](https://github.com/mah0001/metadata-editor) REST API. It lets data curators create, retrieve, update, and manage structured metadata for research datasets — directly from Python.

## Supported metadata types

| Type | Description |
|------|-------------|
| `microdata` | Household surveys, censuses, and other microdata studies |
| `indicator` | Time series indicators (e.g. GDP, poverty rates) |
| `indicators_db` | Databases of indicators |
| `geospatial` | Geographic and spatial datasets |
| `document` | Reports, publications, and documents |
| `script` | Data processing and analysis scripts |
| `image` | Images and photographs |
| `video` | Videos and multimedia |
| `table` | Statistical tables |
| `resource` | General resources |

## Key capabilities

- **Browse & search** projects and collections
- **Create, retrieve, and update** metadata in Python dict, Pydantic model, or Excel format
- **Generate metadata automatically** from PDFs, Word docs, web pages, and more using an LLM (OpenAI, Azure, or a local Ollama model)
- **Manage collections** — create, organize, move, and copy projects between collections
- **Attach resources** — link supporting documents, questionnaires, and tables to projects

## Quick start

```python
from pymetadataeditor import MetadataEditor
import os

# Connect to your Metadata Editor instance
me = MetadataEditor(
    api_url=os.getenv("METADATA_API_URL"),
    api_key=os.getenv("METADATA_API_KEY"),
)

# Verify the connection and list your projects
print(me.count_projects())
me.list_projects(limit=10)
```

See the [Getting Started guide](getting_started.md) for a full walkthrough.

## Installation

```bash
pip install pymetadataeditor
```

Or with Poetry:

```bash
poetry add pymetadataeditor
```

**Requires Python 3.11 or later.**

## Navigation

| Section | What you'll find |
|---------|-----------------|
| [Getting Started](getting_started.md) | Installation, connection, and a complete first workflow |
| [User Guide](user_guide/01_browsing_projects.md) | In-depth guides for every functional area |
| [How-To Guides](how_to/move_projects_between_collections.md) | Practical recipes for common multi-step tasks |
| [API Reference](reference/api.md) | Full method signatures and parameter docs |
| [Reference](reference/output_modes.md) | Output modes, metadata types, error handling |
| [AI & LLMs](ai_and_llms.md) | Agent skill, `llms.txt`, and `llms-full.txt` for AI assistants |
