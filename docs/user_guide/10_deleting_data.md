# Deleting Data

This section covers deleting projects, collections, resources, and templates.

!!! warning "Deletions are permanent"
    There is no undo. Verify you have the correct id before calling any delete method.
    System administrators may restrict deletion rights — if a delete is blocked by the system, a `DeleteNotAppliedError` is raised.

---

## Delete a project

```python
me.delete_project_by_id(id=1042)
```

This deletes the project's metadata record. It does not automatically remove it from any collections it belongs to.

---

## Delete a collection

```python
me.delete_collection_by_id(id=17)
```

Deleting a collection removes the collection itself. The projects it contained are not deleted — they remain accessible outside the collection.

---

## Delete a resource

```python
me.delete_resource_by_id(project_id=1042, resource_id=55)
```

---

## Delete a custom template

```python
me.delete_template(uid="MY_CUSTOM_TEMPLATE_v01")
```

Only custom (non-default) templates can be deleted.

---

## Handling `DeleteNotAppliedError`

If the system's admin settings block a deletion, a `DeleteNotAppliedError` is raised instead of silently failing:

```python
from pymetadataeditor import DeleteNotAppliedError

try:
    me.delete_project_by_id(id=1042)
except DeleteNotAppliedError as e:
    print(f"Deletion was not applied: {e}")
    # Investigate permissions or contact your system administrator
```

See [Error Handling](../reference/error_handling.md) for more detail.
