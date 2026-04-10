# Module: `llm_helpers.py`

**Location:** `pymetadataeditor/llm_helpers.py`

## Overview

Helper functions for LLM-powered automatic metadata generation. This module provides the core logic for querying an LLM (OpenAI or compatible) to generate and validate structured metadata, converting source files to text, and processing LLM responses into validated Pydantic models.

These functions are called by `interface.py` via `draft_metadata_from_files()` and `augment_metadata_from_files()`. Users do not call these directly.

---

## Dependencies

| Dependency | Purpose |
|-----------|---------|
| `openai` | API client for GPT-4o (or compatible models) |
| `tiktoken` | Token counting to stay within LLM context limits |
| `markitdown` | Converts source files (PDF, Word, Excel, etc.) to Markdown text |
| `metadataschemas` | Provides `make_skeleton()`, type utilities for Pydantic model introspection |
| `tqdm` | Progress bar display during field-by-field LLM querying |
| `pydantic` | Model validation and structured output parsing |

---

## Function Reference

### `call_per_field(klass, client, model, messages, show_progress_bar) -> BaseModel`

```python
def call_per_field(
    klass: type[BaseModel],
    client,                          # OpenAI or AzureOpenAI client instance
    model: str,                      # e.g. "gpt-4o" or "llama3.1"
    messages: list[dict[str, str]],  # System + user messages for the LLM
    show_progress_bar: bool = False,
) -> BaseModel
```

Queries the LLM field by field across the top-level fields of a Pydantic model, then assembles and validates the results. Used when a single large call is too expensive or the model is less capable.

**Behavior:**
1. Iterates over each field of `klass`
2. For each field, calls `client.beta.chat.completions.parse()` with `response_format` restricted to that single field (structured output)
3. On `APITimeoutError`, skips the field
4. On `ValidationError` (e.g., field is a complex nested type), recursively calls itself on the sub-type
5. Merges all field responses into a final dict and validates via `_iterated_validated_update_to_outline()`

**Returns:** A validated `BaseModel` instance with all successfully extracted fields populated.

**LLM requirement:** The model must support structured output / response format (OpenAI `beta.chat.completions.parse`). GPT-4o and compatible models work; some local models may not.

---

### `_iterated_validated_update_to_outline(model_def, updates, verbose) -> BaseModel`

```python
def _iterated_validated_update_to_outline(
    model_def: type[BaseModel],
    updates: dict,
    verbose: bool = False,
) -> BaseModel
```

Safely applies a dictionary of updates to a metadata model skeleton, validating each field update individually. If a field value fails Pydantic validation, the original skeleton value is retained rather than raising an error.

**Behavior:**
1. Creates a skeleton of `model_def` via `make_skeleton(model_def).model_dump()`
2. Iterates over `updates` dict
3. For each key/value pair:
   - Resolves the field annotation (unwraps `Optional`, `List`)
   - If the value is a dict and the field is a nested `BaseModel`, recursively calls itself
   - If the value is a list of dicts and the field is `List[BaseModel]`, recursively processes each item
   - Attempts to apply the candidate value to the model
   - On `ValidationError`, reverts to the skeleton's original value
4. Returns the final validated model instance

**Returns:** `BaseModel` — validated instance with as many fields populated as possible.

**Used by:** `call_per_field()` and `interface.py` → `draft_metadata_from_files()` / `augment_metadata_from_files()`

---

### `_prepend_draft_drop_non_str(d, prefix) -> dict | list | str | None`

```python
def _prepend_draft_drop_non_str(
    d: Any,
    prefix: str,
) -> dict | list | str | None
```

Recursively walks a dict/list/string structure and:
- Prepends `prefix` to every non-empty string value
- Drops empty strings and non-string values (including numbers, booleans, None)
- Returns `None` if the result would be empty

**Used for:** Augmenting existing metadata — the prefix (e.g., `"<AI>"`) marks which fields were added by the LLM vs. which were pre-existing. Called by `augment_metadata_from_files()`.

```python
result = _prepend_draft_drop_non_str({"title": "My Study", "year": 2020}, prefix="<AI> ")
# Returns: {"title": "<AI> My Study"}  (year dropped as non-string)
```

---

### `get_date_as_text() -> str`

```python
def get_date_as_text() -> str
```

Returns the current date as a human-readable string with ordinal suffix (e.g., `"March 27th, 2026"`). Used in LLM system prompts to provide temporal context for metadata production date fields.

---

### `json_to_markdown(data, level) -> str`

```python
def json_to_markdown(data, level: int = 1) -> str
```

Converts a JSON object (dict, list, or primitive) to a Markdown string. Nested dicts become headings, lists become bullet points, and primitives are rendered as text.

**Used for:** Converting structured metadata context into Markdown before including it in LLM prompts, making it easier for the LLM to reference.

---

## Supported File Formats

Source files passed to `draft_metadata_from_files()` are converted to Markdown text using `markitdown`:

| Format | Notes |
|--------|-------|
| PDF | Text extracted from PDF pages |
| Word (`.docx`) | Full document text |
| Excel (`.xlsx`, `.xls`) | Sheet content as text |
| PowerPoint (`.pptx`) | Slide text |
| Text (`.txt`) | Read directly |
| CSV | Tabular data as text |
| XML | Structured text |
| ZIP | Contents extracted and processed |
| Images (`.jpg`, `.png`, etc.) | Described via OpenAI vision |
| Audio | Transcribed via OpenAI |
| HTML / URLs | Web content fetched and converted |

---

## Token Handling

Token counting uses `tiktoken` with the specified tokenizer model (default: `"o200k_base"`, corresponding to GPT-4o).

- Files are read and their token counts are accumulated
- If total tokens exceed `max_tokens` (default: `128_000`), a warning is printed and the content is truncated
- The token count is printed per file as files are read in

---

## LLM Configuration

| Parameter | Default | Notes |
|-----------|---------|-------|
| `llm_model_name` | `"gpt-4o"` | Must support structured output (response format) |
| `tokenizer_model` | `"o200k_base"` | Should match the LLM model's tokenizer |
| `max_tokens` | `128_000` | Context window limit |
| `llm_base_url` | `None` | Set for Azure OpenAI or local models (e.g., Ollama) |
| `azure_deployment_name` | `None` | Required when using Azure OpenAI |

**Standard OpenAI:**
```python
client = OpenAI(api_key=llm_api_key)
```

**Azure OpenAI:**
```python
client = AzureOpenAI(
    api_key=llm_api_key,
    azure_endpoint=llm_base_url,
    azure_deployment=azure_deployment_name,
    api_version="2024-08-01-preview",
)
```

**Local model (e.g., Ollama):**
```python
client = OpenAI(api_key=llm_api_key, base_url=llm_base_url)
```

---

## Integration Points

These functions are not called directly by users. They are invoked via:

- `MetadataEditor.draft_metadata_from_files()` → calls `_iterated_validated_update_to_outline()` with full-context LLM response, or `call_per_field()` for field-by-field mode
- `MetadataEditor.augment_metadata_from_files()` → same as above, plus calls `_prepend_draft_drop_non_str()` to prefix LLM-added content

See [`interface.md`](interface.md) for the full signatures of these public methods.
