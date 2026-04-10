# Module: `templates.py`

**Location:** `pymetadataeditor/templates.py`

## Overview

This module converts metadata templates — dictionaries fetched from the Metadata Editor API — into Pydantic model classes. Templates define the schema and validation rules for a given metadata type (e.g., indicator, microdata). The resulting Pydantic models allow structured, type-safe access to metadata fields.

**Public API:** `pydantic_from_template` (the only export via `__all__`).

---

## What is a Template?

A template is a dictionary returned by the Metadata Editor API (via `list_templates()` or `get_template_by_uid()`). It contains a list of field definitions, where each field has:

- `key`: dot-notation path, e.g., `"series_description.name"`
- `type`: the field type (e.g., `"string"`, `"array"`, `"section"`)
- `required`: whether the field is required
- `rules`: optional validation constraints (e.g., `"min:2|max:100"`)

Templates are resolved against a base Pydantic schema from the `metadataschemas` library, and the constraints from the template can overlay the schema constraints.

---

## Key Function: `pydantic_from_template()`

```python
def pydantic_from_template(
    template: dict,
    parent_schema: Type[BaseModel],
    apply_rules: bool = True
) -> Type[BaseModel]
```

The main entry point. Converts a template dictionary into a Pydantic model class by:

1. Flattening dot-notation keys into a hierarchy via `dot_to_hierarchy()`
2. Dispatching each field to the appropriate handler via `template_type_handler()`
3. Composing nested models for sections and arrays
4. Returning a fully-formed Pydantic model class

**Parameters:**
- `template` (dict): The template definition from the API.
- `parent_schema` (Type[BaseModel]): The base metadata schema (from `metadataschemas`) to resolve fields against.
- `apply_rules` (bool): If `True`, applies validation constraints from the template. If `False`, returns a rule-free model suitable for LLM population. Default `True`.

**Returns:** `Type[BaseModel]` — A dynamically created Pydantic model class.

**Used by:** `interface.py` → `_get_template_class_and_type_and_UID()`

---

## Field Type Handlers

The `template_type_handler()` function dispatches each field definition to the correct handler based on its `type`.

| Template Field Type | Handler Function | Python Type |
|---------------------|-----------------|-------------|
| `string` | `define_simple_element()` | `Optional[str]` |
| `text` | `define_simple_element()` | `Optional[str]` |
| `textarea` | `define_simple_element()` | `Optional[str]` |
| `integer` | `define_simple_element()` | `Optional[int]` |
| `number` | `define_simple_element()` | `Optional[float]` |
| `boolean` | `define_simple_element()` | `Optional[bool]` |
| `date` | `define_simple_element()` | `Optional[str]` |
| `array` | `define_array_element()` | `Optional[List[BaseModel]]` |
| `nested_array` | `define_array_element()` | `Optional[List[BaseModel]]` |
| `simple_array` | `define_simple_array_element()` | `Optional[List[str]]` |
| `section` | `define_group_of_elements()` | Nested `BaseModel` |
| `section_container` | `define_group_of_elements()` | Nested `BaseModel` |

---

## Handler Functions

### `define_simple_element(item, parent_schema, element_type, apply_rules)`

Handles scalar fields (`string`, `text`, `integer`, `number`, `boolean`, `date`, `textarea`). Looks up the field in the parent schema to inherit its metadata (title, description, alias), then applies the `required` and constraint rules from the template.

### `define_array_element(item, parent_schema, apply_rules)`

Handles complex list fields (`array`, `nested_array`). The list elements are themselves structured objects (nested Pydantic models). Recursively processes the sub-fields of the array elements.

### `define_simple_array_element(item, parent_schema, apply_rules)`

Handles simple list fields (`simple_array`) where elements are plain strings, e.g., `List[str]`.

### `define_group_of_elements(item, parent_schema, apply_rules)`

Handles nested groups (`section`, `section_container`). Creates a child Pydantic model for the group and returns it as a field on the parent model.

---

## Constraint Parsing: `get_constraints_from_string()`

```python
def get_constraints_from_string(rules_string: str) -> list
```

Parses the `rules` field from a template item (a pipe-separated string like `"min:2|max:100|alpha_dash"`) and returns a list of Pydantic constraint metadata objects (e.g., `MinLen`, `MaxLen`, `Ge`, `Le`).

**Supported constraints:**

| Rule | Applied As |
|------|------------|
| `min:N` | `MinLen(N)` for strings, `Ge(N)` for numbers |
| `max:N` | `MaxLen(N)` for strings, `Le(N)` for numbers |
| `alpha_dash` | Pattern constraint allowing letters, digits, `-`, `_` |
| `required` | Sets `default=...` (Pydantic required marker) |

---

## Utility Functions

### `copy_field_set_required_status(field, required) -> FieldInfo`

Creates a copy of a Pydantic `FieldInfo` with the `required` status changed. Used to apply the template's `required` setting to fields inherited from the base schema.

```python
def copy_field_set_required_status(field: FieldInfo, required: bool) -> FieldInfo
```

### `dot_to_hierarchy(template_items) -> dict`

Converts a flat list of template items with dot-notation `key` fields into a nested dictionary hierarchy. For example, `"series_description.name"` becomes `{"series_description": {"name": ...}}`.

### `fill_skipped_field_info(template_items) -> list`

Fills in field information for template items that reference parent fields by dot notation, ensuring all fields have the metadata needed for Pydantic model creation.

### `strip_model_rules(model) -> Type[BaseModel]`

Re-exported from `utils.py`. Used to create constraint-free versions of template-derived models (needed for LLM metadata population). See [`utils.md`](utils.md).

---

## Common Pattern

```python
# Internally, when a template UID is resolved:
template_dict = me.get_template_by_uid("my-template-uid")
base_schema = MetadataManager().get_metadata_class("indicator")

# Convert template to Pydantic model
TemplateModel = pydantic_from_template(template_dict, base_schema, apply_rules=True)

# Create an outline instance
outline = make_skeleton(TemplateModel)
```

This pattern is abstracted behind `MetadataEditor.make_metadata_outline()` and `MetadataEditor.get_metadata_class()`.
