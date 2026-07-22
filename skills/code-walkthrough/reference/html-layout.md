# Code Walkthrough — HTML generation rules

## Using the template

Copy `assets/template.html` (bundled with this skill) to the output path and fill it in. The layout, CSS variables (light/dark), view modes, expand/collapse, copy buttons, TOC highlighting, progress bar, tab switching, and glossary panel are already implemented in the template — do not rewrite or restyle them. Fill only the placeholders, following the comments in the template:

1. `{{LANG}}` — the `lang` attribute (e.g., `en`, `ja`), matching the language of the user's request
2. `{{TITLE}}` (2 places: `<title>` and header `<h1>`) — `<filename> - Code Walkthrough` in the request language
3. All spots marked `UI-LABEL` (header buttons, "Contents", "Glossary", the hint text, the `UI_TEXT` object in the script) — translate into the request language
4. `TOC INSERTION POINT` — one static link per segment: `<a class="toc-link toc-link-<type>" href="#segment-1">1. Title</a>`
5. `SEGMENTS INSERTION POINT` — the segment markup below
6. `GLOSSARY` — one entry per underlined term (see `reference/glossary-panel.md`)
7. Single file: delete the `MULTI-FILE ONLY` block. Multiple files: see `reference/multi-file-tabs.md`

## Basic requirements

- **Single self-contained file**: the template has no external dependencies; keep the parts you add that way too (no CDN, no external images/fonts)
- **Output language**: commentary, UI text, and the `lang` attribute follow the language of the user's request
- **Character encoding**: UTF-8

## Prohibitions

1. **Do not embed code with JavaScript template literals (backticks `` ` ``)**. Write code directly as static HTML inside `<pre><code>` tags, escaping `<`, `>`, `&`, `"` as `&lt;`, `&gt;`, `&amp;`, `&quot;`.
2. **Do not omit or excerpt code**. Even if a class is 300 lines, include every line in the HTML. Do not use placeholders like `# ... omitted ...`.
3. **Do not delete or modify the template's CSS/JS** (except the marked placeholders and UI labels).

## Segment markup

Insert one `<section>` per segment at the `SEGMENTS INSERTION POINT`:

```html
<section class="segment" id="segment-1" data-type="imports" data-lines="1-42">
  <div class="segment-header">
    <button class="expand-toggle">&#9660;</button>
    <h2>Segment title</h2>
    <span class="badge badge-imports">imports (L1-42)</span>
  </div>
  <div class="segment-body">
    <div class="segment-content">
      <div class="code-block">
        <div class="code-header">
          <span>Python (L1-42)</span>
          <button class="copy-button">Copy</button>
        </div>
        <div class="code-lines">
          <div class="line-numbers"><pre>1
2
3</pre></div>
          <div class="code-content"><pre><code><!-- full highlighted code --></code></pre></div>
        </div>
      </div>
      <div class="explanation">
        <h3>Heading</h3>
        <p>Detailed commentary...</p>
        <!-- SVG diagram as needed (reference/svg.md) -->
      </div>
    </div>
  </div>
</section>
```

- `badge-<type>` and `toc-link-<type>` use the segment type names from `reference/segments.md` (`imports`, `constants`, `types`, `class`, `function`, `main`, `config`, `other`); the colors are defined in the template
- The `line-numbers` `<pre>` holds one number per code line, newline-separated — the same count as the code lines

## CSS-based simple syntax highlighting

Embed `<span>` tags directly in the static HTML (do not generate them with JS). The classes are already styled in the template:

| Class | Target |
|---|---|
| `.kw` | Language keywords (if, for, class, def, return, import, etc.) |
| `.st` | String literals |
| `.cm` | Comments |
| `.nb` | Numeric literals |
| `.fn` | Function names |
| `.bl` | Built-in functions/types |
| `.de` | Decorators |
| `.op` | Operators |

## Handling large files

When the output exceeds what can be written out at once (files over 500 lines / a large combined total across multiple files):

1. Generate `gen_walkthrough.py` under a temporary directory (`/tmp`, `$TMPDIR`, or on Windows `%TEMP%`). The script reads `assets/template.html`, fills the placeholders, and writes the output HTML
2. Run it, confirm the output
3. Delete the script afterward

## Checklist

- [ ] Started from `assets/template.html`; its CSS/JS is unmodified apart from placeholders and UI labels
- [ ] All `{{...}}` placeholders, `UI-LABEL` spots, and insertion-point comments are replaced (no `{{` remains in the output)
- [ ] The full code is embedded as static HTML inside `<pre><code>`, escaped, with no omission
- [ ] Line numbers match the code line count in every code block
- [ ] One TOC link per segment, with the matching `toc-link-<type>` class
- [ ] Single file: the `MULTI-FILE ONLY` block is deleted
- [ ] Large-file case: the generation script was deleted after producing the HTML
