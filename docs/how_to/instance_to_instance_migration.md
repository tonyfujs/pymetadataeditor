# How-To: Migrate Projects Between Instances

This guide shows how to copy projects from one Metadata Editor instance to another — for example, promoting records from a development environment to production.

!!! warning "Template requirement"
    This approach assumes that the **same templates exist in both instances** with identical UIDs. If templates differ between instances, the metadata fields may not map correctly.

---

## Setup

```python
from pymetadataeditor import MetadataEditor
import os

# Connect to the source (development) instance
me_dev = MetadataEditor(
    api_url=os.getenv("DEV_API_URL"),
    api_key=os.getenv("DEV_API_KEY"),
)

# Connect to the target (production) instance
me_prod = MetadataEditor(
    api_url=os.getenv("PROD_API_URL"),
    api_key=os.getenv("PROD_API_KEY"),
)

source_collection_id = 1
```

## Steps

```python
# Step 1: List the projects to migrate
projects_df = me_dev.list_projects_in_collection(
    collection=source_collection_id,
    limit="All",
)

uploaded_ids = []

# Step 2: For each project, fetch metadata from dev and post to prod
for project_id in projects_df.index:

    # Step 3: Download metadata from the dev instance as a dict
    metadata = me_dev.get_project_metadata_by_id(project_id, output_mode="dict")

    # Step 4: Create the record in the prod instance
    new_id = me_prod.create_project_log(
        metadata,
        metadata_type_or_template_uid=projects_df.loc[project_id, "type"],
    )
    uploaded_ids.append(new_id)
    print(f"Migrated project {project_id} → prod id {new_id}")

print(f"\nMigrated {len(uploaded_ids)} projects.")
```

---

## Migrating collection structure too

If you also want to recreate the collection in production:

```python
# Create the same collection in production
source_collection = me_dev.get_collection_by_id(source_collection_id)
prod_collection_id = me_prod.create_collection(
    title=source_collection["title"],
    description=source_collection.get("description", ""),
)

# Add the migrated projects to it
me_prod.add_projects_to_collection(
    collection=prod_collection_id,
    id_format="id",
    projects=uploaded_ids,
)
```

---

## Tips

- Use `output_mode="dict"` for migration (not Pydantic) — it avoids template class resolution issues when templates differ slightly between instances.
- Log `uploaded_ids` alongside the original `project_id` values so you can build a mapping from dev to prod ids.
- Run on a small batch first to verify the template UIDs match before migrating everything.
