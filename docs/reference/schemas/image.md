# `image` schema reference

| Property | Value |
|---|---|
| **Canonical name** | `image` |
| **API alias** | `image` |
| **Pydantic class** | `metadataschemas.image_schema.ImageDataTypeSchema` |
| **Source JSON schema** | [`schemas/image-schema.json`](https://github.com/tonyfujs/metadata-schemas/blob/main/schemas/image-schema.json) |
| **Excel template** | `excel_sheets/Image_metadata.xlsx` |
| **Excel layout** | Multiple sheets (`write_across_many_sheets`) |
| **Schema version** | 0.1.0 |

## What this schema describes

Metadata for individual images (photos, scanned documents, illustrations).
Based on the [IPTC Photo Metadata Standard](http://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata)
plus a small set of project/repository fields. The schema references
`iptc-pmd-schema.json` and `iptc-phovidmdshared-schema.json` for the IPTC
fields themselves.

## Top-level fields

| Field | Type | Notes |
|---|---|---|
| `repositoryid` | `str` | Abbreviation for the collection that owns the image |
| `published` | `int` | `0` = draft, `1` = published |
| `overwrite` | `str` | `"yes"` / `"no"` — whether to overwrite an existing record |
| `metadata_information` | `object` | Metadata about the metadata record |
| `image_description` | `object` | The IPTC-derived image description (creator, dates, location, copyright, etc.) |
| `provenance` | `array` | Provenance entries |
| `tags` | `array` | User-defined tags |
| `additional` | `object` | Free-form bag |

## Required fields

None at the top level. (IPTC standard sub-fields have their own constraints
inside `image_description`.)

## How to create an instance

```python
from metadataschemas.metadata_manager import MetadataManager

mm = MetadataManager()
img = mm.create_metadata_outline("image")
img.repositoryid = "WB_PHOTO"
img.image_description.iptc.photo_video_metadata_iptc.title = "Field worker, Phnom Penh, 2024"
```

## Common pitfalls

- The `image_description` block follows IPTC nesting conventions — fields like
  title, creator, and copyright live several levels deep, mirroring the IPTC
  PhotoMetadata Standard structure.
- `published` is an `int` (0/1), not a `bool`. Pydantic will not coerce
  `True`/`False` automatically without setup.
- Image and video share `iptc-phovidmdshared-schema.json` for common fields —
  bug fixes there affect both schemas.

## See also

- Main skill: [`../skill.md`](../skill.md)
- Source JSON: <https://raw.githubusercontent.com/tonyfujs/metadata-schemas/main/schemas/image-schema.json>
- IPTC Photo Metadata Standard: <https://iptc.org/standards/photo-metadata/>
- Live docs: <https://worldbank.github.io/metadata-schemas/>
