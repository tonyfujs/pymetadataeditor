# Architecture Overview

This page is for developers who want to contribute to pyMetadataEditor or understand how the package is structured internally.

---

## Module map

```
User Code
    │
    ▼
MetadataEditor          (pymetadataeditor/interface.py)
    ├──► RequestsWithSpecificErrors  (requester.py)   ──► Metadata Editor API
    ├──► pydantic_from_template      (templates.py)   ◄── templates from API
    ├──► llm_helpers functions       (llm_helpers.py)  ──► OpenAI / LLM API
    └──► utils functions             (utils.py)
              │
              ▼
    Returns: Dict | Pydantic Model | Excel file path
```

---

## Module responsibilities

| Module | Role |
|--------|------|
| `interface.py` | The only public surface. All user-facing methods live here. 1,969 lines intentionally monolithic — do not split. |
| `requester.py` | All HTTP communication. Never use `requests` directly in `interface.py`. |
| `templates.py` | Resolves a template UID to a Pydantic class. Results are cached in `self._templates`. |
| `llm_helpers.py` | LLM call orchestration, file conversion, field-by-field querying. Called only by `draft_metadata_from_files()` and `augment_metadata_from_files()`. |
| `utils.py` | Pure stateless helpers: JSON Patch validation, empty-value cleaning, constraint stripping. No imports from other package modules except `metadataschemas`. |

---

## Key conventions

### Internal helpers

These stable internal methods are called by every public method — their signatures are contracts:

- `_process_metadata_input()` — normalizes dict/Pydantic/Excel input before posting
- `_process_metadata_output()` — converts raw API responses to the requested `output_mode`
- `_get_metadata_class_and_type_and_UID()` — resolves type name or template UID to a class
- `_get_template_class_and_type_and_UID()` — similar, used for template-specific operations

### Pydantic model modes

Two modes exist for Pydantic models:
- `apply_rules=True` — full validation (for user input)
- `apply_rules=False` — no constraints (for LLM structured output — OpenAI doesn't support constrained fields)

`strip_model_rules()` in `utils.py` handles stripping constraints while preserving structure.

### Caching

Template-derived Pydantic classes are expensive to build. They are cached in `self._templates` after first use. Preserve this cache when refactoring.

### Empty value handling

Call `remove_empty_from_dict()` on any dict before POSTing to the API. `interface.py` does this internally — do not do it again in calling code.

### Metadata type aliases

The API uses different type names internally. `interface.py` maps these before constructing API paths:

| User-facing | API name |
|-------------|---------|
| `indicator` | `timeseries` |
| `indicators_db` | `timeseries_db` |
| `microdata` | `survey` |

Always accept the user-facing names in public methods.

---

## Development setup

```bash
pip install poetry
poetry install --with dev
poetry run pre-commit install
```

### Running tests

```bash
# Unit tests (HTTP mocked)
poetry run pytest tests/test_interface.py

# Integration tests (requires live API)
API_KEY=your_key API_URL=https://your-instance.org/index.php/api poetry run pytest tests/integration_test.py
```

### Linting

```bash
poetry run ruff check pymetadataeditor/
poetry run ruff format pymetadataeditor/
```

---

## Adding a new feature

1. Read `docs/skill.md` and the relevant module docs for existing patterns
2. Add the method to `interface.py` — follow Google-style docstrings
3. Use `_process_metadata_output()` if the method returns metadata in multiple formats
4. Add unit tests in `tests/test_interface.py` using `MockResponse` for HTTP mocking
5. Update `docs/skill.md` and `docs/developer/modules/interface.md`
6. Run `poetry run mkdocs serve` to verify the docs build correctly
