# Code Walkthrough — HTML generation rules

## HTML generation rules

### Basic requirements

- **Single file**: no external dependencies. All CSS and JS are inline
- **White background (light mode) by default**: dark mode is supported via `prefers-color-scheme`, but the default is light mode
- **Responsive**: hide the sidebar at 768px and below, turning it into a hamburger menu
- **Output language**: the UI text (button labels, headings, glossary panel labels, etc.) and the `lang` attribute follow the language of the user's request (e.g., `lang="en"` for an English request, `lang="ja"` for a Japanese request). The English labels in the examples below are placeholders; render them in the request's language
- **Character encoding**: UTF-8

### Prohibitions

1. **Do not embed code with JavaScript template literals (backticks `` ` ``)**. Write code directly as static HTML inside `<pre><code>` tags, escaping with `&lt;`, `&gt;`, `&amp;`, `&quot;`.
2. **Do not omit or excerpt code**. Even if a class is 300 lines, include every line in the HTML. Do not use placeholders like `# ... omitted ...`.
3. **Do not omit `fill="none"` on SVG `<path>` elements**.

### CSS variables

```css
:root {
    /* Light mode (default) */
    --bg-primary: #f5f5f5;
    --bg-secondary: #ffffff;
    --bg-tertiary: #f9f9f9;
    --fg-primary: #333333;
    --fg-secondary: #666666;
    --border-color: #e0e0e0;
    --syntax-keyword: #d73a49;
    --syntax-string: #032f62;
    --syntax-comment: #6a737d;
    --syntax-number: #005cc5;
    --syntax-function: #6f42c1;
    --syntax-builtin: #005a9c;
    --syntax-decorator: #d08770;
    --syntax-operator: #24292e;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #282c34;
        --bg-secondary: #21252b;
        --bg-tertiary: #1e1e1e;
        --fg-primary: #abb2bf;
        --fg-secondary: #828997;
        --border-color: #3e4451;
        --syntax-keyword: #c678dd;
        --syntax-string: #98c379;
        --syntax-comment: #5c6370;
        --syntax-number: #d19a66;
        --syntax-function: #61afef;
        --syntax-builtin: #56b6c2;
        --syntax-decorator: #e5c07b;
        --syntax-operator: #abb2bf;
    }
}
```

### CSS-based simple syntax highlighting

Highlight the code by embedding `<span>` tags directly in the static HTML (do not generate them dynamically with JS).

| Class | Target | CSS |
|---|---|---|
| `.kw` | Language keywords (if, for, class, def, return, import, etc.) | `color: var(--syntax-keyword); font-weight: bold;` |
| `.st` | String literals | `color: var(--syntax-string);` |
| `.cm` | Comments | `color: var(--syntax-comment); font-style: italic;` |
| `.nb` | Numeric literals | `color: var(--syntax-number);` |
| `.fn` | Function names | `color: var(--syntax-function);` |
| `.bl` | Built-in functions/types | `color: var(--syntax-builtin);` |
| `.de` | Decorators | `color: var(--syntax-decorator);` |
| `.op` | Operators | `color: var(--syntax-operator);` |

### Layout structure

```
<body>
  <div class="progress-bar" id="progressBar"></div>

  <div class="header">
    <h1>Filename - Code Walkthrough</h1>
    <div class="header-controls">
      <button id="viewToggleCode">Code + Explanation</button>
      <button id="viewToggleCodeOnly">Code Only</button>
      <button id="viewToggleExplanationOnly">Explanation Only</button>
      <button id="expandAllBtn">Expand</button>
      <button id="collapseAllBtn">Collapse</button>
      <button class="toc-toggle-btn" id="tocToggleBtn">Contents</button>
      <button class="glossary-toggle-btn" id="glossaryToggleBtn">Glossary</button>
      <button class="hamburger" id="hamburgerBtn">☰</button>
    </div>
  </div>

  <!-- Multi-file mode only: tab-switching bar (see "Multi-file tab spec" for details)
       <div class="tabs">
         <div class="tab active" data-tab="a">file_a <span class="tab-meta">(role)</span></div>
         <div class="tab" data-tab="b">file_b <span class="tab-meta">(role)</span></div>
       </div>
  -->

  <div class="container">
    <div class="sidebar" id="sidebar">
      <div id="tocContainer"></div>
    </div>

    <div class="main" id="mainContent">
      <!-- Single file: place the segments directly -->
      <!-- Multiple files: wrap them in tab panels (<div class="tab-panel" data-tab="a">...</div>) -->
      <!-- Segments -->
      <section class="segment" id="segment-1" data-type="imports" data-lines="1-42">
        <div class="segment-header">
          <button class="expand-toggle">▼</button>
          <h2>Segment title</h2>
          <span class="badge badge-imports">imports (L1-42)</span>
        </div>
        <div class="segment-body expanded">
          <div class="segment-content">
            <!-- Left: code block -->
            <div class="code-block">
              <div class="code-header">
                <span>Python (L1-42)</span>
                <button class="copy-button">Copy</button>
              </div>
              <div class="code-lines">
                <div class="line-numbers"><pre>1
2
3
...</pre></div>
                <div class="code-content"><pre><code><!-- Full highlighted code --></code></pre></div>
              </div>
            </div>
            <!-- Right: explanation -->
            <div class="explanation">
              <h3>Heading</h3>
              <p>Detailed commentary...</p>
              <!-- SVG diagram as needed -->
              <svg viewBox="0 0 800 400" style="width: 100%; max-width: 800px;">
                <!-- ... -->
              </svg>
            </div>
          </div>
        </div>
      </section>
      <!-- Next segment... -->
    </div>
  </div>

  <!-- Glossary panel (scroll-following, fixed on the right) -->
  <div class="glossary-panel" id="glossaryPanel">
    <!-- See "Glossary panel" below -->
  </div>

  <script>
    <!-- See "JavaScript" below -->
  </script>
</body>
```

### Segment content layout

```css
.segment-content {
    display: grid;
    grid-template-columns: 1fr 1fr;  /* Desktop: code on the left + explanation on the right */
    gap: 1.5rem;
}
@media (max-width: 768px) {
    .segment-content { grid-template-columns: 1fr; }  /* Mobile: stacked vertically */
}
```

## Checklist

### Layout

- [ ] The sidebar is hidden at 768px and below
- [ ] The sidebar TOC is fixed with `position: fixed`, so the table of contents does not move together with the body when it scrolls (add `margin-left: 280px` to `.main` to make room)
- [ ] The main content's margin-right is adjusted when the glossary panel is shown
- [ ] z-index: progress bar 1000, header 999, glossary panel 998, sidebar 100
- [ ] The vertical alignment of the line numbers and the code matches: explicitly set the same `font-size` (e.g., 12px) and `line-height` (e.g., 1.5) on all three of `.line-numbers pre`, `.code-content pre`, `.code-content code`. Combine them into a shared declaration:
  ```css
  .line-numbers pre, .code-content pre, .code-content code {
    margin: 0;
    font-family: ui-monospace, Consolas, monospace;
    font-size: 12px;
    line-height: 1.5;
  }
  ```

### Handling large files

- [ ] For files over 500 lines, consider generating the HTML with a Python script
- [ ] When the output exceeds what can be written out at once, use the flow of script generation → running `gen_walkthrough.py` under a temporary directory → HTML output (`/tmp`, `$TMPDIR`, or on Windows `%TEMP%`, whichever path fits the environment)
- [ ] Delete the generated script afterward


