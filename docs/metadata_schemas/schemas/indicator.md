# `indicator` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `indicator` |
| **API alias** | `timeseries` |
| **Pydantic class** | `metadataschemas.indicator_schema.TimeseriesSchema` |
| **Source JSON schema** | [`schemas/timeseries-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/timeseries-schema.json) |
| **Excel template** | `excel_sheets/Indicator_metadata.xlsx` |
| **Excel layout** | Multiple sheets (`write_across_many_sheets`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for individual time series / indicators (e.g. "GDP per capita,
Cambodia, 1990–2024"). Each instance describes one indicator series, including
its data structure, source, periodicity, and DataCite metadata for DOI
generation.

This is the per-series schema. For the database/collection that *contains*
many indicators, see [`indicators_db.md`](indicators_db.md).

## Aliases

`timeseries` → `indicator` (handled by
`MetadataManager.standardize_metadata_name`).

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `idno` | `str` | Project unique identifier |
| `metadata_information` | `object` | Information on the production of the metadata |
| `series_description` | `object` | **Required.** The series itself — name, definition, periodicity, units, time period, source, etc. |
| `data_structure` | `array` | Data structure definition entries |
| `data_notes` | `array` | Free-form notes about the data |
| `datacite` | `object` | DataCite metadata for generating a DOI |
| `provenance` | `array` | Provenance entries |
| `tags` | `array` | User-defined tags |
| `additional` | `object` | Free-form bag |

## Required fields

- `series_description`

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
ind = mm.create_metadata_outline("indicator")
ind.idno = "GDP_PC_KHM"
ind.series_description.idno = "GDP_PC_KHM"
ind.series_description.name = "GDP per capita, Cambodia"
ind.series_description.periodicity = "annual"
```

## Common pitfalls

- The API endpoint name is `timeseries`, not `indicator`. `interface.py` maps
  the canonical name to the API alias before constructing URLs — preserve
  that mapping if you add new methods.
- `idno` at the root and `series_description.idno` are different fields. They
  *should* match, but the schema does not enforce it.
- The `datacite` block is required for DOI generation but optional in the
  schema itself. If your method drafts DOIs, validate it explicitly.
- `data_structure` is an array of objects, not a single object — the data
  structure definition can have multiple components.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Indicators-database wrapper: [`indicators_db.md`](indicators_db.md)
- Source JSON: <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/timeseries-schema.json>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
