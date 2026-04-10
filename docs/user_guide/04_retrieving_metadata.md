# Retrieving Existing Metadata

This section explains how to fetch metadata records from the database in each of the three supported output formats, and how to read metadata back from an Excel file.

---

## Retrieve metadata by project id

`get_project_metadata_by_id()` is the primary method for fetching an existing record. It requires the project's integer `id` (visible as the DataFrame index from `list_projects()`).

=== "Pydantic model"

    ```python
    metadata = me.get_project_metadata_by_id(1042, output_mode="pydantic")

    # Navigate with dot notation
    print(metadata.series_description.name)
    print(metadata.series_description.definition_long)

    # Pretty-print the full record
    metadata.pretty_print()
    ```

=== "Dictionary"

    ```python
    metadata = me.get_project_metadata_by_id(1042, output_mode="dict")

    print(metadata["series_description"]["name"])
    ```

=== "Excel file"

    ```python
    filepath = me.get_project_metadata_by_id(
        1042,
        output_mode="excel",
        filename="indicator_1042.xlsx",
    )
    print(f"Saved to {filepath}")
    ```

---

## The `simplify` option

By default (`simplify=True`), empty fields and empty nested objects are stripped from the returned metadata. This keeps the output lean and readable. Set `simplify=False` to get the full schema with all fields, including empty ones:

```python
# Full schema with all empty fields shown
metadata = me.get_project_metadata_by_id(1042, output_mode="pydantic", simplify=False)
```

---

## Re-template metadata on retrieval

If you want the metadata cast into a different template (e.g. when migrating between schema versions), supply the target template UID:

```python
metadata = me.get_project_metadata_by_id(
    1042,
    output_mode="pydantic",
    template_uid="IHSN_INDICATOR_1-0_Template_v01_EN",
)
```

This maps the stored fields onto the new template's structure as closely as possible.

---

## Read metadata from an Excel file

If you or a colleague previously exported metadata to Excel, you can read it back with:

```python
metadata = me.read_metadata_from_excel("indicator_1042.xlsx")
# Returns a Pydantic model by default

# Or as a dict
metadata_dict = me.read_metadata_from_excel("indicator_1042.xlsx", output_mode="dict")
```

The Excel format is described in [Working with Formats](06_working_with_formats.md).

---

## Iterating over many records

A common pattern is to retrieve all projects of a given type and process each one:

```python
# List all indicator projects
projects_df = me.list_projects(limit="All", metadata_type="indicator")

for project_id in projects_df.index:
    metadata = me.get_project_metadata_by_id(project_id, output_mode="dict")
    # ... process metadata ...
```

For large catalogues, consider working in batches to avoid memory issues.
