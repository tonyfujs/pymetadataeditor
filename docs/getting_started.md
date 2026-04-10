# Getting Started

This guide walks you through a complete, typical workflow: installing the library, connecting to your Metadata Editor instance, browsing what's there, retrieving a record, exploring its schema, and saving a change back.

---

## Prerequisites

- Python 3.11 or later
- An API key for your Metadata Editor instance (created via the web interface under your account settings)
- The URL of your Metadata Editor API, which typically looks like:
  `https://<your-instance>.org/index.php/api`

---

## Installation

```bash
pip install pymetadataeditor
```

Or with Poetry:

```bash
poetry add pymetadataeditor
```

---

## Storing your credentials

Never hard-code your API key in scripts. Store it in a `.env` file at the root of your project:

```
METADATA_API_URL=https://<your-instance>.org/index.php/api
METADATA_API_KEY=your_api_key_here
```

Then load it in Python with `python-dotenv` or the built-in `os` module:

```python
import os
# If using python-dotenv:
# from dotenv import load_dotenv; load_dotenv()

api_url = os.getenv("METADATA_API_URL")
api_key = os.getenv("METADATA_API_KEY")
```

---

## Step 1 — Connect to your instance

Import `MetadataEditor` and create a connection:

```python
from pymetadataeditor import MetadataEditor
import os

me = MetadataEditor(
    api_url=os.getenv("METADATA_API_URL"),
    api_key=os.getenv("METADATA_API_KEY"),
)
```

### Connection options

| Parameter | Default | When to change |
|-----------|---------|---------------|
| `verify_ssl` | `True` | Set to `False` if your instance uses a self-signed SSL certificate |
| `allow_http` | `False` | Set to `True` only for local development instances using plain HTTP |

```python
# Example for a development instance with a self-signed cert
me = MetadataEditor(
    api_url=os.getenv("METADATA_API_URL"),
    api_key=os.getenv("METADATA_API_KEY"),
    verify_ssl=False,
)
```

---

## Step 2 — Verify the connection

Check that you can reach the API and that your key has access:

```python
total = me.count_projects()
print(f"You have access to {total} projects.")
```

If this raises an error, double-check your URL and API key.

---

## Step 3 — Browse your projects

Get a quick overview of what's in your instance:

```python
# List the 10 most recently updated projects
me.list_projects(limit=10, sort_by="updated_desc")
```

This returns a pandas DataFrame. You can also filter by metadata type or search by keyword:

```python
# Only indicators
me.list_projects(limit=50, metadata_type="indicator")

# Projects whose title or idno contains "poverty"
me.list_projects(limit=50, keywords="poverty")
```

To retrieve every project (paginates automatically in batches of 500):

```python
all_projects = me.list_projects(limit="All")
```

The DataFrame index is the project's **internal numeric `id`**. Note that this is different from the human-readable `idno` field (e.g. `"WB_NY.GDP.MKTP.CD"`).

---

## Step 4 — Identify a specific record

Once you've spotted a project of interest in the listing, fetch its full details with its `id`:

```python
# Using an id from the listing above
project = me.get_project_by_id(1042)
print(project["title"])
print(project["type"])          # e.g. "indicator", "survey", "document"
print(project["template_uid"])  # the template this project uses
```

The returned `pd.Series` includes the title, type, idno, creation date, and the `template_uid` of the metadata template in use.

---

## Step 5 — Retrieve the metadata

Fetch the full metadata record in your preferred format. Three formats are available:

=== "Pydantic model (recommended)"

    ```python
    metadata = me.get_project_metadata_by_id(1042, output_mode="pydantic")

    # Navigate with dot notation
    print(metadata.series_description.name)

    # Edit a field
    metadata.series_description.definition_long = "Updated definition."
    ```

=== "Dictionary"

    ```python
    metadata = me.get_project_metadata_by_id(1042, output_mode="dict")

    # Navigate with standard dict access
    print(metadata["series_description"]["name"])
    ```

=== "Excel file"

    ```python
    filepath = me.get_project_metadata_by_id(
        1042,
        output_mode="excel",
        filename="my_indicator.xlsx",
    )
    print(f"Saved to {filepath}")
    ```

See [Working with Formats](user_guide/06_working_with_formats.md) for a full comparison.

---

## Step 6 — Explore the schema

Not sure what fields are available? Generate an empty skeleton (an "outline") to see the full structure:

```python
# View as a dict
outline = me.make_metadata_outline("indicator", output_mode="dict")

# Or as an Excel file — useful for manual editing
me.make_metadata_outline("indicator", output_mode="excel", filename="indicator_template.xlsx")
```

The Pydantic model version is especially useful for exploring the schema interactively:

```python
outline = me.make_metadata_outline("indicator", output_mode="pydantic")
outline.series_description   # tab-complete to discover fields
```

---

## Step 7 — Make a change and save it back

After editing the metadata object (in any format), push the update to the database:

```python
# Fetch the current metadata as a Pydantic model
metadata = me.get_project_metadata_by_id(1042, output_mode="pydantic")

# Edit a field
metadata.series_description.definition_long = "Revised definition text."

# Save the change back
me.update_project_log_by_id(id=1042, new_metadata=metadata)
```

For a small, targeted change to a single field, the patch approach is more precise:

```python
me.patch_update_project_log_by_id(
    id=1042,
    op="replace",
    path="/series_description/definition_long",
    value="Revised definition text.",
)
```

---

## Step 8 — Create a new metadata record

Start with an outline, fill in the required fields, then log it to the database:

```python
# Get an empty outline
new_metadata = me.make_metadata_outline("indicator", output_mode="pydantic")

# Fill in key fields
new_metadata.series_description.idno = "MY_INDICATOR_001"
new_metadata.series_description.name = "My New Indicator"
new_metadata.series_description.definition_long = "A detailed description."

# Create the record — returns the new project's id
new_id = me.create_project_log(new_metadata)
print(f"Created project with id: {new_id}")
```

---

## Next steps

| What you want to do | Where to go |
|--------------------|------------|
| Search, filter, and paginate projects | [Browsing Projects](user_guide/01_browsing_projects.md) |
| Understand templates and schemas | [Schemas & Templates](user_guide/02_schemas_and_templates.md) |
| Work with dict/Pydantic/Excel formats | [Working with Formats](user_guide/06_working_with_formats.md) |
| Auto-generate metadata with an LLM | [AI-Powered Generation](user_guide/07_ai_powered_generation.md) |
| Organize projects into collections | [Managing Collections](user_guide/08_managing_collections.md) |
| Full method reference | [API Reference](reference/api.md) |
