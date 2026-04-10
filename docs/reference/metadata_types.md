# Metadata Types

pyMetadataEditor supports ten metadata types. Each type has a user-facing name (what you pass to library methods) and an internal API name (what the Metadata Editor API uses). The library handles this mapping automatically.

---

## Type reference

| User-facing name | API name | Description |
|-----------------|----------|-------------|
| `microdata` | `survey` | Household surveys, censuses, and other microdata studies |
| `indicator` | `timeseries` | Individual time series indicators (e.g. GDP, poverty rates) |
| `indicators_db` | `timeseries_db` | Databases or collections of indicators |
| `geospatial` | `geospatial` | Geographic and spatial datasets |
| `document` | `document` | Reports, publications, books, working papers |
| `script` | `script` | Data processing and analysis scripts |
| `image` | `image` | Images and photographs |
| `video` | `video` | Videos and multimedia content |
| `table` | `table` | Statistical tables |
| `resource` | `resource` | General resources |

Always use the **user-facing name** when calling library methods. Never use the internal API name directly.

---

## Using type names in method calls

Any method that accepts a `metadata_type_or_template_uid` parameter accepts type names:

```python
# Creating an outline
me.make_metadata_outline("indicator", output_mode="pydantic")
me.make_metadata_outline("microdata", output_mode="pydantic")

# Filtering a project list
me.list_projects(limit=100, metadata_type="indicator")

# AI-powered generation
me.draft_metadata_from_files(
    llm_api_key=...,
    files=["report.pdf"],
    metadata_type_or_template_uid="document",
    output_mode="pydantic",
)
```

---

## Detecting the type of an existing project

The `type` column in `list_projects()` and `list_projects_in_collection()` returns the **internal API name**. Use the table above to map back to the user-facing name:

```python
projects = me.list_projects(limit=50)

# The "type" column contains API names like "timeseries", "survey"
print(projects["type"].value_counts())
```

When calling `get_project_by_id()`, the `type` field also uses the internal API name.

---

## AI-supported types

Only a subset of types are currently supported by `draft_metadata_from_files()` and `augment_metadata_from_files()`:

`microdata`, `geospatial`, `indicator`, `document`, `script`, `video`

---

## Schema reference

Detailed field listings for each type are in the schema reference pages:

- [Document](schemas/document.md)
- [Geospatial](schemas/geospatial.md)
- [Image](schemas/image.md)
- [Indicator](schemas/indicator.md)
- [Indicators DB](schemas/indicators_db.md)
- [Microdata](schemas/microdata.md)
- [Resource](schemas/resource.md)
- [Script](schemas/script.md)
- [Table](schemas/table.md)
- [Video](schemas/video.md)
