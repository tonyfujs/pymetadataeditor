from typing import Annotated, Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, Union, get_args, get_origin

import pandas as pd
from metadataschemas.utils.utils import is_list_annotation, is_optional_annotation, is_optional_list
from pydantic import BaseModel, Field

_VALID_SORT_BY: Tuple[str, ...] = ("title_asc", "title_desc", "updated_asc", "updated_desc")


def paginate_all_pages(
    fetch_page: Callable[[int, int], pd.DataFrame],
    offset: int = 0,
    page_size: int = 500,
    *,
    ignore_index: bool = False,
) -> pd.DataFrame:
    """Fetch successive pages from ``fetch_page`` until a short page is returned, then concatenate.

    The supplied callable must accept ``(offset, page_size)`` and return the corresponding page as a
    ``pd.DataFrame``. Iteration stops as soon as a page shorter than ``page_size`` comes back.

    Args:
        fetch_page: Callable invoked as ``fetch_page(offset, page_size)`` for each page.
        offset: Starting offset for the first page. Defaults to 0.
        page_size: Page size requested from ``fetch_page`` on each call. Defaults to 500.
        ignore_index: If True, the concatenated DataFrame is re-indexed (matches
            ``pd.concat(..., ignore_index=True)``). Defaults to False.

    Returns:
        pd.DataFrame: The concatenated pages, or an empty ``pd.DataFrame`` if no rows were returned.
    """
    current_offset = offset
    pages: List[pd.DataFrame] = []
    while True:
        page = fetch_page(current_offset, page_size)
        pages.append(page)
        if len(page) < page_size:
            break
        current_offset += page_size
    non_empty = [page for page in pages if len(page) > 0]
    if not non_empty:
        return pd.DataFrame()
    return pd.concat(non_empty, ignore_index=ignore_index)


def format_keywords(keywords: Optional[Union[str, Iterable[str]]]) -> Optional[str]:
    """Format a keyword filter value for the Metadata Editor API.

    Iterables (other than strings) are joined with ``%``. Whitespace inside the resulting string is
    also replaced with ``%``. ``None`` passes through unchanged.

    Args:
        keywords: A keyword string, an iterable of keyword strings, or ``None``.

    Returns:
        The formatted keyword string, or ``None`` if ``keywords`` is ``None``.
    """
    if keywords is None:
        return None
    if not isinstance(keywords, str) and isinstance(keywords, Iterable):
        keywords = "%".join(keywords)
    return keywords.replace(" ", "%")


def validate_sort_by(sort_by: Optional[str]) -> Optional[str]:
    """Lowercase and validate a ``sort_by`` value against the supported set.

    Args:
        sort_by: One of ``title_asc``, ``title_desc``, ``updated_asc``, ``updated_desc`` (case-insensitive),
            or ``None``.

    Returns:
        The lowercased sort value, or ``None`` if ``sort_by`` is ``None``.

    Raises:
        ValueError: If ``sort_by`` is provided but not one of the supported values.
    """
    if sort_by is None:
        return None
    normalized = sort_by.lower()
    if normalized not in _VALID_SORT_BY:
        raise ValueError(f"sort_by must be one of {list(_VALID_SORT_BY)}, got {sort_by!r}")
    return normalized


def validate_json_patches(patches):
    """Validates a list of JSON patches according to the JSON Patch specification.

    Args:
        patches (list): A list of JSON patch dictionaries.

    Returns:
        list: The validated patches with corrected paths if necessary.

    Raises:
        ValueError: If a patch is invalid or contains an error.
    """
    valid_ops = {"add", "remove", "replace", "move", "copy", "test"}
    validated_patches = []

    for patch in patches:
        if not isinstance(patch, dict):
            raise ValueError(f"Invalid patch format: {patch}. Each patch must be a dictionary.")

        op = patch.get("op")
        path = patch.get("path")

        if op not in valid_ops:
            raise ValueError(f"Invalid operation '{op}'. Valid operations are {valid_ops}.")

        if not isinstance(path, str):
            raise ValueError(f"Invalid path: {path}. Path must be a string.")

        if not path.startswith("/"):
            path = "/" + path

        # Additional checks for specific operations
        if op in {"add", "replace", "test"} and "value" not in patch:
            raise ValueError(f"Operation '{op}' requires a 'value' field.")

        if op in {"move", "copy"} and "from" not in patch:
            raise ValueError(f"Operation '{op}' requires a 'from' field.")

        validated_patches.append({**patch, "path": path})

    return validated_patches


def remove_empty_from_dict(old_dict: Dict) -> Dict:
    """Helper function for removing entries from dictionaries that look like:
    [{'name': ''}]
    """
    new_dict = {}
    for k, v in old_dict.items():
        if v is None:
            continue
        if isinstance(v, str):
            if v != "":
                new_dict[k] = v
        elif isinstance(v, dict):
            new_sub_dict = remove_empty_from_dict(v)
            if len(new_sub_dict) > 0:
                new_dict[k] = new_sub_dict
        elif isinstance(v, list):
            new_list = remove_empty_from_list(v)
            if len(new_list) > 0:
                new_dict[k] = new_list
        else:
            new_dict[k] = v
    return new_dict


def remove_empty_from_list(v):
    new_list = []
    for elem in v:
        if elem is None:
            continue
        elif isinstance(elem, dict):
            new_elem = remove_empty_from_dict(elem)
            if len(new_elem) > 0:
                new_list.append(new_elem)
        elif isinstance(elem, str):
            if elem != "":
                new_list.append(elem)
        elif isinstance(elem, list):
            new_elem = remove_empty_from_list(elem)
            if len(new_elem) > 0:
                new_list.append(new_elem)
        else:
            new_list.append(elem)
    return new_list


# def strip_model_rules(original_model: Type[BaseModel]) -> Type[BaseModel]:
#     """
#     Create a copy of a Pydantic model class (and its nested models) with validation rules stripped,
#     but retaining titles and descriptions.
#     """
#     # Process fields
#     stripped_fields = {}
#     annotations = {}

#     for name, field in original_model.model_fields.items():
#         annotation = field.annotation
#         default_value = field.default

#         # Prepare metadata to retain title and description
#         extra_kwargs = {}
#         if field.title:
#             extra_kwargs["title"] = field.title
#         if field.description:
#             extra_kwargs["description"] = field.description

#         # Check if the annotation refers to another Pydantic model
#         if isinstance(annotation, type) and issubclass(annotation, BaseModel):
#             # Recursively process the nested model
#             stripped_sub_model = strip_model_rules(annotation)
#             stripped_fields[name] = (
#                 stripped_sub_model,
#                 Field(default=default_value, **extra_kwargs),
#             )
#         # Handle lists of models
#         elif get_origin(annotation) is list or get_origin(annotation) is List:
#             item_type = get_args(annotation)[0]
#             if isinstance(item_type, type) and issubclass(item_type, BaseModel):
#                 # Recursively process the nested model
#                 stripped_item_type = strip_model_rules(item_type)
#                 stripped_fields[name] = (
#                     List[stripped_item_type],
#                     Field(default=default_value, **extra_kwargs),
#                 )
#             else:
#                 # Leave other types untouched
#                 stripped_fields[name] = (annotation, Field(default=default_value, **extra_kwargs))
#         else:
#             # For non-model fields, just copy the type, default value, and metadata
#             stripped_fields[name] = (annotation, Field(default=default_value, **extra_kwargs))

#         # Update annotations
#         annotations[name] = stripped_fields[name][0]

#     # Create the new stripped model
#     new_model = type(
#         f"{original_model.__name__}",
#         (SchemaBaseModel,),
#         {"__annotations__": annotations, **{name: field[1] for name, field in stripped_fields.items()}},
#     )

#     return new_model


def strip_constraints_from_annotated(annotation: Any) -> Any:
    """Strip constraints from Annotated types, Optional, List, and combinations,
    while preserving the base type.
    """
    # # Handle Annotated types, e.g., Annotated[str, constr(min_length=1)]
    # if get_origin(annotation) is Annotated:
    #     base_type = get_args(annotation)[0]
    #     return base_type

    # # Handle Optional (Union[Type, None])
    # if get_origin(annotation) is Union:
    #     args = get_args(annotation)
    #     if NoneType in args:
    #         # Get the other type in Union and return it
    #         other_type = [arg for arg in args if arg is not None][0]
    #         return strip_constraints_from_annotated(other_type)

    # # Handle List and List of models
    # if get_origin(annotation) is List:
    #     item_type = get_args(annotation)[0]
    #     return List[strip_constraints_from_annotated(item_type)]

    if is_optional_list(annotation):
        inner_annotation = get_args(get_args(annotation)[0])[0]
        if get_origin(inner_annotation) is Annotated:
            return Optional[List[get_args(inner_annotation)[0]]]
    elif is_optional_annotation(annotation):
        inner_annotation = get_args(annotation)[0]
        if get_origin(inner_annotation) is Annotated:
            return Optional[get_args(inner_annotation)[0]]
    elif is_list_annotation(annotation):
        inner_annotation = get_args(annotation)[0]
        if get_origin(inner_annotation) is Annotated:
            return List[get_args(inner_annotation)[0]]
    elif get_origin(annotation) is Annotated:
        return get_args(annotation)[0]

    # If it's not a generic type or Annotated, return the original annotation
    return annotation


def strip_model_rules(original_model: Type[BaseModel]) -> Type[BaseModel]:
    """Create a copy of a Pydantic model class (and its nested models) with validation rules stripped,
    but retaining titles and descriptions. Handles Annotated types like StringConstraints.
    """
    stripped_fields = {}
    annotations = {}

    for name, field in original_model.model_fields.items():
        annotation = field.annotation
        default_value = field.default

        # Prepare metadata to retain title and description
        extra_kwargs = {}
        if field.title:
            extra_kwargs["title"] = field.title
        if field.description:
            extra_kwargs["description"] = field.description

        # Handle Annotated types (e.g., Annotated[str, StringConstraints])
        annotation = strip_constraints_from_annotated(annotation)

        # Check if the annotation refers to another Pydantic model
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            # Recursively process the nested model
            stripped_sub_model = strip_model_rules(annotation)
            stripped_fields[name] = (
                stripped_sub_model,
                Field(default=default_value, **extra_kwargs),
            )
        # Handle lists of models
        elif get_origin(annotation) is list or get_origin(annotation) is List:
            item_type = get_args(annotation)[0]
            if isinstance(item_type, type) and issubclass(item_type, BaseModel):
                # Recursively process the nested model
                stripped_item_type = strip_model_rules(item_type)
                stripped_fields[name] = (
                    List[stripped_item_type],
                    Field(default=default_value, **extra_kwargs),
                )
            else:
                # Leave other types untouched
                stripped_fields[name] = (annotation, Field(default=default_value, **extra_kwargs))
        # Handle Union types with Annotated or nested models
        elif get_origin(annotation) is Union:
            stripped_union_args = tuple(
                strip_constraints_from_annotated(arg) if isinstance(arg, type) else arg for arg in get_args(annotation)
            )
            stripped_fields[name] = (
                Union[stripped_union_args],
                Field(default=default_value, **extra_kwargs),
            )
        else:
            # For non-model fields, just copy the type, default value, and metadata
            stripped_fields[name] = (annotation, Field(default=default_value, **extra_kwargs))

        # Update annotations
        annotations[name] = stripped_fields[name][0]

    # Create the new stripped model
    new_model = type(
        f"{original_model.__name__}",
        (BaseModel,),
        {"__annotations__": annotations, **{name: field[1] for name, field in stripped_fields.items()}},
    )

    return new_model
