# Creating New Metadata

This section covers the full workflow for creating a new metadata record: starting from an empty schema outline, filling in the fields, and logging the record to the database.

---

## Overview

The typical creation workflow is:

1. Generate an empty outline for your metadata type
2. Fill in the fields (in Python or in Excel)
3. Log it to the database with `create_project_log()`

---

## Step 1 — Generate an empty outline

An outline is a blank instance of a metadata schema with every field present but empty. Start here rather than constructing a dict from scratch.

```python
# Pydantic model — best for Python-based editing
outline = me.make_metadata_outline("indicator", output_mode="pydantic")

# Dict — useful for building metadata programmatically
outline = me.make_metadata_outline("indicator", output_mode="dict")

# Excel — useful for filling in manually or sharing with collaborators
filepath = me.make_metadata_outline(
    "indicator",
    output_mode="excel",
    filename="new_indicator.xlsx",
)
```

---

## Step 2 — Fill in the fields

### Using the Pydantic model (recommended)

Pydantic models support dot notation and give you type hints and validation:

```python
outline = me.make_metadata_outline("indicator", output_mode="pydantic")

# Set top-level fields
outline.series_description.idno = "MY_INDICATOR_001"
outline.series_description.name = "GDP per capita (constant 2015 USD)"
outline.series_description.display_name = "GDP per capita"
outline.series_description.definition_long = (
    "GDP per capita is gross domestic product divided by midyear population."
)

# Nested objects use the same dot notation
outline.series_description.statistical_concept = "National accounts"

# Lists — update existing items or append new ones
outline.series_description.topics[0].id = "economy"
outline.series_description.topics[0].name = "Economy & Growth"
```

### Using a dictionary

```python
outline = me.make_metadata_outline("indicator", output_mode="dict")

outline["series_description"]["idno"] = "MY_INDICATOR_001"
outline["series_description"]["name"] = "GDP per capita (constant 2015 USD)"
```

### Using an Excel file

Export the outline to Excel, fill it in manually, then read it back:

```python
filepath = me.make_metadata_outline("indicator", output_mode="excel", filename="new_indicator.xlsx")
# ... edit the file manually ...
filled_metadata = me.read_metadata_from_excel(filepath)
```

---

## Step 3 — Log the record to the database

`create_project_log()` accepts a Pydantic model, a dict, or a path to an Excel file. It returns the new project's integer `id`:

```python
# From a Pydantic model
new_id = me.create_project_log(outline)
print(f"Created project with id: {new_id}")

# From a dict — must specify the type
new_id = me.create_project_log(
    {"series_description": {"idno": "MY_INDICATOR_001", "name": "GDP per capita"}},
    metadata_type_or_template_uid="indicator",
)

# From an Excel file
new_id = me.create_project_log("path/to/filled_indicator.xlsx")
```

!!! tip
    When passing a Pydantic model, the metadata type is inferred automatically. When passing a plain dict, you must supply `metadata_type_or_template_uid`.

---

## Creating metadata for different types

The workflow is the same for all types — only the type name and available fields differ:

```python
# Microdata (household survey)
outline = me.make_metadata_outline("microdata", output_mode="pydantic")
outline.study_desc.title_statement.title = "My Household Survey 2024"
me.create_project_log(outline)

# Document
outline = me.make_metadata_outline("document", output_mode="pydantic")
outline.document_description.title_statement.title = "My Research Report"
me.create_project_log(outline)
```

See the [Schema Reference](../reference/schemas/microdata.md) for field listings for each type.

---

## Let an LLM draft the metadata for you

If you have source files (PDFs, Word docs, web pages), you can have an LLM generate a first draft:

```python
draft = me.draft_metadata_from_files(
    llm_api_key=os.getenv("OPENAI_API_KEY"),
    files=["survey_manual.pdf"],
    metadata_type_or_template_uid="microdata",
    output_mode="pydantic",
)
# Review and edit draft, then log it
me.create_project_log(draft)
```

See [AI-Powered Metadata Generation](07_ai_powered_generation.md) for the full guide.
