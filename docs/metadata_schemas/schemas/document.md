# `document` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `document` |
| **API alias** | `document` |
| **Pydantic class** | `metadataschemas.document_schema.ScriptSchemaDraft` |
| **Source JSON schema** | [`schemas/document-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/document-schema.json) |
| **Excel template** | `excel_sheets/Document_metadata.xlsx` |
| **Excel layout** | Multiple sheets (`write_across_many_sheets`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for documents and publications — reports, working papers, books,
articles. The pydantic class is named `ScriptSchemaDraft` (an artifact of how
the schema was originally drafted) but it represents documents, not scripts.
The script type lives in `script_schema.ResearchProjectSchemaDraft`.

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `idno` | `str` | Project unique identifier |
| `metadata_information` | `object` | Metadata about the metadata record (producer, prod_date, version) |
| `document_description` | `object` | **Required.** The actual document description (title, authors, abstract, dates, language, etc.) |
| `provenance` | `array` | Provenance entries describing where this metadata came from |
| `tags` | `array` | User-defined tags (objects with `tag` and `tag_group`) |
| `additional` | `object` | Free-form bag for fields not covered by the schema |

## Required fields

- `document_description`

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
doc = mm.create_metadata_outline("document")
doc.document_description.title_statement.idno = "WB_REPORT_2024_001"
doc.document_description.title_statement.title = "Example report"
```

## Common pitfalls

- The class name `ScriptSchemaDraft` is misleading — it documents *documents*,
  not scripts. Don't confuse it with `script_schema.ResearchProjectSchemaDraft`.
- The `idno` at the root level is the project identifier; the document's own
  identifier lives at `document_description.title_statement.idno`. Both should
  usually be set to the same value.
- `document_description` is the only required top-level field — everything
  else can be omitted at validation time.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Source JSON: <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/document-schema.json>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
