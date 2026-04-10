# `table` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `table` |
| **API alias** | `table` |
| **Pydantic class** | `metadataschemas.table_schema.Model` |
| **Source JSON schema** | [`schemas/table-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/table-schema.json) |
| **Excel template** | `excel_sheets/Table_metadata.xlsx` |
| **Excel layout** | Multiple sheets (`write_across_many_sheets`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for **published statistical tables** — pre-computed cross-tabs,
statistical bulletins, summary tables. Distinct from `microdata` (unit-record
data) and `indicator` (single time series) — `table` is for fully aggregated
tabular outputs that are published as a unit.

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `repositoryid` | `str` | Abbreviation for the collection that owns the table |
| `published` | `int` | `0` = draft, `1` = published |
| `overwrite` | `str` | `"yes"` / `"no"` |
| `metadata_information` | `object` | Metadata about the metadata record |
| `table_description` | `object` | The table itself — title, statement of responsibility, dates, geographic coverage, methodology, table structure |
| `provenance` | `array` | Provenance entries |
| `tags` | `array` | User-defined tags |
| `additional` | `object` | Free-form bag |

## Required fields

None at the top level. Populate `table_description.title_statement.idno` and
`table_description.title_statement.title` for a useful record.

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
tbl = mm.create_metadata_outline("table")
tbl.repositoryid = "WB_TABLES"
tbl.table_description.title_statement.idno = "POVERTY_CAMBODIA_2024"
tbl.table_description.title_statement.title = "Poverty rates by province, Cambodia 2024"
```

## Common pitfalls

- The pydantic class is `Model`, not `TableSchema`. Always import as
  `from metadataschemas import table_schema` and reference `table_schema.Model`.
- Don't confuse `table` with `microdata` — `table` describes a *published
  cross-tab*, not a tabular dataset of unit records.
- Don't confuse `table` with `indicator` — `table` is a multi-dimensional
  table published as a unit, `indicator` is a single time series.
- `table_schema.py` defines ~40 classes for nested structure (statement of
  responsibility, methodology, table layout). Use IDE introspection rather
  than guessing field names.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Source JSON: <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/table-schema.json>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
