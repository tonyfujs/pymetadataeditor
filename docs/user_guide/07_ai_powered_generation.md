# AI-Powered Metadata Generation

pyMetadataEditor can use a Large Language Model (LLM) to automatically draft or augment metadata from source files and web pages. This can dramatically reduce the time needed to create high-quality metadata records.

---

## Supported metadata types

AI-powered generation works for:
`microdata`, `geospatial`, `indicator`, `document`, `script`, `video`

---

## Supported source formats

The LLM can read from:

| Format | Notes |
|--------|-------|
| PDF | Text extracted and sent to the LLM |
| Word (`.docx`) | |
| Excel (`.xlsx`) | |
| PowerPoint (`.pptx`) | |
| Plain text (`.txt`) | |
| CSV | |
| JSON | |
| XML | |
| ZIP archive | Contents extracted and processed |
| Images (PNG, JPG, etc.) | Described by the LLM vision capability |
| Web URLs | Page content fetched and read |

---

## Draft metadata from scratch

`draft_metadata_from_files()` reads your source files and produces a complete first draft:

```python
import os

draft = me.draft_metadata_from_files(
    llm_api_key=os.getenv("OPENAI_API_KEY"),
    files=["survey_manual.pdf", "survey_report.pdf"],
    metadata_type_or_template_uid="microdata",
    output_mode="pydantic",
    metadata_producer_organization="My Organization",
)

draft.pretty_print()
```

The library logs progress as it reads each file:

```
Read in survey_manual.pdf, running token count is 6381
Read in survey_report.pdf, running token count is 24910
Sending to OpenAI, this may take a few minutes...
```

Once you're happy with the draft, log it to the database:

```python
new_id = me.create_project_log(draft)
```

### From a web URL

Pass a URL directly in the `files` list:

```python
draft = me.draft_metadata_from_files(
    llm_api_key=os.getenv("OPENAI_API_KEY"),
    files=["https://data.worldbank.org/indicator/NY.GDP.MKTP.CD"],
    metadata_type_or_template_uid="indicator",
    output_mode="pydantic",
)
```

### Output format

The `output_mode` parameter works the same way as all other metadata methods — `"pydantic"`, `"dict"`, or `"excel"`.

---

## Augment existing metadata

`augment_metadata_from_files()` takes an existing metadata object and enriches it using information from additional files:

```python
# Fetch existing metadata
existing = me.get_project_metadata_by_id(2202, output_mode="pydantic")

# Augment from a source document
augmented = me.augment_metadata_from_files(
    input_metadata=existing,
    llm_api_key=os.getenv("OPENAI_API_KEY"),
    files=["https://example.org/report.pdf"],
    output_mode="pydantic",
    metadata_producer_organization="My Organization",
    prefix="<AI>",   # optional: marks AI-generated fields
)
```

The `prefix` parameter prepends a marker to any string field that the LLM filled in, making it easy to review and approve AI-generated content before saving.

---

## LLM model selection

By default the library uses `gpt-4o` via OpenAI. You can specify a different model:

```python
draft = me.draft_metadata_from_files(
    llm_api_key=os.getenv("OPENAI_API_KEY"),
    files=["report.pdf"],
    metadata_type_or_template_uid="document",
    output_mode="pydantic",
    llm_model_name="gpt-4-turbo",   # override default model
)
```

---

## Privacy options

### Run locally with Ollama

For fully private inference, run an open-source model on your own machine via [Ollama](https://ollama.com/):

```bash
# Install Ollama, then pull and serve a model
ollama pull llama3.1
ollama serve llama3.1
```

```python
draft = me.draft_metadata_from_files(
    llm_api_key="ollama",
    files=["report.pdf"],
    metadata_type_or_template_uid="document",
    output_mode="pydantic",
    llm_base_url="http://localhost:11434/v1",
    llm_model_name="llama3.1",
)
```

!!! note
    Locally-run models are typically less capable than large cloud models like GPT-4o. Expect lower quality metadata from smaller local models.

### Azure OpenAI

If your organization runs an LLM via Azure AI Services:

```python
augmented = me.augment_metadata_from_files(
    input_metadata=existing,
    llm_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    files=["report.pdf"],
    output_mode="pydantic",
    azure_deployment_name="your-deployment-name",
    llm_base_url="https://{your-resource-name}.openai.azure.com",
)
```

---

## Token management

Very large files may exceed the model's context window. The library counts tokens as it reads files:

```
Read in large_report.pdf, running token count is 78,432
```

If you hit limits, consider splitting large PDFs into smaller sections before passing them.

The default token limit is 128,000 (`max_tokens=128_000`). You can lower this to stay within cheaper model tiers:

```python
draft = me.draft_metadata_from_files(
    llm_api_key=os.getenv("OPENAI_API_KEY"),
    files=["report.pdf"],
    metadata_type_or_template_uid="document",
    output_mode="pydantic",
    max_tokens=32_000,
)
```
