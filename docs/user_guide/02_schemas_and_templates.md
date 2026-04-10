# Schemas & Templates

Every metadata record in the Metadata Editor conforms to a **schema** — a structured definition of what fields exist and what values they accept. Schemas are delivered as **templates**, which can be the built-in defaults or custom variants configured per collection.

Understanding schemas and templates is key to creating valid metadata and interpreting existing records.

---

## Metadata types vs. templates

Every project has a **metadata type** (e.g. `indicator`, `microdata`, `document`) and a **template UID** (e.g. `IHSN_INDICATOR_1-0_Template_v01_EN`).

- The **type** defines the broad category of metadata.
- The **template** is a specific version or customization of the schema for that type.

Most users work with type names. Template UIDs are needed when you want to use a custom template or need to target a specific schema version.

---

## List available templates

```python
templates = me.list_templates()
print(templates[["uid", "name", "data_type"]].to_string())
```

The `uid` column is what you pass to methods that accept a `metadata_type_or_template_uid` argument.

---

## Get a specific template

```python
template = me.get_template_by_uid("IHSN_INDICATOR_1-0_Template_v01_EN")
print(template["name"])
print(template["data_type"])
```

---

## Get the Pydantic class for a type

`get_metadata_class()` returns the Python class that represents a metadata type's schema. This is useful for programmatic validation or introspection:

```python
IndicatorClass = me.get_metadata_class("indicator")

# Inspect fields
print(IndicatorClass.model_fields.keys())
```

---

## Explore a schema with an outline

The most practical way to explore a schema is to generate an empty outline. This creates an instance of the metadata structure with all fields present but empty:

=== "Pydantic model"

    ```python
    outline = me.make_metadata_outline("indicator", output_mode="pydantic")

    # Explore with tab-completion or introspection
    print(outline.series_description.model_fields.keys())
    ```

=== "Dictionary"

    ```python
    outline = me.make_metadata_outline("indicator", output_mode="dict")
    import json
    print(json.dumps(outline, indent=2, default=str))
    ```

=== "Excel file"

    ```python
    # Creates a formatted Excel file showing all fields
    filepath = me.make_metadata_outline(
        "indicator",
        output_mode="excel",
        filename="indicator_schema.xlsx",
    )
    ```

The Excel output is especially useful for sharing schema structure with non-technical collaborators.

---

## Using a custom template UID

Anywhere a method accepts `metadata_type_or_template_uid`, you can pass either a type name (`"indicator"`) or a specific template UID:

```python
# Using type name — uses the default template for that type
me.make_metadata_outline("indicator", output_mode="pydantic")

# Using a specific template UID
me.make_metadata_outline("IHSN_INDICATOR_1-0_Template_v01_EN", output_mode="pydantic")
```

---

## Set the default template for a collection

To ensure all projects in a collection use the same template:

```python
me.set_template_for_collection(
    collection_id=17,
    template_uid="IHSN_INDICATOR_1-0_Template_v01_EN",
)
```

---

## Delete a custom template

```python
me.delete_template(uid="MY_CUSTOM_TEMPLATE_v01")
```

This only works for custom (non-default) templates. Built-in templates cannot be deleted.

---

## Schema reference

Detailed field listings for every supported metadata type are in the [Schema Reference](../reference/schemas/microdata.md) section.
