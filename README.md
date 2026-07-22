# code-learn-skill

A pair of agent skills focused on making code understandable. One turns a technical concept into staged, runnable learning code split element by element; the other turns your source code — one file or many — into a single self-contained, annotated HTML walkthrough. Both are reading aids: they help you understand code, whether you're learning a concept from scratch or making sense of an existing codebase.

## 📑 Table of Contents

- [✨ Skills](#-skills)
- [🚀 Quick Start](#-quick-start)
- [🎓 staged-learning-code](#-staged-learning-code)
- [📖 code-walkthrough](#-code-walkthrough)
- [🗂️ Repository Structure](#-repository-structure)
- [📄 License](#-license)

## ✨ Skills

| Skill | What it does | Trigger phrases (examples) |
|---|---|---|
| **`staged-learning-code`** | Decomposes a technical concept (agent harness, RAG, compiler, network protocol, …) into elements and generates staged learning material — minimal code split one element per folder, each folder runnable on its own. | "make learning code", "teaching material I can study in stages", "implement it split by element" |
| **`code-walkthrough`** | Splits source code into processing units and generates a self-contained HTML that embeds the **full code**, per-unit commentary, SVG diagrams, and a glossary panel. Multiple files are combined into a single HTML with tabs. | "explain this code", "make a walkthrough", "create a code-explanation HTML" |

Both are [Agent Skills](https://agentskills.io) — a `SKILL.md` with `name` / `description` front matter plus body, with detailed specs separated into `reference/`. Each skill produces its output in the language of your request.

## 🔗 How the two skills fit together

The skills can be chained: turn a concept into runnable learning code, then turn that code into a single readable HTML.

```
Technology you want to learn (e.g. an agent harness)
        │
        ▼   ① staged-learning-code skill
        │      Turns the topic into "learning code you can build and run"
   ┌────────────────────────────────────────────────┐
   │ Staged material (one folder per element)        │  ← each folder runs on its own
   └────────────────────────────────────────────────┘
        │
        ▼   ② code-walkthrough skill
        │      Turns the material into "one HTML you can read and understand"
   ┌────────────────────────────────────────────────┐
   │ A single explanatory HTML                       │  ← all files as tabs / code + commentary + glossary
   └────────────────────────────────────────────────┘
        │
        ▼
   Open in a browser
```

## 🚀 Quick Start

Clone the repo and copy the skills into your skills directory (`~/.claude/skills/` for Claude Code; use your tool's equivalent):

```bash
git clone https://github.com/yumeiriowl/code-learn-skill.git
cp -r code-learn-skill/skills/* ~/.claude/skills/
```

Restart your agent tool, then invoke them (Claude Code slash-command style shown):

```bash
/staged-learning-code <technical concept>
/code-walkthrough path/to/source.py
```

## 🎓 staged-learning-code

Given a technical concept, the skill researches up-to-date information about it (skipping textbook-level basics), then generates minimal code split **one element per folder**. The split granularity is left to the model, following the natural decomposition of the subject. Dependencies are removed as far as possible — the LLM, DB, and external APIs are **stubbed** so every folder runs offline with a single command (e.g. `python main.py`). Only the final integrated folder wires up a real LLM / DB / external API.

The generated code deliberately optimizes for **human readability over reuse**. It follows YAGNI and KISS but intentionally does **not** follow DRY:

| Principle | Applied? | What it means for the generated code |
|---|---|---|
| **DRY** (Don't Repeat Yourself) | **Intentionally not applied** | Readability comes before "clean" code. Each folder stands alone and is written to be understood by reading straight through, top to bottom — no jumping to shared modules. |
| **YAGNI** (You Aren't Gonna Need It) | Applied | No speculative extensibility or "might need it later" code — only the minimum needed to understand the concept. |
| **KISS** (Keep It Simple, Stupid) | Applied | Avoids clever or dense-but-cryptic logic; favors plain, straightforward code even when it is more verbose. |

> The output is **learning material, not production code**.

## 📖 code-walkthrough

The skill splits code into processing units (functions, classes, …) and pairs each with commentary — **code on the left, explanation on the right**. Key characteristics:

- **One portable HTML.** When the source spans multiple files, they are combined into a single HTML with **tab switching** — easy to carry and share, with no file-hopping.
- **No omission.** The full code is shown and explained; nothing is truncated or summarized.
- **SVG flow diagrams** are inserted for long or complex logic.
- **Glossary panel.** Technical terms in the commentary are underlined; click one to see its overview inline, so you can keep reading without looking it up elsewhere.

The output is a single self-contained HTML with no external dependencies — just open it in a browser.

## 🗂️ Repository Structure

```
code-learn-skill/
├── README.md
├── LICENSE
└── skills/
    ├── code-walkthrough/
    │   ├── SKILL.md
    │   ├── assets/
    │   │   └── template.html     # ready-made page skeleton (CSS/JS); only placeholders are filled per run
    │   └── reference/            # detailed spec (loaded on demand)
    │       ├── segments.md
    │       ├── html-layout.md
    │       ├── multi-file-tabs.md
    │       ├── interactive.md
    │       ├── glossary-panel.md
    │       └── svg.md
    └── staged-learning-code/
        ├── SKILL.md
        └── assets/
            ├── entrypoint_template.py   # per-folder entry-point skeleton
            └── readme_template.md       # per-folder README skeleton
```

## 📄 License

MIT License. See [LICENSE](LICENSE).

---

Author: [@yumeiriowl](https://github.com/yumeiriowl)
