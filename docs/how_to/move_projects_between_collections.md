# How-To: Move Projects Between Collections

This guide shows how to move a filtered subset of projects from one collection to another — for example, extracting all indicator projects from a mixed collection into a dedicated one.

---

## Setup

```python
from pymetadataeditor import MetadataEditor
import os

me = MetadataEditor(
    api_url=os.getenv("METADATA_API_URL"),
    api_key=os.getenv("METADATA_API_KEY"),
)

source_collection_id = 17
```

## Steps

```python
# Step 1: Create a new destination collection
new_collection_id = me.create_collection(
    title="My Indicators Collection",
    description="Indicators moved from the mixed source collection.",
)

# Step 2: List all projects in the source collection
projects_df = me.list_projects_in_collection(
    collection=source_collection_id,
    limit="All",
)

# Step 3: Filter for the type you want to move
indicator_projects = projects_df[projects_df["type"] == "timeseries"]
project_ids = indicator_projects.index.tolist()

# Step 4: Add those projects to the new collection
me.add_projects_to_collection(
    collection=new_collection_id,
    id_format="id",
    projects=project_ids,
)

# Step 5: Remove them from the source collection
me.remove_projects_from_collection(
    collection=source_collection_id,
    id_format="id",
    projects=project_ids,
)

print(f"Moved {len(project_ids)} projects to collection {new_collection_id}.")
```

!!! note "Type names in the listing"
    The `type` column in `list_projects_in_collection()` uses internal API names. Indicators are stored as `"timeseries"`, microdata as `"survey"`. See [Metadata Types](../reference/metadata_types.md) for the full mapping table.
