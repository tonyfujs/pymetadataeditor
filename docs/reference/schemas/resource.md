# `resource` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `resource` |
| **API alias** | `resource` |
| **Pydantic class** | `metadataschemas.resource_schema.Model` |
| **Source JSON schema** | [`schemas/resource-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/resource-schema.json) |
| **Excel template** | `excel_sheets/Resource_metadata.xlsx` |
| **Excel layout** | Single sheet (`write_to_single_sheet`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for an *external resource* attached to any project — a downloadable
file, a URL, a related document. Far smaller and flatter than the other
schemas: a single object with Dublin Core-style fields. Used to attach
supporting materials (questionnaires, technical reports, codebooks) to
microdata or indicator projects.

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `dctype` | `str` | Document type, e.g. `doc/adm`, `doc/qst`, `tbl`, `map` (uses Dublin Core type vocabulary with project-specific extensions) |
| `dcformat` | `str` | MIME type, e.g. `application/zip`, `application/pdf` |
| `title` | `str` | **Required.** Resource title |
| `author` | `str` | Author |
| `dcdate` | `str` | Date associated with the resource |
| `country` | `str` | Country coverage |
| `language` | `str` | Language |
| `contributor` | `str` | Contributor |
| `publisher` | `str` | Publisher |
| `rights` | `str` | Rights statement |
| `description` | `str` | Description |
| `abstract` | `str` | Abstract |
| `toc` | `str` | Table of contents |
| `filename` | `str` | Resource file name or URL. For uploading a file, use the `file` field in form-data on the API call instead |

## Required fields

- `title`

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
res = mm.create_metadata_outline("resource")
res.title = "Cambodia LSMS+ 2019-20 Questionnaire"
res.dctype = "doc/qst"
res.dcformat = "application/pdf"
res.filename = "https://example.org/khm_2019_qst.pdf"
```

## Common pitfalls

- The pydantic class is just `Model` (not `ResourceSchema`). When importing
  directly, use `from metadataschemas import resource_schema` and reference
  `resource_schema.Model`.
- All fields are flat strings — there is no nested structure. This is the
  simplest schema in the package.
- For uploads, the `filename` field holds the file *name or URL*; the actual
  binary upload uses a separate `file` form-data field on the API request.
  Don't try to base64-encode files into `filename`.
- Excel layout is a *single* sheet — round-tripping uses
  `excel_single_sheet_to_pydantic`.
- `dctype` uses a controlled vocabulary mixing Dublin Core types and
  project-specific codes. See the schema's `enum` for the full list.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Source JSON: <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/resource-schema.json>
- Dublin Core type vocabulary: <https://www.dublincore.org/specifications/dublin-core/dcmi-type-vocabulary/>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
