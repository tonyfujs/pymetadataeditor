# Output Modes

Most metadata methods in pyMetadataEditor accept an `output_mode` parameter that controls the format of the returned data. Three modes are available.

---

## `"pydantic"` — Pydantic model

Returns a typed Python object with dot-notation access, tab completion, and built-in validation.

```python
metadata = me.get_project_metadata_by_id(1042, output_mode="pydantic")

# Dot notation
print(metadata.series_description.name)

# Edit and validate
metadata.series_description.name = "New name"

# Pretty-print
metadata.pretty_print()
```

**Accepted aliases:** `"pydantic"`, `"model"`, `"basemodel"`, `"object"`

**Best for:** Python-based editing, type-safe workflows, LLM-assisted generation, interactive exploration.

---

## `"dict"` — Python dictionary

Returns a plain `dict`. Fields are nested according to the schema structure.

```python
metadata = me.get_project_metadata_by_id(1042, output_mode="dict")

print(metadata["series_description"]["name"])
```

**Accepted aliases:** `"dict"`, `"dictionary"`

**Best for:** JSON serialization, lightweight programmatic access, passing data to other libraries.

---

## `"excel"` — Excel spreadsheet

Writes the metadata to a formatted `.xlsx` file and returns the file path as a string.

```python
# Returns the file path
filepath = me.get_project_metadata_by_id(1042, output_mode="excel", filename="out.xlsx")

# Automatic filename if not specified
filepath = me.get_project_metadata_by_id(1042, output_mode="excel")
```

**Best for:** Sharing with non-technical collaborators, manual editing, bulk input workflows.

---

## Which methods support `output_mode`?

All methods that return a metadata record support `output_mode`:

| Method | Supports `output_mode` |
|--------|----------------------|
| `get_project_metadata_by_id()` | Yes |
| `make_metadata_outline()` | Yes |
| `draft_metadata_from_files()` | Yes |
| `augment_metadata_from_files()` | Yes |
| `change_mode_or_template()` | Yes |
| `read_metadata_from_excel()` | Yes (`"pydantic"` or `"dict"`) |

---

## Converting between modes

Use `change_mode_or_template()` to convert an existing metadata object without touching the database:

```python
# Pydantic → dict
as_dict = me.change_mode_or_template(metadata_pydantic, output_mode="dict")

# dict → Excel
filepath = me.change_mode_or_template(metadata_dict, output_mode="excel")

# Read Excel back to Pydantic
as_pydantic = me.read_metadata_from_excel(filepath)
```
