# Working with Formats

Most metadata methods support three interchangeable output formats: **dict**, **Pydantic model**, and **Excel**. This section explains each format, when to use it, and how to convert between them.

---

## The three formats at a glance

| Format | `output_mode` value | Best for |
|--------|--------------------|----|
| Python dictionary | `"dict"` | Programmatic access, JSON serialization, quick inspection |
| Pydantic model | `"pydantic"` | Type-safe editing, dot notation, validation, LLM output |
| Excel spreadsheet | `"excel"` | Manual editing, sharing with collaborators, bulk input |

---

## Requesting a specific format

Every metadata retrieval method accepts `output_mode`:

```python
# Pydantic model
metadata = me.get_project_metadata_by_id(1042, output_mode="pydantic")

# Dictionary
metadata = me.get_project_metadata_by_id(1042, output_mode="dict")

# Excel file (returns the file path)
filepath = me.get_project_metadata_by_id(1042, output_mode="excel", filename="my_file.xlsx")
```

The same applies to `make_metadata_outline()`:

```python
outline_pydantic = me.make_metadata_outline("indicator", output_mode="pydantic")
outline_dict     = me.make_metadata_outline("indicator", output_mode="dict")
filepath         = me.make_metadata_outline("indicator", output_mode="excel")
```

---

## Pydantic models

Pydantic models are the richest format for Python-based work. They provide:

- **Dot notation navigation**: `metadata.series_description.name`
- **Tab completion** in Jupyter notebooks and IDEs
- **Pretty printing**: `metadata.pretty_print()`
- **Type validation**: wrong value types raise clear errors

```python
metadata = me.get_project_metadata_by_id(1042, output_mode="pydantic")

# Read fields
print(metadata.series_description.name)

# Edit fields
metadata.series_description.definition_long = "Updated definition."

# Inspect structure
print(list(metadata.model_fields.keys()))
```

---

## Dictionaries

Dictionaries are plain Python dicts — lightweight and easy to serialize to JSON:

```python
import json

metadata = me.get_project_metadata_by_id(1042, output_mode="dict")

# Standard dict access
print(metadata["series_description"]["name"])

# Serialize
json_string = json.dumps(metadata, indent=2)
```

---

## Excel files

The Excel format produces a structured spreadsheet that non-technical users can fill in and return. Use it to:

- Distribute blank templates to data curators
- Review and edit metadata in a familiar tool
- Bulk-create records from existing spreadsheets

```python
# Export to Excel
filepath = me.save_metadata_to_excel(metadata, filename="indicator_1042.xlsx")

# Read back into Python after editing
updated = me.read_metadata_from_excel("indicator_1042.xlsx")           # Pydantic (default)
updated = me.read_metadata_from_excel("indicator_1042.xlsx", output_mode="dict")
```

---

## Converting between formats

Use `change_mode_or_template()` to convert a metadata object between formats without touching the database:

```python
# Pydantic → dict
metadata_dict = me.change_mode_or_template(metadata_pydantic, output_mode="dict")

# dict → Excel
filepath = me.change_mode_or_template(metadata_dict, output_mode="excel", filename="out.xlsx")

# Excel → Pydantic
metadata_pydantic = me.read_metadata_from_excel("out.xlsx")
```

### Re-template during conversion

You can also switch to a different template in the same step:

```python
# Convert to dict using a different template
converted = me.change_mode_or_template(
    metadata,
    output_mode="dict",
    output_template_uid="MY_CUSTOM_TEMPLATE_v01",
)
```

---

## Output mode aliases

The following aliases are also accepted (case-insensitive):

| Canonical | Accepted aliases |
|-----------|-----------------|
| `"dict"` | `"dictionary"` |
| `"pydantic"` | `"model"`, `"basemodel"`, `"object"` |
| `"excel"` | — |
