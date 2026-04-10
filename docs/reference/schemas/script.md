# `script` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `script` |
| **API alias** | `script` |
| **Pydantic class** | `metadataschemas.script_schema.ResearchProjectSchemaDraft` |
| **Source JSON schema** | [`schemas/script-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/script-schema.json) |
| **Excel template** | `excel_sheets/Script_metadata.xlsx` |
| **Excel layout** | Multiple sheets (`write_across_many_sheets`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for **research projects and data analysis scripts** — reproducible
research artefacts: code repositories, processing pipelines, analytical
workflows. Captures the project description, methodology, software/language
dependencies, inputs, and outputs. The pydantic class name
`ResearchProjectSchemaDraft` reflects the broader research-project framing.

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `repositoryid` | `str` | Abbreviation for the collection that owns the project |
| `published` | `int` | `0` = draft, `1` = published |
| `overwrite` | `str` | `"yes"` / `"no"` |
| `doc_desc` | `object` | Document description — about the metadata record itself (idno, producer, prod_date) |
| `project_desc` | `object` | The research project description — title, abstract, authors, software, code repository, inputs, outputs, methodology |
| `provenance` | `array` | Provenance entries |
| `tags` | `array` | User-defined tags |
| `additional` | `object` | Free-form bag |

## Required fields

None at the top level. In practice, populate `project_desc.title_statement.idno`
and `project_desc.title_statement.title` to make the record useful.

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
proj = mm.create_metadata_outline("script")
proj.repositoryid = "WB_RESEARCH"
proj.project_desc.title_statement.idno = "WB_GROWTH_2024"
proj.project_desc.title_statement.title = "Growth analysis pipeline"
```

## Common pitfalls

- The pydantic class name is `ResearchProjectSchemaDraft`, not `ScriptSchema`.
  Don't confuse it with `document_schema.ScriptSchemaDraft` — that one is for
  *documents*, despite its misleading name. They are two distinct types in two
  distinct modules:
  - `script_schema.ResearchProjectSchemaDraft` ← scripts/research projects
  - `document_schema.ScriptSchemaDraft` ← documents
- The "script" framing is narrow but the actual schema covers research
  projects more broadly (methodology, software dependencies, code locations).
- `doc_desc` and `project_desc` are both objects — `doc_desc` is metadata
  *about* the metadata record, `project_desc` is metadata *about* the project.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Document schema (also named `*ScriptSchemaDraft*`): [`document.md`](document.md)
- Source JSON: <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/script-schema.json>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
