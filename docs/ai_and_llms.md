# AI & LLMs

pyMetadataEditor ships three purpose-built files to make it easy for AI assistants — and for humans who are briefing them — to work with the package without having to click through the whole documentation site.

| File | Audience | When to use it |
|------|----------|----------------|
| **Agent skill** (`docs/skill.md`) | An AI agent or developer who needs a compact, architecturally-organised reference | Drop into a Claude / ChatGPT / Cursor system prompt, or hand to a coding-agent harness |
| **`llms.txt`** | Any LLM that can follow the [llms.txt spec](https://llmstxt.org/) | Point the LLM at the site root — it will retrieve the pages it needs on demand |
| **`llms-full.txt`** | An LLM with a large context window that prefers a single paste | Copy into the prompt when you want the whole documentation set available up front |

All three are regenerated automatically by ``python make_docs.py``; open an issue if anything gets out of date with the source.

---

## Agent skill — `docs/skill.md`

The [agent skill](skill.md) is a hand-authored guide that packages everything an AI assistant needs to be useful on this codebase: package purpose, architecture diagram, capability map, supported output modes, end-to-end workflow examples (including user onboarding and error handling), and pointers into every other doc. It is far denser than the user guide and is the single best starting point for an agent.

- **Browse it on the site:** [skill.md](skill.md)
- **Copy it into a prompt:** download or curl the raw file —
  ```bash
  curl -L https://raw.githubusercontent.com/tonyfujs/pymetadataeditor/DEV/docs/skill.md
  ```
- **Size:** roughly one page of context; safe to include verbatim in a system prompt.

---

## `llms.txt` — site map for LLMs

`llms.txt` follows the [llms.txt spec](https://llmstxt.org/). It lives at the **root of the deployed site** (standard convention), plus in the repo root for people cloning the source:

- Served: [/llms.txt](llms.txt)
- In the repo: [`llms.txt` at the repo root](https://github.com/tonyfujs/pymetadataeditor/blob/DEV/llms.txt)

Structure:

- An H1 with the project name and a blockquote summarising the package.
- Short intro paragraphs describing conventions (output modes, exception hierarchy).
- Grouped H2 sections — *Start here*, *User guide*, *How-to recipes*, *Reference*, *Developer reference*, *Schema reference*, *Optional* — each listing doc pages as bullet links with one-line descriptions.

Intended use: an LLM or agent tool loads `llms.txt`, parses the section structure, then follows the individual links only when needed. This keeps token usage low while still letting the model reach the full docs.

---

## `llms-full.txt` — single-shot documentation bundle

`llms-full.txt` is one big concatenation of every user-facing doc on the site (≈7,400 lines). Use it when you want to paste the whole documentation set into a large-context LLM prompt in a single shot:

- Served: [/llms-full.txt](llms-full.txt)
- In the repo: [`llms-full.txt` at the repo root](https://github.com/tonyfujs/pymetadataeditor/blob/DEV/llms-full.txt)

Each included page is delimited by a marker of the form `===== docs/<path> =====` so splitters and retrieval-augmented setups can rebuild the individual files if needed.

---

## Regenerating the AI assets

All three are rebuilt from the live `docs/` tree by a single command:

```bash
python make_docs.py
```

Under the hood:

- `build_llms_txt()` builds the spec-compliant site map.
- `build_llms_full_txt()` concatenates the docs in reading order.
- Both write simultaneously to the repo root (for contributors cloning the source) and to `docs/` (so MkDocs serves them at `/llms.txt` and `/llms-full.txt`).

If you add a new page, remember to add it to the ordered lists in `make_docs.py` (`LLMS_TXT_SECTIONS` and `LLMS_FULL_ORDER`) before regenerating.

---

## Using the assets with popular tools

- **Claude / ChatGPT / Gemini web UIs:** paste `docs/skill.md` into a Project / custom-GPT / system instructions field for every conversation, and attach `llms-full.txt` to a specific chat when you need deep context on a particular feature.
- **Claude Code / Cursor / Aider and other coding agents:** commit `docs/skill.md` alongside `CLAUDE.md` — the agents will pick it up automatically. Point the agent at `llms.txt` if you want it to fetch individual pages on demand.
- **Retrieval pipelines:** ingest `llms-full.txt`, split on `===== docs/<path> =====` markers, and index each chunk with its source path for attribution.
