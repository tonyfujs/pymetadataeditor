# Managing Admin Metadata

Admin metadata is a separate layer of structured information that can be attached to a project — distinct from the project's own descriptive metadata. It is designed for institutional or administrative data (workflows, approval statuses, internal notes, etc.) that live outside the project schema.

Key differences from project metadata:

| | Project metadata | Admin metadata |
|---|---|---|
| Schema source | Project template | Admin metadata template |
| Keyed by | Project ID | Project ID **+** template UID |
| One or many per project | One | Many (one per template) |
| Output formats | dict / pydantic / Excel | dict only |
| Template registry | `list_templates()` | `list_admin_metadata_templates()` |

---

## Discover available templates

Before reading or writing admin metadata, find out which admin templates exist on your instance:

```python
me = MetadataEditor(api_url=api_url, api_key=api_key)

templates = me.list_admin_metadata_templates()
print(templates[["uid", "name"]])
```

To inspect a specific template in detail:

```python
template = me.get_admin_metadata_template_by_uid("my_admin_template")
print(template["name"])
print(template["schema"])   # the field definitions
```

Raises `TemplateError` if the UID does not exist or access is denied.

---

## Read admin metadata

### Get a single record

Retrieve the admin metadata attached to a specific project under a specific template:

```python
record = me.get_admin_metadata(project_id=1042, template_uid="my_admin_template")
print(record["metadata"])
```

Raises `ValueError` if no record exists for the given `(project_id, template_uid)` pair.

### List records

`list_admin_metadata()` returns a DataFrame of records across all projects. All parameters are optional:

```python
# All records, all projects
all_records = me.list_admin_metadata()

# Filter by project
project_records = me.list_admin_metadata(project_id=1042)

# Filter by template
template_records = me.list_admin_metadata(template_uid="my_admin_template")

# Filter by multiple templates
multi_template = me.list_admin_metadata(template_uid=["tpl_a", "tpl_b"])

# Filter by date range (ISO 8601 strings)
recent = me.list_admin_metadata(date_from="2024-01-01", date_to="2024-12-31")

# Manual pagination
page = me.list_admin_metadata(limit=50, offset=100)
```

By default `limit="All"` — the method automatically pages through the API in batches of 500 and returns a single concatenated DataFrame.

---

## Create or update admin metadata

Use `upsert_admin_metadata()` to create or fully replace a record. If a record already exists for the `(project_id, template_uid)` pair it is replaced; otherwise a new record is created:

```python
me.upsert_admin_metadata(
    project_id=1042,
    template_uid="my_admin_template",
    metadata={
        "status": "approved",
        "reviewer": "Jane Smith",
        "review_date": "2024-06-15",
        "notes": "Reviewed and approved for publication.",
    },
)
```

!!! note
    `upsert_admin_metadata` accepts a plain `dict` only — Pydantic models and Excel are not supported for admin metadata.

Empty values are stripped automatically before sending to the API. Raises `ValueError` if `metadata` is not a dict or `template_uid` is empty.

---

## Partial updates (JSON Patch)

To update individual fields without replacing the entire record, use `patch_admin_metadata()`. This applies one or more [RFC 6902 JSON Patch](https://datatracker.ietf.org/doc/html/rfc6902) operations:

```python
me.patch_admin_metadata(
    project_id=1042,
    template_uid="my_admin_template",
    patches=[
        {"op": "replace", "path": "/status", "value": "published"},
        {"op": "replace", "path": "/review_date", "value": "2024-07-01"},
    ],
)
```

Supported operations: `add`, `remove`, `replace`, `test`. Paths that do not start with `/` have it prepended automatically.

Raises `ValueError` if `patches` is empty or contains an invalid operation.

---

## Delete admin metadata

```python
me.delete_admin_metadata(project_id=1042, template_uid="my_admin_template")
```

Raises `DeleteNotAppliedError` if the record still exists after the delete request.

---

## End-to-end example

```python
from pymetadataeditor import MetadataEditor

me = MetadataEditor(api_url="https://your-instance.org/index.php/api", api_key="YOUR_KEY")

# 1. Discover what admin templates are available
templates = me.list_admin_metadata_templates()
print(templates[["uid", "name"]])
# uid              name
# review_workflow  Review Workflow
# ...

template_uid = "review_workflow"
project_id = 1042

# 2. Attach admin metadata to a project
me.upsert_admin_metadata(
    project_id=project_id,
    template_uid=template_uid,
    metadata={"status": "draft", "assignee": "John Doe"},
)

# 3. Read it back
record = me.get_admin_metadata(project_id=project_id, template_uid=template_uid)
print(record["metadata"]["status"])   # "draft"

# 4. Move to review via patch
me.patch_admin_metadata(
    project_id=project_id,
    template_uid=template_uid,
    patches=[{"op": "replace", "path": "/status", "value": "under_review"}],
)

# 5. List all records for this project
all_records = me.list_admin_metadata(project_id=project_id)
print(all_records[["template_uid", "metadata"]])

# 6. Clean up
me.delete_admin_metadata(project_id=project_id, template_uid=template_uid)
```
