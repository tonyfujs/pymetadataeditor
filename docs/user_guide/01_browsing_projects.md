# Browsing & Discovering Projects

This section covers how to explore what's in your Metadata Editor instance: counting projects, listing them with filters and sorting, and fetching the details of a specific project.

---

## Count projects

Get the total number of projects your API key has access to:

```python
total = me.count_projects()
print(f"Total projects: {total}")
```

---

## List projects

`list_projects()` returns a pandas DataFrame with one row per project.

### Basic listing

```python
# Get the first 20 projects
me.list_projects(limit=20)
```

The DataFrame's **index** is the project's internal numeric `id`. Other columns typically include `type`, `idno`, `title`, and `created`.

### Retrieve all projects

Pass `limit="All"` to retrieve every project. The library paginates automatically in batches of 500:

```python
all_projects = me.list_projects(limit="All")
```

### Filter by metadata type

```python
# Only indicator (time series) projects
me.list_projects(limit=100, metadata_type="indicator")

# Other valid types: "microdata", "geospatial", "document", "script", "image", "video"
```

### Search by keyword

Keywords are matched against project titles and idnos:

```python
me.list_projects(limit=50, keywords="poverty")

# Multiple keywords — all must match
me.list_projects(limit=50, keywords=["poverty", "africa"])
```

### Sort results

```python
# Most recently updated first
me.list_projects(limit=20, sort_by="updated_desc")

# Alphabetically by title
me.list_projects(limit=20, sort_by="title_asc")
```

Valid `sort_by` values: `"title_asc"`, `"title_desc"`, `"updated_asc"`, `"updated_desc"`.

### Pagination

For large result sets, paginate manually using `offset`:

```python
# Page 1: records 0–49
page1 = me.list_projects(limit=50, offset=0)

# Page 2: records 50–99
page2 = me.list_projects(limit=50, offset=50)
```

---

## Get a single project

Retrieve full details about one project by its numeric `id`:

```python
project = me.get_project_by_id(1042)

print(project["title"])
print(project["type"])          # e.g. "indicator", "survey", "document"
print(project["idno"])          # human-readable identifier
print(project["template_uid"])  # the template used for this project's metadata
```

!!! tip "id vs idno"
    The `id` is the internal database integer (visible as the DataFrame index from `list_projects`).
    The `idno` is a human-readable string identifier like `"WB_NY.GDP.MKTP.CD"`. The API uses `id` for all operations.

---

## Browse projects in a collection

```python
# Count projects in collection 17
count = me.count_projects_in_collection(collection=17)

# List them, with optional keyword and sort filtering
me.list_projects_in_collection(
    collection=17,
    limit=50,
    keywords="survey",
    sort_by="title_asc",
)
```

See [Managing Collections](08_managing_collections.md) for how to work with collections.
