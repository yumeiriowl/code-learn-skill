---
name: code-walkthrough
description: 'Split source code into segments and generate a self-contained explanatory HTML that embeds the full code, commentary, SVG diagrams, and a glossary panel (multiple files are combined into a single HTML with tabs). Use it for "explain this code", "make a walkthrough", "create a code-explanation HTML/report", "make it readable with diagrams", and similar. When a source path is given and an explained HTML is wanted, use it even without an explicit instruction.'
---

# Code Walkthrough — Source Code Explanation HTML Generation Skill

Split source code from the top into processing units (segments), and generate a single self-contained interactive HTML that pairs the fully embedded code with detailed commentary, SVG diagrams, and a glossary panel.

> For progressive loading, this skill splits the detailed spec into `reference/`. As shown in the table below, read the relevant file at the point you need it.

## Usage

Arguments: source file paths (required, multiple allowed), output HTML path (optional). If the last argument ends in `.html`, treat it as the output destination.

### Single file

Pass one source file. If an output destination is specified, generate there; if omitted, generate `walkthrough-<filename>.html` in the same folder as the source.

### Multiple files (combined into a single HTML with tabs)

Passing two or more source files switches to multi-file mode, combining them into a single HTML with a tab-switching UI.

- When the output destination is omitted, generate `walkthrough-<a>-<b>[-...].html` in the folder of the first file. If the combined name exceeds 80 characters, fall back to `walkthrough-multi-<N>files.html`
- Each source file = one tab. The tab label is the base file name (without extension). When names collide, such as `main.py`, prefix the parent folder name (e.g., `08_rlm_real/main`)
- If even one file does not exist, exit with an error

## Execution steps

1. Parse the arguments:
   - Just one file → single-file mode
   - Two or more files → multi-file mode (see "Multi-file tab spec")
   - If the last argument ends in `.html`, separate it out as the output destination
2. Confirm that all source files exist. If even one is missing, exit with an error.
3. Determine the output destination:
   - If specified by argument, that path
   - Single file: `walkthrough-<filename>.html` (same folder as the source)
   - Multiple files: `walkthrough-<a>-<b>[-...].html` (folder of the first file; if too long, `walkthrough-multi-<N>files.html`)
4. Read each source file in full.
5. For each file, write the commentary following "Segment splitting rules" and "Structure of each segment". In environments where web search is available, when a library, API, or spec you use is new / your knowledge is stale / you are unsure, check the official docs before writing the commentary.
   - Identify "technical terms that even a general engineer would find hard to understand without specialized knowledge" appearing in the commentary, underline them with `<span class="term">` following `reference/glossary-panel.md`, and register their overviews in `GLOSSARY`.
   - When you diagram a processing flow with SVG, run the "SVG verification phase" in `reference/svg.md` every time you make a diagram, and confirm that all arrows connect to their targets before moving on to the next segment.
6. Assemble and output the HTML:
   - Single file: use the layout structure in "HTML generation rules"
   - Multiple files: add `<div class="tabs">` and tab panels following "Multi-file tab spec"
   - Incorporate the glossary panel following `reference/glossary-panel.md`
   - When the output exceeds what can be written out at once (files over 500 lines / a large combined total across multiple files): generate and run `gen_walkthrough.py` under a temporary directory (`/tmp`, `$TMPDIR`, or on Windows `%TEMP%`, whichever path fits the environment) to produce the HTML
7. Open it in the browser with "Browser display command".

## Reference (read when needed)

The detailed spec is split into `reference/`. Read the relevant file at the point it becomes needed within the execution steps.

| Reference file | Contents | When to read |
|---|---|---|
| `reference/segments.md` | Segment splitting rules, structure of each segment, checklist for code embedding/commentary | When splitting the code and writing commentary (execution step 5) |
| `reference/svg.md` | SVG diagram generation rules, CSS classes, SVG verification phase, checklist | When diagramming a complex processing flow, after making the diagram (execution step 5) |
| `reference/html-layout.md` | HTML generation rules, CSS variables, syntax highlighting, layout structure | When assembling the HTML (execution step 6) |
| `reference/multi-file-tabs.md` | Multi-file tab spec (HTML/CSS/JS) | When there are two or more sources (execution step 6, multi-file case) |
| `reference/interactive.md` | Interactive features (TOC, progress bar, view modes, expand/collapse, copy) | When implementing UI behavior |
| `reference/glossary-panel.md` | Glossary panel (HTML/CSS/JS, term underlining, scroll following) | When implementing term underlining and the glossary panel (execution steps 5 and 6) |

## Browser display command

After generating, open it in the default browser matching the OS of the execution environment (`$OUTPUT_PATH` is the path to the output HTML):

- **macOS**: `open "$OUTPUT_PATH"`
- **Linux**: `xdg-open "$OUTPUT_PATH"`
- **WSL**: `cmd.exe /c start "" "$(wslpath -w "$OUTPUT_PATH")"`
- **Windows (cmd)**: `start "" "%OUTPUT_PATH%"`
- **Windows (PowerShell)**: `Start-Process "$OUTPUT_PATH"`

To auto-detect in a POSIX shell:

```bash
if grep -qi microsoft /proc/version 2>/dev/null; then
  cmd.exe /c start "" "$(wslpath -w "$OUTPUT_PATH")" 2>/dev/null   # WSL
elif command -v open >/dev/null 2>&1; then
  open "$OUTPUT_PATH"                                              # macOS
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$OUTPUT_PATH"                                          # Linux
fi
```

## Pre-completion check

Before outputting the HTML, review the "Checklist" at the end of each reference file corresponding to the features you used. At a minimum, always review `reference/segments.md` (code embedding, commentary), `reference/html-layout.md` (layout), and `reference/glossary-panel.md` (glossary panel). If you used SVG or multiple files, also review the checklists of `reference/svg.md` (that the SVG verification phase has been run) and `reference/multi-file-tabs.md` respectively.
