---
name: staged-learning-code
description: 'A skill that decomposes a technical concept (agent harness, RAG, compiler, network protocol, etc.) into its elements and generates learning material you can study in stages, with minimal code split per folder. Each folder runs on its own and can be verified with a single command (e.g., `python main.py`). It prioritizes in-file transparency over DRY, and copy-paste readability over abstraction. Use it for "learning code", "make teaching material", "implement it split by element", "in a form I can learn in stages", "I want to add more samples", and similar.'
---

# staged-learning-code — Staged Learning Material Code Generation Skill

Decompose a technical concept (agent harness, RAG pipeline, compiler frontend, network protocol, etc.) element by element, and generate learning material that lays out minimal code per folder. Prioritize transparency over DRY, and plainness over abstraction — the reverse of normal code design, because the reader is a learner, not a maintainer.

## Goals

- Take out elements one at a time, and reduce each to minimal code that runs on its own
- Opening each folder, a few files make that element's behavior clear
- Start from mocks, and connect the real thing (LLM/DB/external API) at the end
- Structure it so learners can copy-paste, run, and read along

## When to use

- "Make learning code for X"
- "I want X split element by element into a form I can learn in stages"
- "X as a minimal implementation, split per folder"
- "I want to add more samples (add a new folder to existing material)"

If there are no arguments, ask the following:

1. Target topic (what the material teaches)
2. Scope preference (optional; e.g., "minimal configuration" or "just this element". If none, decide the number of elements according to the natural decomposition of the subject)
3. Mock/implementation boundary (from which folder to use the real thing)
4. Dependency packages (standard library only, or external dependencies)
5. Adding to existing material, or a new project

## Natural language of the material (README and comments)

Decide the natural language of README.md and code comments in this priority order:

1. If the user specifies a language, follow it
2. When adding to existing material, match the existing material's language
3. Otherwise, write in the same language as the user's request

Do not infer the language from the repository name, directory name, or unrelated adjacent files. If none of the above settles it, ask before writing.

## Process

### Phase 0: Preliminary research

In environments where web search is available, before proceeding to Phase 1:

- Open at least one official document (the latest version)
- If possible, check one representative OSS repository or official sample
- If it differs from your understanding, reflect it in the material code

Check especially: technologies not in the training data or whose last update is old, libraries after a major version upgrade, and models/protocols/frameworks released within the last 1–2 years.

Skip: basic language-spec-level features (`for`, `dict`, `dataclass`, etc.), algorithm-textbook-level subjects (sorting, searching, DP, etc.), and subjects you researched within the past year with no major version upgrade since.

Leave the sources you checked (URLs) as footnotes in the README or the integrated version.

### Phase 1: Fixing the scope

Make a "won't-do list" first:

- Decompose the subject into elements; decide which to cover and which not to. Decide the count by the subject's natural decomposition, not a fixed number
- Number each folder sequentially from `01_` (gaps allowed)
- If there is existing material, do not touch existing files
- Write out the "not this time" list

If the user says "bare minimum", "minimal", "keep it simple", "just this element", etc., trim the scope accordingly.

### Phase 2: Deciding the directory structure

```
project/
├── 01_<element_name>/            # the most basic element
│   ├── <entry point>             # ~100 lines (e.g., main.py)
│   └── README.md
├── 02_<next element>/
│   ├── <entry point>             # ~150 lines
│   └── README.md
├── 03_<the one after>/
│   └── ...
└── XX_integrated/                # the integrated version at the end
    ├── <entry point>             # ~400 lines
    ├── .env.example              # if needed
    └── README.md
```

Naming rules:

- `<number>_<snake_case element name>/` format
- Assign numbers by learning order, not implementation difficulty
- Gaps and branches are allowed (e.g., `02b_<another variant>` as an alternate implementation to contrast with `02`)
- Mock folders come first; only the final integrated folder(s) use real external services (LLM / DB / external API)

### Phase 3: File-composition rules

Each folder is basically 2 files:

- Entry point — the minimal implementation of that element, with verification in the direct-execution block (e.g., Python's `if __name__ == "__main__":`, Node's `index.js`, Go's `func main`)
- `README.md` — purpose, how to run, example output, the folder to proceed to next

Exceptions:

- `.env.example` — only for folders that use real external services (LLM, DB, external API, etc.)
- Sub-dependency files — only when bundling a separate-process server, etc.

Do not create shared modules, config modules, package markers, or test files (in Python, `utils.py` / `config.py` / `__init__.py`).

### Phase 4: Implementation (mock → real)

1. Build first the folder with zero external dependencies (mock LLM, DB, external API)
2. The next folder embeds the previous folder's class while adding one new element
3. Use real external dependencies for the first time in the integrated version

If there is an execution environment and you can run the entry point directly, verify it. If you cannot, do a syntax/import check (e.g., `py_compile` for Python).

### Phase 5: Verification and documentation

- Run each folder's entry point (e.g., `python main.py`) and confirm the expected output appears
- If it fails, fix it before handing it to the user
- Put the run command and an actual example output (10–30 lines) in the README
- Guide to the next folder in a "Where to go next" section

## Principles

| Principle | Application |
|---|---|
| Give up DRY | No shared modules. The same class in two folders is fine as copy-paste — learners can place the two side by side and compare |
| Enforce YAGNI | No abstract base classes, config layers/files, plugin mechanisms, loggers, or test frameworks. Do not write "might be needed in the future" code — add it once it is needed |
| Write plainly | Use even a verbose idiom (e.g., Python's `for i in range(len(xs)):`) if it is more readable |
| Minimal abstraction | An abstract base class only when multiple concrete classes share a common interface; a class with one instance is written directly |
| Do not add dependencies | Standard library + the bare minimum. Replace convenience libraries (e.g., `jsonschema`) with handwritten code |
| Use mocks | Stub the LLM, DB, and external APIs so learners run everything without external keys |
| Use standard output | No logging library; visualize behavior with standard output (e.g., `print("[Step N] tool=...")`) |
| Embed verification | The direct-execution block runs through success + failure cases lined up in a list |
| Return errors as strings | The tool layer and external-call layer do not throw exceptions; they return an ERROR string |
| No package markers | No `__init__.py` etc.; each folder is a standalone script |
| Do not touch existing files | "Add a sample" means only adding. Editing existing folders requires permission |
| Respect "minimal" | If the user says "bare minimum", stop partway instead of building all elements |

## Per-folder templates

Start each folder from the bundled templates (Python example; for other languages, substitute the entry-point name, the direct-execution idiom, and standard-library naming):

- `assets/entrypoint_template.py` — entry-point skeleton (docstring header, section-comment blocks, showcase in the direct-execution block)
- `assets/readme_template.md` — README skeleton (What you can learn / Run / Composition / Why X is not used / Where to go next)

## How to proceed with the design

1. List the constituent elements of the target concept
2. Choose the one element the learner touches first (the one with the fewest dependencies)
3. Decide the goal experience the integrated version shows
4. Decide how many folders to place in between, limiting the element that increases in each folder to one
5. Decide the mock → real stages (only the last 1–2 folders are real)
6. Spell out the "won't-do" items in a list
7. Get the user's confirmation before entering implementation

## Completion checklist

- [ ] Each folder is basically 2 files: the entry point + `README.md`
- [ ] No shared module (e.g., `utils.py`) exists
- [ ] No package marker (e.g., `__init__.py`) is placed
- [ ] The top of each entry point states "what to learn" and "the run command"
- [ ] The showcase runs in each entry point's direct-execution block
- [ ] The mock-only folders need no external dependencies (API keys, etc.)
- [ ] Folders that use real external services have a `.env.example`
- [ ] Each README has "run command", "actual example output", and "where to go next" sections
- [ ] An abstract base class exists only when multiple concretes share a common interface
- [ ] The tool layer and external-call layer do not throw exceptions and return ERROR strings
- [ ] What is needed via a dependency-install command is stated in the README
- [ ] When adding to existing material, not a single line of existing files was touched (except when permitted)
