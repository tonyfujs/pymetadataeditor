# `video` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `video` |
| **API alias** | `video` |
| **Pydantic class** | `metadataschemas.video_schema.Model` |
| **Source JSON schema** | [`schemas/video-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/video-schema.json) |
| **Excel template** | `excel_sheets/Video_metadata.xlsx` |
| **Excel layout** | Single sheet (`write_to_single_sheet`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for video files. Based on Dublin Core elements and Schema.org's
[`VideoObject`](https://schema.org/VideoObject) type. Smaller than the image
schema (~21 pydantic classes), with a flat-ish description block.

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `repositoryid` | `str` | Abbreviation for the collection that owns the video |
| `published` | `int` | `0` = draft, `1` = published |
| `overwrite` | `str` | `"yes"` / `"no"` |
| `metadata_information` | `object` | Metadata about the metadata record |
| `video_description` | `object` | **Required.** Title, creator, date, description, content URL, duration, encoding, language, etc. (Dublin Core / VideoObject fields) |
| `provenance` | `array` | Provenance entries |
| `tags` | `array` | User-defined tags |
| `additional` | `object` | Free-form bag |

## Required fields

- `video_description`

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
vid = mm.create_metadata_outline("video")
vid.repositoryid = "WB_VIDEO"
vid.video_description.idno = "WB_INTERVIEW_2024_001"
vid.video_description.title = "Field interview, Phnom Penh, 2024"
```

## Common pitfalls

- The pydantic class is `Model`, not `VideoSchema`. Import as
  `from metadataschemas import video_schema` and reference `video_schema.Model`.
- Excel layout is a *single* sheet — round-tripping uses
  `excel_single_sheet_to_pydantic`. The image schema, by contrast, uses
  multiple sheets.
- The video and image schemas share `iptc-phovidmdshared-schema.json` for
  some common fields. Bug fixes there affect both.
- `video_description.contentUrl` (note camelCase from schema.org) holds the
  playable video URL — don't put it in `filename`.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Source JSON: <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/video-schema.json>
- Schema.org VideoObject: <https://schema.org/VideoObject>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
