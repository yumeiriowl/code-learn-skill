# Code Walkthrough — Multi-file tab spec

## Multi-file tab spec

Additional spec for combining multiple source files into a single HTML. Does not apply to the single-file case.

### Design policy

- One file = one tab. Switching tabs shows the segments of each file selectively
- Use alphabet letters (`a`, `b`, `c`, ...) for tab IDs
- The segment DOM ID has the form `seg-<tab>-<idx>-<key>` (e.g., `seg-a-3-llm`). It does not collide across tabs
- The table of contents (TOC) is split per tab, and only the active tab's is shown
- The glossary panel is shared across all tabs. `GLOSSARY` is unified as one for the whole HTML (so the same term can be referenced across tabs)
- Optionally place a "file info intro block" at the top of each tab (its role and relationship to other tabs in 2–3 sentences)

### HTML structure

```html
<!-- A fixed tab bar just below the header, above the container -->
<div class="tabs">
  <div class="tab active" data-tab="a">08_rlm_real <span class="tab-meta">(RLM)</span></div>
  <div class="tab" data-tab="b">09_lambda_real <span class="tab-meta">(λ-RLM)</span></div>
</div>

<div class="container">
  <div class="sidebar" id="sidebar">
    <h3>Contents</h3>
    <!-- Split toc-group per tab, toggling display with the active class -->
    <div class="toc-group active" data-file="a">
      <a class="toc-link toc-link-imports" href="#seg-a-1-hdr"
         onclick="event.preventDefault(); scrollToSeg('seg-a-1-hdr', 'a');">...</a>
      ...
    </div>
    <div class="toc-group" data-file="b">
      <a class="toc-link toc-link-imports" href="#seg-b-1-hdr"
         onclick="event.preventDefault(); scrollToSeg('seg-b-1-hdr', 'b');">...</a>
      ...
    </div>
  </div>

  <div class="main" id="mainContent">
    <!-- One tab = one tab-panel. Non-active ones are display: none -->
    <div class="tab-panel active" data-tab="a">
      <div class="intro">
        <h2>08_rlm_real (RLM real-LLM integrated version)</h2>
        <p>What this tab covers and its relationship to the other tabs, in 2–3 sentences.</p>
      </div>
      <!-- Segments: with a tab prefix, like id="seg-a-1-hdr" -->
    </div>
    <div class="tab-panel" data-tab="b">
      <div class="intro">
        <h2>09_lambda_real (λ-RLM real-LLM integrated version)</h2>
        <p>...</p>
      </div>
      <!-- Segments: like id="seg-b-1-hdr" -->
    </div>
  </div>
</div>
```

### CSS

```css
.tabs {
  position: sticky; top: 47px; z-index: 998;
  background: var(--bg-secondary); border-bottom: 1px solid var(--border-color);
  padding: 6px 16px; display: flex; gap: 8px; align-items: center;
}
.tab {
  padding: 8px 14px; cursor: pointer;
  background: var(--bg-tertiary); color: var(--fg-secondary);
  border: 1px solid var(--border-color); border-radius: 4px 4px 0 0;
  font-size: 13px; font-weight: 600;
  border-bottom: 3px solid transparent;
}
.tab.active {
  background: var(--bg-primary); color: var(--fg-primary);
  border-bottom-color: var(--syntax-function);
}
.tab .tab-meta { color: var(--fg-secondary); font-weight: normal; font-size: 11px; margin-left: 6px; }

.tab-panel { display: none; }
.tab-panel.active { display: block; }

.toc-group { display: none; }
.toc-group.active { display: block; }

/* Lower the top of sidebar / glossary-panel by the height of the tab bar (47px + about 41px = 88px) */
/* sidebar is position: fixed (see "Interactive features"). From top 60px in the single-file case to 88px */
.sidebar { top: 88px; height: calc(100vh - 88px); }
.glossary-panel { top: 88px; height: calc(100vh - 88px); }
.container { min-height: calc(100vh - 88px); }
```

### JavaScript

```javascript
let currentTab = 'a';

function setTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.dataset.tab === tab));
  document.querySelectorAll('.toc-group').forEach(g => g.classList.toggle('active', g.dataset.file === tab));
  window.scrollTo({ top: 0, behavior: 'auto' });
  updateProgressBar();
}

document.querySelectorAll('.tab').forEach(t => {
  t.addEventListener('click', () => setTab(t.dataset.tab));
});

// Scrolling from a TOC link (with automatic tab switching)
function scrollToSeg(id, file) {
  if (file !== currentTab) setTab(file);
  requestAnimationFrame(() => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
}

// The expand-all / collapse-all buttons target only the active tab
//   document.querySelectorAll('.tab-panel.active .segment-body').forEach(...)
```

### Intro block (optional)

In the multi-file case, place a short explanation at the top of each tab:

```css
.intro {
  background: var(--bg-secondary); border: 1px solid var(--border-color);
  border-radius: 6px; padding: 16px 20px; margin-bottom: 24px;
}
.intro h2 { margin: 0 0 8px; font-size: 17px; }
.intro p { margin: 6px 0; font-size: 14px; }
```

### Distinguishing from the single-file case

- **Single file**: do not generate tab-related HTML / CSS / JS. Keep the layout simple
- **Multi-file only**: add the structure above. Enable tab switching / TOC switching / context narrowing

## Checklist


- [ ] When there are two or more source files, integrate them into a single HTML with tabs (do not make a separate HTML per file)
- [ ] Place `<div class="tabs">` just below the header, linking tab panels and links via the `data-tab` attribute
- [ ] The segment DOM ID has the form `seg-<tab>-<idx>-<key>` with no collision across tabs
- [ ] The TOC is split per tab into `toc-group`, and only the active tab's is shown
- [ ] The CSS has `.tab-panel{display:none}` and `.tab-panel.active{display:block}`, so inactive panels are hidden (without this, all files stack vertically)
- [ ] Calling `setTab(tab)` switches the tab / TOC / tab-panel simultaneously
- [ ] The glossary panel is shared across all tabs, and `GLOSSARY` is unified as one for the whole HTML
- [ ] The expand-all / collapse-all buttons are scoped to under `.tab-panel.active`
- [ ] An intro block (a short file description) is placed at the top of each tab (optional but recommended)
- [ ] The output file name is `walkthrough-<a>-<b>[-...].html`, or `walkthrough-multi-<N>files.html` if it exceeds 80 characters
- [ ] The `top` of sidebar / glossary-panel is adjusted by the height of the tab bar (about 88px)


