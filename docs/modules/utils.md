# Module: `utils.py`

**Location:** `pymetadataeditor/utils.py`

## Overview

Shared helper functions used across the package. This module provides utilities for validating JSON Patch operations (RFC 6902), cleaning empty values from nested data structures, and stripping Pydantic validation constraints from type annotations.

These functions are primarily consumed by `interface.py` and `templates.py` and are not part of the public API.

---

## Function Reference

### `validate_json_patches(patches: list) -> list`

Validates a list of JSON Patch dictionaries according to [RFC 6902](https://jsonpatch.com/).

**Parameters:**
- `patches` (list): A list of JSON patch dicts, each with at minimum `"op"` and `"path"` keys.

**Returns:** `list` — The validated patches with paths corrected (prepends `/` if missing).

**Raises:** `ValueError` — If any patch dict is malformed, has an invalid `op`, has a non-string `path`, or is missing required fields (`value` for `add`/`replace`/`test`, `from` for `move`/`copy`).

**Valid operations:** `add`, `remove`, `replace`, `move`, `copy`, `test`

**Used by:** `interface.py` → `patch_update_project_log_by_id()`

```python
patches = validate_json_patches([{"op": "replace", "path": "/title", "value": "New Title"}])
```

---

### `remove_empty_from_dict(old_dict: Dict) -> Dict`

Recursively removes entries from a dictionary where the value is `None` or an empty string `""`. Nested dicts and lists are also cleaned, and the parent entry is removed if the nested structure becomes empty after cleaning.

**Parameters:**
- `old_dict` (dict): The dictionary to clean.

**Returns:** `dict` — A new dictionary with empty/null values removed.

**Used by:** `interface.py` before POSTing metadata to the API (ensures clean payloads).

```python
cleaned = remove_empty_from_dict({"title": "My Study", "abstract": "", "authors": [{"name": ""}]})
# Returns: {"title": "My Study"}
```

---

### `remove_empty_from_list(v: list) -> list`

Recursively removes `None` values and empty strings from a list. Nested dicts and lists are cleaned using `remove_empty_from_dict` / `remove_empty_from_list` respectively. The element is excluded if it becomes empty after cleaning.

**Parameters:**
- `v` (list): The list to clean.

**Returns:** `list` — A new list with empty/null values removed.

**Used by:** `remove_empty_from_dict()` for list-valued fields.

---

### `strip_constraints_from_annotated(annotation: Any) -> Any`

Strips Pydantic validation constraints from `Annotated` type hints, while preserving the base type. Handles `Optional`, `List`, `Optional[List[...]]`, and combinations.

**Parameters:**
- `annotation` (Any): A Python type annotation, potentially wrapped in `Annotated[...]`.

**Returns:** The unwrapped base type (e.g., `Annotated[str, StringConstraints(min_length=1)]` → `str`).

**Used by:** `strip_model_rules()`.

---

### `strip_model_rules(original_model: Type[BaseModel]) -> Type[BaseModel]`

Creates a new Pydantic model class that is structurally identical to `original_model` but with all validation constraints removed. Retains field titles and descriptions. Processes nested models recursively.

This is needed when populating metadata outlines from LLM output — the LLM may produce values that violate strict constraints, so a constraint-free model is used for initial population before validation.

**Parameters:**
- `original_model` (Type[BaseModel]): The Pydantic model class to strip.

**Returns:** `Type[BaseModel]` — A new model class with the same structure but no validation constraints.

**Handles:** `Annotated` types, `Optional`, `List`, `Union`, and nested `BaseModel` subclasses.

**Used by:** `templates.py` → `strip_model_rules()`, `interface.py` → `_get_metadata_class_and_type_and_UID()`

---

## Usage Patterns

These utilities are internal and rarely called directly by users. However, understanding them is helpful when:

- Debugging why metadata dicts come back smaller than expected (empty values are stripped before API calls)
- Understanding why template-derived Pydantic models accept LLM output that would otherwise fail validation
- Writing custom JSON Patch operations to partially update project metadata
