# `indicators_db` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `indicators_db` |
| **API alias** | `timeseries_db` |
| **Pydantic class** | `metadataschemas.indicators_db_schema.TimeseriesDatabaseSchema` |
| **Source JSON schema** | [`schemas/timeseries-db-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/timeseries-db-schema.json) |
| **Excel template** | `excel_sheets/Indicators_db_metadata.xlsx` |
| **Excel layout** | Single sheet (`write_to_single_sheet`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for an *indicators database* (a collection that contains multiple
individual indicators / time series). Use this when documenting the umbrella
dataset (e.g. "World Development Indicators 2024"). For per-series metadata,
see [`indicator.md`](indicator.md).

## Aliases

`timeseries_db`, `indicator_db` → `indicators_db` (handled by
`MetadataManager.standardize_metadata_name`).

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `published` | `int` | `0` = draft, `1` = published |
| `overwrite` | `str` | `"yes"` / `"no"` — overwrite existing record? |
| `metadata_information` | `object` | Metadata about the metadata record |
| `database_description` | `object` | **Required.** The database itself — title, abbreviation, producer, version, time period covered, etc. |
| `provenance` | `array` | Provenance entries |
| `additional` | `object` | Free-form bag |

## Required fields

- `database_description`

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
db = mm.create_metadata_outline("indicators_db")
db.database_description.title_statement.idno = "WDI_2024"
db.database_description.title_statement.title = "World Development Indicators 2024"
```

## Common pitfalls

- The API endpoint name is `timeseries_db`, not `indicators_db`. The
  user-facing name is `indicators_db` (plural). Keep both in mind when
  constructing URLs vs. accepting input.
- Unlike the per-series `indicator` schema, this schema has **no `idno` at the
  root** — the identifier lives at `database_description.title_statement.idno`.
- Excel layout is a *single* sheet (unlike `indicator`, which uses multiple
  sheets). Reading round-trips through `excel_single_sheet_to_pydantic`.
- This schema has no `tags` field at the root — tagging is per-indicator, not
  per-database.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Per-series indicator: [`indicator.md`](indicator.md)
- Source JSON: <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/timeseries-db-schema.json>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
