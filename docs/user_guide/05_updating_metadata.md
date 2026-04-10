# Updating Metadata

There are two ways to update an existing metadata record: a **full replacement** with `update_project_log_by_id()`, or a **surgical patch** with `patch_update_project_log_by_id()`. This section explains both and when to use each.

---

## Full replacement: `update_project_log_by_id()`

This method replaces the stored metadata with whatever you provide. It accepts the same input formats as `create_project_log()`: a Pydantic model, a dict, or a path to an Excel file.

### Typical pattern: fetch → edit → save

```python
# 1. Fetch the current metadata
metadata = me.get_project_metadata_by_id(1042, output_mode="pydantic")

# 2. Edit one or more fields
metadata.series_description.definition_long = "Revised definition."

# 3. Push the update
me.update_project_log_by_id(id=1042, new_metadata=metadata)
```

### Partial update with a dict

If you only want to change specific fields, pass a plain dict. The API merges it with the existing record:

```python
me.update_project_log_by_id(
    id=1042,
    new_metadata={
        "series_description": {
            "definition_long": "Revised definition."
        }
    },
)
```

### Update from an Excel file

```python
me.update_project_log_by_id(id=1042, new_metadata="edited_indicator.xlsx")
```

!!! warning "Template compatibility"
    If you change the template of a record during an update, all fields that don't exist in the new template will be dropped. Verify template compatibility with `list_templates()` before doing a template migration.

---

## Surgical patch: `patch_update_project_log_by_id()`

Patches apply a single [RFC 6902 JSON Patch](https://datatracker.ietf.org/doc/html/rfc6902) operation to the stored metadata. Use this when you want to change exactly one field without fetching the full record first.

### Supported operations

| `op` | Effect |
|------|--------|
| `"replace"` | Set a field to a new value |
| `"add"` | Add a new field or list item |
| `"remove"` | Delete a field |
| `"test"` | Verify a field has a specific value |

### Path syntax

The `path` uses JSON Pointer notation: `/` separates levels, starting from the metadata root. The leading `/` is added automatically if you omit it.

```
/series_description/definition_long      → the definition_long field
/series_description/topics/0/name        → first topic's name
```

### Examples

```python
# Replace a field's value
me.patch_update_project_log_by_id(
    id=1042,
    op="replace",
    path="/series_description/definition_long",
    value="Revised definition text.",
)

# Add a new field
me.patch_update_project_log_by_id(
    id=1042,
    op="add",
    path="/series_description/base_period",
    value="2015",
)

# Remove a field
me.patch_update_project_log_by_id(
    id=1042,
    op="remove",
    path="/series_description/base_period",
)

# Test that a field has the expected value (raises an error if it doesn't)
me.patch_update_project_log_by_id(
    id=1042,
    op="test",
    path="/series_description/idno",
    value="MY_INDICATOR_001",
)
```

---

## Choosing the right method

| Situation | Recommended approach |
|-----------|---------------------|
| Editing multiple fields at once | `update_project_log_by_id()` after fetch |
| Editing one specific field without fetching | `patch_update_project_log_by_id()` |
| Updating from a manually edited Excel file | `update_project_log_by_id()` with file path |
| Bulk updates across many records | `update_project_log_by_id()` in a loop |
| Precise, auditable single-field change | `patch_update_project_log_by_id()` |
