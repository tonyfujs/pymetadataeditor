# `geospatial` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `geospatial` |
| **API alias** | `geospatial` |
| **Pydantic class** | `metadataschemas.geospatial_schema.GeospatialSchema` |
| **Source JSON schema** | [`schemas/geospatial-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/geospatial-schema.json) |
| **Excel template** | `excel_sheets/Geospatial_metadata.xlsx` |
| **Excel layout** | Multiple sheets (`write_across_many_sheets`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for geospatial datasets (rasters, vector layers, services). Based on
ISO 19115 / 19139 with World Bank extensions. This is one of the largest
schemas — the underlying JSON file is ~86 KB and `geospatial_schema.py`
defines ~80 pydantic classes.

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `idno` | `str` | Project unique identifier |
| `metadata_information` | `object` | Metadata about the metadata record |
| `description` | `object` | **Required.** The geospatial dataset description — citation, identification, distribution, spatial reference system, content info, etc. This is the bulk of the schema. |
| `provenance` | `array` | Provenance entries |
| `tags` | `array` | User-defined tags |
| `additional` | `object` | Free-form bag |

## Required fields

- `description`

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
geo = mm.create_metadata_outline("geospatial")
geo.idno = "GEO_PROJECT_001"
# Most fields live deep inside `geo.description.*` — use IDE introspection
# or fetch the JSON schema for the full nested structure.
```

## Common pitfalls

- `description` is the only required top-level field but it has *many* deeply
  nested required sub-fields (citation, identification info, etc.). Validation
  will surface these in `ValidationError.errors()`.
- Spatial reference system fields (`reference_system_info`) follow ISO 19115
  conventions — EPSG codes go in `reference_system_identifier.code`, not at the
  top level.
- This file generates 80+ Pydantic classes. When refactoring `templates.py`
  for geospatial, expect deep recursion through `Optional[List[X]]` types and
  rely on `is_optional_list` / `get_subtype_of_optional_or_list` from
  `metadataschemas.utils.utils`.
- Excel writes use `write_across_many_sheets` — round-tripping a populated
  geospatial object produces a multi-sheet workbook.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Source JSON: <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/geospatial-schema.json>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
