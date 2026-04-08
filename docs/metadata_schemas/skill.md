# Metadata Schemas — Skill Reference

This is the dedicated skill file for working with the `metadataschemas` package
inside `pymetadataeditor`. It documents the sibling source repo
[`tonyfujs/metadata-schemas`](https://github.com/tonyfujs/metadata-schemas), the
public API surface that `pymetadataeditor` already integrates with, and the
per-schema reference files an agent should consult before writing schema-aware
code.

The general agent skill for `pymetadataeditor` lives at
[`docs/skill.md`](../skill.md). Read that first for the package context, then
come here when the task touches metadata schemas.

---

## When to use this skill

Consult this file before doing any of the following:

- Adding a new public method to `MetadataEditor` that returns, validates, or
  transforms a metadata object
- Supporting a new metadata type end-to-end
- Fixing a bug in `templates.py`, `llm_helpers.py`, or schema-touching parts
  of `interface.py`
- Debugging Excel read/write round-trips
- Writing tests that instantiate any `*Schema` model
- Investigating why a field is missing or has the wrong type after a refactor

If the task only touches HTTP, auth, project listing, or pure utility code with
no `metadataschemas` import, this skill is not needed.

---

## What is `metadataschemas`?

`metadataschemas` is a PyPI package
([source](https://github.com/tonyfujs/metadata-schemas), maintained by the
World Bank) that provides:

1. **Canonical JSON Schema definitions** for 10 supported metadata types in the
   `schemas/` directory of the source repo
2. **Auto-generated Pydantic v2 models** in `pydantic_schemas/<type>_schema.py`,
   regenerated from the JSON via `generate_pydantic_schemas.py`
3. **A `MetadataManager` class** that wraps schema discovery, skeleton
   creation, and Excel I/O
4. **Shared utilities** in `metadataschemas.utils.utils` that
   `pymetadataeditor` imports and reuses (annotation introspection, dict
   merging, key standardization)
5. **Excel templates** in `excel_sheets/` for each metadata type

`pymetadataeditor` declares it as a dependency in `pyproject.toml`
(`metadataschemas = "^0.1.3"`) and imports from it in **every source file** of
the package. Live docs for the schemas themselves:
<https://worldbank.github.io/metadata-schemas/>.

---

## Repository map for `tonyfujs/metadata-schemas`

```
metadata-schemas/
├── schemas/                          # Canonical JSON Schema files (source of truth)
│   ├── document-schema.json
│   ├── geospatial-schema.json
│   ├── image-schema.json
│   ├── microdata-schema.json
│   ├── timeseries-schema.json        # → "indicator"
│   ├── timeseries-db-schema.json     # → "indicators_db"
│   ├── resource-schema.json
│   ├── script-schema.json
│   ├── table-schema.json
│   ├── video-schema.json
│   ├── ddi-schema.json               # Sub-schema referenced by microdata
│   ├── datacite-schema.json          # Sub-schema referenced by indicator
│   ├── provenance-schema.json        # Shared provenance fields
│   ├── variable-schema.json          # Shared variable fields
│   ├── variable-group-schema.json
│   ├── series-schema.json
│   ├── datafile-schema.json
│   ├── dcmi-schema.json
│   ├── iptc-pmd-schema.json          # Shared image metadata
│   └── iptc-phovidmdshared-schema.json
│
├── pydantic_schemas/                 # Auto-generated Pydantic v2 models
│   ├── __init__.py                   # (empty)
│   ├── metadata_manager.py           # MetadataManager class
│   ├── document_schema.py
│   ├── geospatial_schema.py
│   ├── image_schema.py
│   ├── indicator_schema.py
│   ├── indicators_db_schema.py
│   ├── microdata_schema.py
│   ├── resource_schema.py
│   ├── script_schema.py
│   ├── table_schema.py
│   ├── video_schema.py
│   ├── generators/
│   │   ├── generate_pydantic_schemas.py   # JSON → Pydantic
│   │   └── generate_excel_files.py        # Pydantic → Excel
│   └── utils/
│       ├── schema_base_model.py      # SchemaBaseModel base class
│       ├── utils.py                  # Shared annotation/dict helpers
│       ├── quick_start.py            # make_skeleton()
│       ├── excel_to_pydantic.py
│       └── pydantic_to_excel.py
│
├── excel_sheets/                     # Pre-formatted Excel templates
│   └── <Type>_metadata.xlsx
│
└── json_to_python_config.yaml        # name → JSON file → Python module → class
```

The `pip install metadataschemas` package ships only the contents of
`pydantic_schemas/`. The raw JSON files in `schemas/` are not bundled — fetch
them from the source repo when you need to inspect them.

---

## Public API the agent must know

### `metadataschemas.metadata_manager.MetadataManager`

The main entry point. Already used by `pymetadataeditor/interface.py`.

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
```

| Method / property | Returns | What it does |
|---|---|---|
| `metadata_type_names` | `list[str]` | The 10 canonical names (see table below) |
| `metadata_class_from_name(name)` | `type[BaseModel]` | Pydantic class for a name; calls `standardize_metadata_name` first |
| `standardize_metadata_name(name)` | `str` | Canonical name; handles aliases (`survey` → `microdata`, `timeseries` → `indicator`, `timeseries_db`/`indicator_db` → `indicators_db`) |
| `create_metadata_outline(name_or_class, debug=False)` | `BaseModel` | Skeleton instance with all fields set to defaults / `None`; thin wrapper over `make_skeleton` |
| `write_metadata_outline_to_excel(name, filename=None, ...)` | `str` | Writes a blank Excel template for the given type |
| `save_metadata_to_excel(metadata_object, filename=None, ...)` | `str` | Serialises a populated metadata object to Excel |
| `read_metadata_from_excel(filename, ...)` | `BaseModel` | Reads an Excel file back into a Pydantic instance |

### `metadataschemas.utils.schema_base_model.SchemaBaseModel`

Base class that every generated `*Schema` model inherits from. It provides
`pretty_print()`, populates `model_config = ConfigDict(populate_by_name=True,
extra="forbid", validate_assignment=True)`, and other Pydantic v2 niceties.
**Any new model that mimics a generated schema must subclass this** so that
field aliasing and validation behave consistently.

### `metadataschemas.utils.utils` — reusable utilities

These already power `pymetadataeditor`. **Always import them — never
reimplement them.**

| Function | Use |
|---|---|
| `merge_dicts(a, b)` | Deep-merge two dicts; `b` wins on conflicts |
| `standardize_keys_in_dict(d)` | Normalises keys (lowercase, replace separators) |
| `is_optional_annotation(t)` | `True` if `t` is `Optional[X]` / `Union[X, None]` |
| `is_list_annotation(t)` | `True` if `t` is `list[X]` |
| `is_optional_list(t)` | `True` if `t` is `Optional[list[X]]` |
| `get_subtype_of_optional_or_list(t)` | Returns the inner type `X` |
| `subset_pydantic_model_type(model, fields)` | Builds a new model containing only the named fields |

### `metadataschemas.utils.quick_start.make_skeleton(schema, debug=False)`

Creates an instantiated Pydantic model with all fields populated to defaults
(typically `None` or empty list). `MetadataManager.create_metadata_outline()`
delegates to this. `pymetadataeditor/llm_helpers.py` uses it directly.

---

## Supported metadata types — master table

Source of truth: `metadata-schemas/json_to_python_config.yaml`. All schemas are
currently at version `0.1.0`.

| Canonical name | API alias | Pydantic class | JSON schema | Reference file |
|---|---|---|---|---|
| `document` | `document` | `document_schema.ScriptSchemaDraft` | `schemas/document-schema.json` | [schemas/document.md](schemas/document.md) |
| `geospatial` | `geospatial` | `geospatial_schema.GeospatialSchema` | `schemas/geospatial-schema.json` | [schemas/geospatial.md](schemas/geospatial.md) |
| `image` | `image` | `image_schema.ImageDataTypeSchema` | `schemas/image-schema.json` | [schemas/image.md](schemas/image.md) |
| `indicator` | `timeseries` | `indicator_schema.TimeseriesSchema` | `schemas/timeseries-schema.json` | [schemas/indicator.md](schemas/indicator.md) |
| `indicators_db` | `timeseries_db` | `indicators_db_schema.TimeseriesDatabaseSchema` | `schemas/timeseries-db-schema.json` | [schemas/indicators_db.md](schemas/indicators_db.md) |
| `microdata` | `survey` | `microdata_schema.MicrodataSchema` | `schemas/microdata-schema.json` | [schemas/microdata.md](schemas/microdata.md) |
| `resource` | `resource` | `resource_schema.Model` | `schemas/resource-schema.json` | [schemas/resource.md](schemas/resource.md) |
| `script` | `script` | `script_schema.ResearchProjectSchemaDraft` | `schemas/script-schema.json` | [schemas/script.md](schemas/script.md) |
| `table` | `table` | `table_schema.Model` | `schemas/table-schema.json` | [schemas/table.md](schemas/table.md) |
| `video` | `video` | `video_schema.Model` | `schemas/video-schema.json` | [schemas/video.md](schemas/video.md) |

### Name aliases handled by `standardize_metadata_name()`

| Input | Canonical |
|---|---|
| `survey`, `survey_microdata` | `microdata` |
| `timeseries` | `indicator` |
| `timeseries_db`, `indicator_db` | `indicators_db` |

Always normalise user-supplied names through `MetadataManager.standardize_metadata_name`
before using them as keys or building API paths.

---

## Where pymetadataeditor already integrates

A literal inventory so an agent can grep locally instead of re-reading source.

### `pymetadataeditor/interface.py`

```python
from metadataschemas.metadata_manager import MetadataManager
from metadataschemas.utils.schema_base_model import SchemaBaseModel
from metadataschemas.utils.utils import merge_dicts, standardize_keys_in_dict
```

`MetadataEditor` uses `MetadataManager` to resolve metadata types and create
outlines, and `SchemaBaseModel` as a type hint for any function that accepts a
schema instance.

### `pymetadataeditor/templates.py`

```python
from metadataschemas.utils.schema_base_model import SchemaBaseModel
from metadataschemas.utils.utils import (
    get_subtype_of_optional_or_list,
    is_list_annotation,
    is_optional_annotation,
    is_optional_list,
    merge_dicts,
    standardize_keys_in_dict,
)
```

Templates extend the base schemas dynamically. The annotation utilities are
used to walk Pydantic field types and rebuild them with adjusted required
status.

### `pymetadataeditor/llm_helpers.py`

```python
from metadataschemas.utils.quick_start import make_skeleton
from metadataschemas.utils.utils import (
    get_subtype_of_optional_or_list,
    is_list_annotation,
    is_optional_annotation,
    is_optional_list,
    subset_pydantic_model_type,
)
```

LLM helpers use `make_skeleton` to seed an empty pydantic object that the LLM
will populate field-by-field, and `subset_pydantic_model_type` to ask the LLM
about a subset of fields at a time.

### `pymetadataeditor/utils.py`

```python
from metadataschemas.utils.utils import (
    is_list_annotation,
    is_optional_annotation,
    is_optional_list,
)
```

Used by `strip_model_rules()` to recurse over a model's field types when
removing validation constraints for LLM structured output.

---

## Common task recipes

### Resolve a user-supplied name to its pydantic class

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
canonical = mm.standardize_metadata_name(user_input)   # "survey" → "microdata"
schema_cls = mm.metadata_class_from_name(canonical)     # MicrodataSchema
```

### Create a blank metadata object for any type

```python
mm = MetadataManager()
obj = mm.create_metadata_outline("indicator")
obj.series_description.idno = "GDP_PC_001"
obj.series_description.name = "GDP per capita"
```

### Validate a raw dict against a schema

```python
from metadataschemas.metadata_manager import MetadataManager
from pydantic import ValidationError

mm = MetadataManager()
schema_cls = mm.metadata_class_from_name("geospatial")

try:
    obj = schema_cls.model_validate(raw_dict)
except ValidationError as e:
    # Handle field-level errors
    ...
```

### Read or write Excel

```python
mm = MetadataManager()

# Blank template
blank_path = mm.write_metadata_outline_to_excel("microdata", filename="blank.xlsx")

# Populated object → Excel
populated_path = mm.save_metadata_to_excel(microdata_obj, filename="filled.xlsx")

# Excel → Pydantic
loaded = mm.read_metadata_from_excel("filled.xlsx")
```

### Fetch the source JSON schema for inspection

When you need the raw JSON (e.g. to look up enum values, descriptions, or
nested structure not exposed by the pydantic class), fetch it from the source
repo:

```python
# From a Claude Code session with GitHub MCP access:
mcp__github__get_file_contents(
    owner="tonyfujs",
    repo="metadata-schemas",
    path="schemas/timeseries-schema.json",
    ref="main",
)
```

Or via raw URL:

```
https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/timeseries-schema.json
```

---

## Versioning and regeneration workflow

The schemas are versioned independently of `pymetadataeditor`. From
`metadata-schemas/README.md`:

| Bump | Triggered by |
|---|---|
| **Major** | Breaking field type changes (e.g. string → array), or a new mandatory field, or an optional field becoming mandatory |
| **Minor** | Field removed, or a new optional field added |
| **Patch** | Coercible type changes (e.g. int → string) |

**Update procedure** (run inside `tonyfujs/metadata-schemas`, on a feature
branch):

1. Edit the JSON file in `schemas/`
2. Bump `version` in `pyproject.toml`
3. Bump the per-schema `version` in `json_to_python_config.yaml`
4. Regenerate pydantic models:
   `python pydantic_schemas/generators/generate_pydantic_schemas.py`
5. Regenerate Excel templates:
   `python -m pydantic_schemas.generators.generate_excel_files`
6. Cut a release; bump `metadataschemas` in `pymetadataeditor/pyproject.toml`

**Rule for agents:** Never edit the generated `pydantic_schemas/*_schema.py`
files directly — they get overwritten on the next regeneration. Edit the JSON
schema and regenerate.

---

## Things to never do

- **Don't bundle JSON schema files inside `pymetadataeditor/`.** They live in
  the sibling repo and are pulled in via the `metadataschemas` PyPI package.
- **Don't reimplement annotation introspection** (`is_optional_annotation`,
  `is_list_annotation`, `is_optional_list`, `get_subtype_of_optional_or_list`,
  `merge_dicts`, `standardize_keys_in_dict`). They are already exported from
  `metadataschemas.utils.utils`.
- **Don't hardcode the list of metadata types.** Delegate to
  `MetadataManager().metadata_type_names`.
- **Don't use `survey`, `timeseries`, or `timeseries_db` as canonical names**
  in new code. Always normalise via `MetadataManager.standardize_metadata_name`.
- **Don't edit the generated pydantic files in `metadataschemas`.** Edit the
  JSON schema and regenerate.
- **Don't subclass `BaseModel` directly for schema-shaped data.** Subclass
  `metadataschemas.utils.schema_base_model.SchemaBaseModel` so that field
  aliasing, `extra="forbid"`, and `validate_assignment=True` apply.

---

## Per-schema reference files

Each supported metadata type has a dedicated reference file with its top-level
fields, required fields, common pitfalls, and instantiation example:

- [schemas/document.md](schemas/document.md)
- [schemas/geospatial.md](schemas/geospatial.md)
- [schemas/image.md](schemas/image.md)
- [schemas/indicator.md](schemas/indicator.md)
- [schemas/indicators_db.md](schemas/indicators_db.md)
- [schemas/microdata.md](schemas/microdata.md)
- [schemas/resource.md](schemas/resource.md)
- [schemas/script.md](schemas/script.md)
- [schemas/table.md](schemas/table.md)
- [schemas/video.md](schemas/video.md)
