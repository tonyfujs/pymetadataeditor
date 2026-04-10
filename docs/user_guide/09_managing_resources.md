# Managing Resources

Resources are supporting documents attached to a project — things like questionnaires, field manuals, data tables, reports, or syntax files. Each resource has its own title, type, and optionally an uploaded file.

---

## List resources for a project

```python
resources = me.get_resources_by_id(project_id=1042)
print(resources[["id", "dctype", "title", "filename"]])
```

The `dctype` column indicates the resource type (see below for valid values).

---

## Attach a resource

Use `log_resource()` to register a new resource. Only `project_id`, `dctype`, and `title` are required; all other parameters are optional.

```python
resource_id = me.log_resource(
    project_id=1042,
    dctype="doc/qst",          # questionnaire
    title="Main Questionnaire",
    author="Data Collection Team",
    dcdate="2024-01-15",
    description="The primary household questionnaire used in the survey.",
    filename="questionnaire.pdf",   # optional file upload
)
```

### Common resource types (`dctype`)

| `dctype` | Description |
|---------|-------------|
| `"doc/qst"` | Questionnaire |
| `"doc/rpt"` | Report |
| `"doc/tec"` | Technical document |
| `"doc/ref"` | Reference document |
| `"dat/micro"` | Microdata |
| `"dat/agg"` | Aggregate data / table |
| `"prg"` | Program / syntax file |
| `"oth"` | Other |

---

## Update a resource

Update a resource's metadata or replace its uploaded file:

```python
me.update_resource(
    project_id=1042,
    resource_id=resource_id,
    dctype="doc/qst",
    title="Main Questionnaire (revised)",
    description="Updated questionnaire with corrected question wording.",
    filename="questionnaire_v2.pdf",   # replaces the existing file
)
```

---

## Delete a resource

```python
me.delete_resource_by_id(project_id=1042, resource_id=resource_id)
```
