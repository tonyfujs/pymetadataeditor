# CLAUDE.md — pyMetadataEditor

This file provides context for Claude agents working on this codebase. Read this first, then consult the skill and module docs linked below for deeper understanding.

---

## Package Purpose

`pymetadataeditor` (v0.4.0) is a Python client library for the [Metadata Editor](https://github.com/mah0001/metadata-editor) REST API. It manages structured metadata for research datasets across seven data types (microdata, indicators, geospatial, documents, scripts, images, videos), provides LLM-powered automatic metadata generation, and adds admin-metadata CRUD, user lookup, and collection permission management on top of the core project workflow.

The package is used by data curators at institutions such as the World Bank Group.

---

## Agent Skill Reference

For a comprehensive understanding of the package's capabilities, architecture, and common workflows, start here:

- **[docs/skill.md](docs/skill.md)** — Main skill file: package overview, architecture diagram, all capabilities, output formats, common workflows, and pointers to module docs

Per-module deep dives (referenced from `skill.md`):

| Module doc | Source file | What it covers |
|-----------|------------|----------------|
| [docs/modules/interface.md](docs/modules/interface.md) | `pymetadataeditor/interface.py` | All public `MetadataEditor` methods — full signatures, params, return types, examples |
| [docs/modules/requester.md](docs/modules/requester.md) | `pymetadataeditor/requester.py` | HTTP layer, auth, error handling, SSL configuration |
| [docs/modules/templates.md](docs/modules/templates.md) | `pymetadataeditor/templates.py` | Template-to-Pydantic conversion, field types, constraint parsing |
| [docs/modules/llm_helpers.md](docs/modules/llm_helpers.md) | `pymetadataeditor/llm_helpers.py` | LLM call orchestration, file conversion, validation logic |
| [docs/modules/utils.md](docs/modules/utils.md) | `pymetadataeditor/utils.py` | JSON Patch validation, empty-value cleaning, constraint stripping |

Schema reference — for any work touching metadata schemas (new metadata type, schema validation, Excel round-trips, pydantic model generation, debugging field types), consult the dedicated schema skill. It documents the sibling [`tonyfujs/metadata-schemas`](https://github.com/tonyfujs/metadata-schemas) repo that supplies every `*Schema` class used by this package:

- **[docs/metadata_schemas/skill.md](docs/metadata_schemas/skill.md)** — Overview of the `metadataschemas` package: supported types, public API (`MetadataManager`, `SchemaBaseModel`, shared utilities), where pymetadataeditor already integrates, versioning workflow, things to never do, and pointers to per-schema reference files.

Per-schema reference files (one per supported metadata type — top-level fields, required fields, common pitfalls, instantiation examples):

| Schema | Reference |
|---|---|
| `document` | [docs/metadata_schemas/schemas/document.md](docs/metadata_schemas/schemas/document.md) |
| `geospatial` | [docs/metadata_schemas/schemas/geospatial.md](docs/metadata_schemas/schemas/geospatial.md) |
| `image` | [docs/metadata_schemas/schemas/image.md](docs/metadata_schemas/schemas/image.md) |
| `indicator` | [docs/metadata_schemas/schemas/indicator.md](docs/metadata_schemas/schemas/indicator.md) |
| `indicators_db` | [docs/metadata_schemas/schemas/indicators_db.md](docs/metadata_schemas/schemas/indicators_db.md) |
| `microdata` | [docs/metadata_schemas/schemas/microdata.md](docs/metadata_schemas/schemas/microdata.md) |
| `resource` | [docs/metadata_schemas/schemas/resource.md](docs/metadata_schemas/schemas/resource.md) |
| `script` | [docs/metadata_schemas/schemas/script.md](docs/metadata_schemas/schemas/script.md) |
| `table` | [docs/metadata_schemas/schemas/table.md](docs/metadata_schemas/schemas/table.md) |
| `video` | [docs/metadata_schemas/schemas/video.md](docs/metadata_schemas/schemas/video.md) |

Auto-generated API reference and user-facing docs:

The package has a full MkDocs + Material site in `docs/` (built with `mkdocs build`, deployed via GitHub Actions). Key pages:

| Doc | Description |
|----|-------------|
| [docs/index.md](docs/index.md) | Site landing page |
| [docs/getting_started.md](docs/getting_started.md) | End-to-end first workflow |
| [docs/user_guide/](docs/user_guide/) | 13 pages — one per functional area (includes `12_managing_admin_metadata.md`, `13_users_and_permissions.md`) |
| [docs/how_to/](docs/how_to/) | Recipes: batch upload, collection moves, instance migration |
| [docs/reference/api.md](docs/reference/api.md) | mkdocstrings-generated reference; always current with docstrings |
| [docs/reference/error_handling.md](docs/reference/error_handling.md) | Full exception hierarchy and handling patterns |
| [docs/reference/output_modes.md](docs/reference/output_modes.md) | Dict / Pydantic / Excel output formats |
| [docs/reference/metadata_types.md](docs/reference/metadata_types.md) | Supported metadata types and API aliases |
| [docs/reference/schemas/](docs/reference/schemas/) | Per-type schema references |
| [docs/developer/architecture.md](docs/developer/architecture.md) | Internal architecture |
| [docs/developer/modules/](docs/developer/modules/) | Deep-dive per-module reference (site-served copies of the skill module docs) |
| [docs/examples.md](docs/examples.md) | Worked examples: batch upload, collection migration, instance-to-instance transfer |
| [docs/using_automated_metadata_creation.md](docs/using_automated_metadata_creation.md) | LLM metadata generation guide |
| [docs/ai_and_llms.md](docs/ai_and_llms.md) | AI & LLMs landing page — explains the skill, `llms.txt`, and `llms-full.txt` for users |
| [llms.txt](llms.txt) / [llms-full.txt](llms-full.txt) | llms.txt-spec summary + single-file concatenation for LLM ingestion (also copied into `docs/` so the MkDocs site serves them at `/llms.txt` and `/llms-full.txt`) |

---

## Repository Layout

```
pymetadataeditor/
├── pymetadataeditor/       # Package source
│   ├── __init__.py         # Exports MetadataEditor + the HTTP exception hierarchy
│   ├── interface.py        # MetadataEditor class — the only public API (~2500 lines)
│   ├── llm_helpers.py      # LLM utilities (~260 lines)
│   ├── requester.py        # HTTP layer + exception translation (~320 lines)
│   ├── templates.py        # Template-to-Pydantic conversion (~680 lines)
│   └── utils.py            # Shared utilities (~260 lines)
├── tests/
│   ├── test_interface.py   # Unit tests with mocked HTTP (primary test suite)
│   ├── template_checks.py  # Template warning diagnostics (not a pytest suite)
│   └── integration_test.py # Integration tests against a live API (requires env vars)
├── demo/                   # Jupyter notebooks (source for docs/demo.md etc.)
├── docs/                   # MkDocs site + agent skill
│   ├── index.md            # Site landing page
│   ├── getting_started.md
│   ├── user_guide/         # 13 per-topic user guides
│   ├── how_to/             # Multi-step recipes
│   ├── reference/          # Output modes, metadata types, error handling, API, schemas
│   ├── developer/          # Architecture + per-module deep dives
│   ├── skill.md            # Agent skill entry point ← start here
│   ├── modules/            # Legacy per-module docs (kept in sync with developer/modules/)
│   ├── examples.md         # Converted from demo/examples.ipynb
│   ├── demo.md             # Converted from demo/demo.ipynb
│   └── using_automated_metadata_creation.md
├── llms.txt                # llms.txt-spec summary of the docs site
├── llms-full.txt           # Single-file concatenation of all docs for LLM ingestion
├── mkdocs.yml              # MkDocs + Material + mkdocstrings config
├── make_docs.py            # Converts demo notebooks; run after updating demos
├── pyproject.toml          # Poetry config — Python ^3.11, dependencies, ruff config
└── .pre-commit-config.yaml # Hooks: detect-secrets + ruff lint + ruff format
```

---

## Development Setup

```bash
# Install all dependencies (including dev tools)
pip install poetry
poetry install --with dev

# Install pre-commit hooks (runs ruff and detect-secrets on every commit)
poetry run pre-commit install
```

**Python requirement:** 3.11 or later.

---

## Running Tests

```bash
# Unit tests only (no live API required — HTTP is mocked)
poetry run pytest tests/test_interface.py

# Integration tests (requires a live Metadata Editor API)
API_KEY=your_key API_URL=https://your-instance.org/index.php/api poetry run pytest tests/integration_test.py

# All tests
poetry run pytest
```

`tests/template_checks.py` is not a pytest suite — it is a diagnostic script for checking template warnings against a live API. Run it directly if investigating template schema mismatches.

---

## Code Quality

**Linter/formatter:** [Ruff](https://docs.astral.sh/ruff/) — configured in `pyproject.toml`.

| Setting | Value |
|---------|-------|
| Line length | 120 characters |
| Docstring style | Google |
| Selected rules | `I` (isort), `E`, `F`, `D` (pydocstyle) |
| Test files | `D103`, `D100` ignored (no docstrings required for test functions) |

Run manually:

```bash
poetry run ruff check pymetadataeditor/   # lint
poetry run ruff format pymetadataeditor/  # format
```

Pre-commit hooks run ruff automatically on every `git commit`. Do not use `--no-verify` to skip them.

**Secret detection:** `detect-secrets` runs as a pre-commit hook. Do not commit API keys or credentials.

---

## Regenerating Documentation

```bash
# Converts demo/*.ipynb to docs/*.md (no longer generates API_Reference.md — mkdocstrings does that live)
python make_docs.py

# Build the docs site locally (preview at http://127.0.0.1:8000)
poetry run mkdocs serve

# Build the static site into ./site/
poetry run mkdocs build
```

`docs/reference/api.md` is populated live by mkdocstrings from `pymetadataeditor/interface.py` docstrings — keep those docstrings current. Everything else in `docs/` is hand-authored:

- `docs/skill.md` — agent skill entry point
- `docs/user_guide/*` — per-topic guides
- `docs/how_to/*` — multi-step recipes
- `docs/reference/*` — output modes, metadata types, error handling, schemas
- `docs/developer/modules/*` — per-module reference (site-served copies; keep in sync with `docs/modules/*`)
- `llms.txt` and `llms-full.txt` — regenerate after any user-facing doc change so LLM consumers stay current

---

## Architecture & Key Conventions

### Module responsibilities

- **`interface.py`** is the only public surface. All user-facing work goes here. Other modules are internal helpers.
- **`requester.py`** handles all HTTP. Do not use `requests` directly in `interface.py` — go through `self._apinterface`.
- **`templates.py`** is called when resolving a template UID to a Pydantic class. The result is cached in `self._templates`.
- **`llm_helpers.py`** is called by `draft_metadata_from_files` and `augment_metadata_from_files` only. Keep LLM logic out of `interface.py`.
- **`utils.py`** contains pure, stateless helpers. No imports from other package modules except `metadataschemas`.

### Pydantic models

- Metadata schemas come from the external `metadataschemas` library (base schemas) and are extended by template-derived models built in `templates.py`.
- Two modes exist: with rules (`apply_rules=True`) for validation, and without rules (`apply_rules=False`) for LLM structured output (OpenAI doesn't support constrained Pydantic fields).
- `strip_model_rules()` in `utils.py` handles stripping constraints while preserving structure.

### Output modes

Every metadata method supports three output modes: `'dict'`, `'pydantic'`, `'excel'`. New methods that return metadata should follow the same pattern using `_process_metadata_output()`.

### Metadata type aliases

The API uses different type names internally. `interface.py` maps these before constructing API paths:

| User-facing | API endpoint name |
|-------------|-----------------|
| `indicator` | `timeseries` |
| `indicators_db` | `timeseries_db` |
| `microdata` | `survey` |

Always accept the user-facing names in public methods.

### Empty value handling

Call `remove_empty_from_dict()` on any dict before POSTing to the API. `interface.py` does this internally — do not do it again in calling code.

### Admin metadata

Admin metadata is a separate namespace from project metadata, with its own template registry (`/admin-metadata/templates`) and its own CRUD endpoints. It is **not** hooked into `list_templates()` or `self._templates`. Multi-op JSON Patch is supported on admin metadata but not (yet) on project metadata. Admin metadata records are keyed by `(project_id, template_uid)` pairs — a single project can have multiple admin metadata records, one per template.

### JSON Patch

`patch_update_project_log_by_id` applies a single RFC 6902 patch operation. Multi-patch is not exposed publicly (the API supports it but it is not yet surfaced). Paths are auto-corrected to start with `/`.

---

## Adding a New Feature

1. **Read** `docs/skill.md` and the relevant module docs to understand existing patterns.
2. **Add the method** to `interface.py` — follow the existing docstring format (Google style, full Args/Returns/Raises/Example sections).
3. **Use `_process_metadata_output()`** if the method returns metadata in multiple formats.
4. **Add unit tests** in `tests/test_interface.py` using `MockResponse` for HTTP mocking.
5. **Update `docs/skill.md`** — add the method to the appropriate capability group.
6. **Update both module doc copies** (`docs/modules/interface.md` and `docs/developer/modules/interface.md`).
7. **Add or update a user guide page** under `docs/user_guide/` when the feature is user-facing; add a recipe under `docs/how_to/` if it's multi-step.
8. **Regenerate `llms.txt` and `llms-full.txt`** so LLM consumers pick up the change.
9. **Build the site locally** with `poetry run mkdocs build --strict` to confirm nav and links still resolve.

## Refactoring Guidelines

- `interface.py` is large (~2500 lines) but intentionally monolithic — the public API is one class. Do not split it into multiple classes.
- Internal helpers (`_process_metadata_input`, `_process_metadata_output`, `_get_metadata_class_and_type_and_UID`, `_get_template_class_and_type_and_UID`) are stable contracts — their signatures affect every public method.
- The `metadataschemas` library is an external dependency managed separately. Do not copy its types into this package.
- Caching of template-derived Pydantic classes (`self._templates`) is intentional — template builds are expensive. Preserve the cache when refactoring.
- The HTTP exception hierarchy (`MetadataEditorAPIError` and its subclasses) lives in `requester.py` and is re-exported from `__init__.py`. Preserve `HTTPError` as an ancestor so existing `except HTTPError` handlers keep working.
