# `microdata` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `microdata` |
| **API alias** | `survey` |
| **Pydantic class** | `metadataschemas.microdata_schema.MicrodataSchema` |
| **Source JSON schema** | [`schemas/microdata-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/microdata-schema.json) (composes [`schemas/ddi-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/ddi-schema.json)) |
| **Excel template** | `excel_sheets/Microdata_metadata.xlsx` |
| **Excel layout** | Multiple sheets (`write_across_many_sheets`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for survey microdata — household surveys, censuses, and similar
unit-record datasets. Built on the **DDI Codebook 2.5** standard. The pydantic
class hierarchy is the largest in the package (~70 classes in
`microdata_schema.py`).

## Aliases

`survey`, `survey_microdata` → `microdata` (handled by
`MetadataManager.standardize_metadata_name`).

## Top-level structure

`microdata-schema.json` is composed via `allOf` of three parts:

1. **Project wrapper** — adds `repositoryid`, `access_policy`, `published`,
   `overwrite`
2. **DDI body** (`$ref: ddi-schema.json`) — `doc_desc`, `study_desc`,
   `data_files`, `variables`, `variable_groups`
3. **Project tail** — `provenance`, `tags`, `additional`

The flattened set of top-level fields on `MicrodataSchema`:

| Field | Source | Notes |
|---|---|---|
| `repositoryid` | wrapper | Collection that owns the survey |
| `access_policy` | wrapper | One of `direct`, `open`, `public`, `licensed`, `remote`, `data_na` |
| `published` | wrapper | `0` = draft, `1` = published |
| `overwrite` | wrapper | `"yes"` / `"no"` |
| `doc_desc` | DDI | Document description (about the metadata record itself) |
| `study_desc` | DDI | **Where the survey lives.** Title, IDs, producers, sponsors, methodology, scope, geographic coverage, version |
| `data_files` | DDI | Array of data file descriptions |
| `variables` | DDI | Array of variable definitions |
| `variable_groups` | DDI | Array of variable groupings |
| `provenance` | tail | Provenance entries |
| `tags` | tail | User-defined tags |
| `additional` | tail | Free-form bag |

## Required fields

None enforced at the top level by the JSON schema (the `allOf` composition
hides this), but in practice every record must populate at least
`study_desc.title_statement.idno` and `study_desc.title_statement.title`.

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
md = mm.create_metadata_outline("microdata")
md.repositoryid = "WB_LSMS"
md.study_desc.title_statement.idno = "KHM_2019_LSMS+_v01_EN"
md.study_desc.title_statement.title = "Cambodia LSMS+ 2019-20"
md.access_policy = "licensed"
```

## Common pitfalls

- **Use DDI terminology, not flat names.** The main identifier is
  `study_desc.title_statement.idno`, not `idno` at the root. The title is
  `study_desc.title_statement.title`. The producers are
  `study_desc.title_statement.producers`.
- The API endpoint name is `survey`, not `microdata`. `interface.py` already
  maps this — preserve the mapping.
- `access_policy` is an enum: `direct`, `open`, `public`, `licensed`,
  `remote`, `data_na`. Don't pass arbitrary strings.
- `variables` and `variable_groups` are arrays of full variable descriptions,
  not just names — populating them by hand is rarely the right approach. Use
  the metadata editor UI or LLM helpers for bulk variable metadata.
- Because `microdata-schema.json` uses `allOf` with a `$ref` to
  `ddi-schema.json`, naive top-level introspection of the JSON will return
  zero properties. Always read both files together.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Source JSON (microdata wrapper): <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/microdata-schema.json>
- Source JSON (DDI body): <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/ddi-schema.json>
- DDI Codebook 2.5: <https://ddialliance.org/Specification/DDI-Codebook/2.5/>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
