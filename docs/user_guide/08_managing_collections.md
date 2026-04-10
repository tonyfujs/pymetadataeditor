# Managing Collections

Collections are the primary way to organize projects in the Metadata Editor. A collection is a named group of projects — similar to a folder. Projects can belong to multiple collections, and collections can be nested within other collections.

---

## List collections

```python
collections = me.list_collections()
print(collections[["id", "title", "description"]])
```

---

## Get a single collection

```python
collection = me.get_collection_by_id(17)
print(collection["title"])
print(collection["description"])
```

---

## Create a collection

```python
new_id = me.create_collection(
    title="World Bank Poverty Indicators",
    description="A curated set of poverty-related indicators.",
)
print(f"Created collection with id: {new_id}")
```

---

## Update a collection

```python
me.update_collection(
    id=17,
    title="Updated Collection Title",
    description="Updated description.",
)
```

At least one of `title` or `description` must be provided.

---

## Add projects to a collection

Projects can be identified by their numeric `id` or their string `idno`:

```python
# Add a single project by id
me.add_projects_to_collection(
    collection=17,
    id_format="id",
    projects=1042,
)

# Add multiple projects by id
me.add_projects_to_collection(
    collection=17,
    id_format="id",
    projects=[1042, 1043, 1044],
)

# Add by idno
me.add_projects_to_collection(
    collection=17,
    id_format="idno",
    projects=["WB_NY.GDP.MKTP.CD", "WB_SP.POP.TOTL"],
)
```

### Add to multiple collections at once

```python
me.add_projects_to_collection(
    collection=[17, 21],
    id_format="id",
    projects=[1042, 1043],
)
```

---

## Remove projects from a collection

```python
me.remove_projects_from_collection(
    collection=17,
    id_format="id",
    projects=[1042, 1043],
)
```

This is non-destructive — it removes the project from the collection but does not delete the project itself. No error is raised if the project wasn't in the collection.

---

## Copy a collection

Copies all projects and users from one collection to another:

```python
me.copy_collection(source_id=17, target_id=21)
```

---

## Move a collection

Makes one collection a sub-collection of another:

```python
me.move_collection(source_id=17, target_id=5)
```

---

## Assign a default template to a collection

All new projects created in this collection will default to the specified template:

```python
me.set_template_for_collection(
    collection_id=17,
    template_uid="IHSN_INDICATOR_1-0_Template_v01_EN",
)
```

---

## Count and list projects in a collection

```python
count = me.count_projects_in_collection(collection=17)

projects_df = me.list_projects_in_collection(
    collection=17,
    limit=50,
    sort_by="title_asc",
)
```

---

## Delete a collection

```python
me.delete_collection_by_id(id=17)
```

Deleting a collection does not delete the projects it contains — they remain accessible outside the collection.
