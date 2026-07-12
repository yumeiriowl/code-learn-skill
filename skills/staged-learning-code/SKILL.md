---
name: staged-learning-code
description: 'A skill that decomposes a technical concept (agent harness, RAG, compiler, network protocol, etc.) into its elements and generates learning material you can study in stages, with minimal code split per folder. Each folder runs on its own and can be verified with a single command (e.g., `python main.py`). It prioritizes in-file transparency over DRY, and copy-paste readability over abstraction. Use it for "learning code", "make teaching material", "implement it split by element", "in a form I can learn in stages", "I want to add more samples", and similar.'
---

# staged-learning-code — Staged Learning Material Code Generation Skill

Decompose a technical concept (agent harness, RAG pipeline, compiler frontend, network protocol, etc.) element by element, and generate learning material that lays out minimal code per folder. The principles are the reverse of normal code design: prioritize transparency over DRY, and plainness over abstraction.

## Goals

- Take out elements one at a time, and reduce each to minimal code that runs on its own
- Opening each folder, a few files make that element's behavior clear
- Start from mocks, and connect the real thing (LLM/DB/external API) at the end
- Structure it so learners can copy-paste, run, and read along

The writer will be tempted toward DRY and abstraction, but avoid that in learning material.

## When to use

- "Make learning code for X"
- "I want X split element by element into a form I can learn in stages"
- "X as a minimal implementation, split per folder"
- "I want to add more samples (add a new folder to existing material)"

If there are no arguments, ask the following:

1. Target topic (what the material teaches)
2. Scope preference (optional; if there is a specification like "minimal configuration" or "just this element". If none, decide the number of elements yourself according to the natural decomposition of the subject)
3. Mock/implementation boundary (from which folder to use the real thing)
4. Dependency packages (standard library only, or external dependencies)
5. Adding to existing material, or a new project

## Natural language of the material (README and comments)

Decide the natural language of README.md and code comments in this priority order:

1. If the user specifies a language, follow it.
2. When adding to existing material, match the existing material's language.
3. Otherwise, write in the same language as the user's request.

Do not infer the language from the repository name, directory name, or unrelated adjacent files — those are not reliable signals. If none of the above settles it, ask before writing.

## Process

### Phase 0: Preliminary research

In environments where web search is available, before proceeding to Phase 1, check 1–2 pieces of official information or representative implementations.

- Open at least one official document (the latest version)
- If possible, check one representative OSS repository or official sample
- If it differs from your understanding, reflect it in the material code

Targets to check especially:

- Technologies not in the training data, or whose last update is old
- After a major version upgrade of a library
- New models / protocols / frameworks released within the last 1–2 years

Subjects you may skip:

- Basic language-spec-level features (`for`, `dict`, `dataclass`, etc.)
- Algorithm-textbook-level subjects (sorting, searching, DP, etc.)
- When you have already researched the same subject within the past year and are confident there has been no major version upgrade since

Leave the sources you checked (URLs) as footnotes in the README or the integrated version.

### Phase 1: Fixing the scope

First, make a "won't-do list".

- What to treat as elements (decompose the subject into elements, and decide which elements to cover and which not to. Decide the number of elements according to the natural decomposition of the subject; do not set a fixed number)
- Numbering of each folder (sequential numbers starting from `01_`. Gaps are allowed)
- If there is existing material, do not touch existing files
- Write out the "not this time" list

By default, decide the number of elements according to the natural decomposition of the subject. If the user explicitly says "bare minimum", "minimal", "keep it simple", "just this element", etc., trim the scope accordingly.

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
- Gaps are allowed (e.g., add a branch with `02b_<another variant>`)

Example structure patterns:

| Folder | Role | External dependency |
|---|---|---|
| `01_<element A>/` | the basic element with the fewest dependencies | mock |
| `02_<element B>/` | add the next element | mock |
| `02b_<element B variant>/` | an alternate implementation to contrast with 02 | mock |
| `03_<element C>/` | add another element | mock |
| `08_integrated/` | the finished form integrating all elements | real (LLM / DB / external API) |
| `09_integrated_<variant>/` | another variant of the integrated version | real |

### Phase 3: File-composition rules

Each folder is basically 2 files:

- Entry point — the minimal implementation of that element. Include verification in the direct-execution block (e.g., Python's `if __name__ == "__main__":`, Node's `index.js`, Go's `func main`)
- `README.md` — purpose, how to run, example output, the folder to proceed to next

Things to add as exceptions:

- `.env.example` — only for folders that use real external services (LLM, DB, external API, etc.)
- Sub-dependency files — only when bundling a separate-process server, etc.

Do not create shared modules, config modules, package markers, or test files (in Python, `utils.py` / `config.py` / `__init__.py`).

### Phase 4: Implementation (mock → real)

1. The first thing to build is a folder with zero external dependencies (mock LLM, DB, external API)
2. The next folder embeds the previous folder's class while adding one new element
3. Use real external dependencies for the first time in the integrated version

If there is an execution environment and you can run the entry point directly, verify it. If you cannot, do a syntax/import check (e.g., `py_compile` for Python).

### Phase 5: Verification and documentation

- Run each folder's entry point (e.g., `python main.py`) and confirm the expected output appears
- If it fails, fix it before handing it to the user
- Put the run command and an actual example output (10–30 lines) in the README
- Guide to the next folder in a "Where to go next" section

## Principles to uphold

| Principle | Interpretation in material code |
|---|---|
| Give up DRY | Do not create shared modules. The same class in two folders is fine as copy-paste. Learners can place the two side by side and compare |
| Enforce YAGNI | Do not create abstract base classes, config layers, plugin mechanisms, loggers, or test frameworks |
| Write plainly | Use even a verbose idiom (e.g., Python's `for i in range(len(xs)):`) if it is more readable |
| Minimal abstraction | Use an abstract base class only when multiple concrete classes share a common interface. If there is only one, write it directly |
| Do not add dependencies | When adding a dependency, check "does it not work without this". Replace convenience libraries (e.g., `jsonschema`) with handwritten code |
| Use mocks | With mocks (stubs of LLM, DB, external API), let learners run it without external keys |
| Use standard output | Do not use a logging library; visualize behavior with standard output (e.g., `print("[Step N] tool=...")`) |
| Embed verification | In the direct-execution block, run through success cases + failure cases lined up in a list |
| Return errors as strings | The tool layer and external-call layer do not throw exceptions; they return an ERROR string |
| Do not touch existing files | When asked to "add a sample", only add. Editing existing folders requires permission |

## Anti-patterns

1. Create a shared module → make each folder self-contained
2. Create abstract base classes too early (e.g., Python `ABC`) → a class that has only one instance needs no abstraction
3. Bring in a logging library (e.g., Python `logging`) → standard output is enough
4. Add a test framework (e.g., `pytest`, `jest`) → the showcase in the direct-execution block is enough
5. Create config files (YAML/TOML, etc.) → hardcoding is enough
6. Add dependency packages → standard library + the bare minimum only
7. Throw exceptions (e.g., `raise`, `throw`) → catch upstream and stringify, or return an ERROR string
8. Write "X might be needed in the future" → add it once it is needed
9. Place package markers (e.g., `__init__.py`) → each folder is a standalone script
10. Build all elements at once → if the user says "bare minimum", stop partway

## Per-folder template

The following is a Python example. For other languages, substitute the entry-point name (e.g., `index.js`, `main.go`), the direct-execution idiom, and standard-library naming.

### Typical structure of the entry point (Python `main.py`)

```python
"""
<number>_<element_name> — <one-line description of the element>.

<a declaration that reading just this file makes the behavior clear>
<what is intentionally omitted>

Run: python main.py
"""

# Standard library only. If there are external dependencies, keep them minimal.

# ---------------------------------------------------------------------------
# <the element's lead class>: <one-line description>
#   - <key point 1>
#   - <key point 2>
# ---------------------------------------------------------------------------
class MainClass:
    def __init__(self, ...):
        ...

    def public_method(self, ...):
        ...


# ---------------------------------------------------------------------------
# Showcase for verification. Run through success + failure cases lined up in a list.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    instance = MainClass(...)

    print("=== Cases ===")
    cases = [
        ("success case 1", {"arg": "..."}),
        ("failure case 1", {"arg": "..."}),  # deliberately break it to show the behavior
    ]
    for name, args in cases:
        result = instance.public_method(args)
        print(f"  {name}: {result}")
```

### Typical structure of README.md

```markdown
# <number>_<element_name> — <short title>

<1–2 line folder overview>

## What you can learn

- <learning point 1>
- <learning point 2>
- <learning point 3>

## Run

```bash
<the entry point's run command>   # e.g., python main.py
```

<10–30 lines of expected example output>

## Composition

- `MainClass` — <role>
- `helper` — <role>

## Why X is not used

<2–3 lines about the elements cut via YAGNI>

## Where to go next

- `<next folder>/` — <what increases there>
```

## How to proceed with the design

1. List the constituent elements of the target concept (follow the natural decomposition of the subject; do not fix the count)
2. Choose the one element the learner touches first (the one with the fewest dependencies)
3. Decide the goal experience the integrated version shows
4. Decide how many folders to place in between according to the subject's decomposition (do not set a fixed number; if the user specifies "minimal", etc., reduce accordingly)
5. Limit the element that increases in each folder to one
6. Decide the mock → real stages (only the last 1–2 folders are real)
7. Spell out the "won't-do" items in a list
8. Get the user's confirmation before entering implementation

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

## Notes when writing

When you feel tempted toward DRY, abstraction, or configurability, stop. In learning material, prioritize the following:

- Do not abstract (so the learner does not have to chase one level deeper)
- Do not share (do not make the learner reference other folders)
- Do not make it configurable (so the learner does not puzzle over what to configure)

Copy-paste the same code, and keep it in a state where a beginner can place the two side by side and compare the differences.
