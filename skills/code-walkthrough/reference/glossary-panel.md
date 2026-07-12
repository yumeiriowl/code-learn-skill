# Code Walkthrough — Glossary panel

## Glossary panel

Underline "technical terms that even a general engineer would find hard to understand without specialized knowledge" appearing in the commentary, and when clicked, show the term's overview in the panel on the right. Fix the panel to the right edge so it follows along as the page scrolls.

(The panel's UI text — heading, hint, term list, etc. — follows the language of the user's request. The English labels below are placeholders.)

### Overall structure

1. Underline terms in the commentary by wrapping them in `<span class="term" data-term="key">display term</span>`
2. Place a fixed glossary panel (`#glossaryPanel`) on the right. It follows the scroll with `position: fixed`
3. Register the term overviews in the `GLOSSARY` object at the end of the HTML as `key: { term, desc }`
4. `.term` click → read `GLOSSARY[key]`, show the term name and overview in the panel body, and highlight the clicked term

### Term underline (commentary side)

In the commentary, wrap terms that require specialized knowledge in a `<span>`. `data-term` is the key the panel uses to look up the overview.

```html
<p>This segment is implemented as an <span class="term" data-term="idempotent">idempotent</span> operation,
and takes <span class="term" data-term="backpressure">backpressure</span> into account.</p>
```

Even if the same term appears multiple times, give them all the same `data-term` key (define the overview only once in `GLOSSARY`).

### Term underline CSS

```css
.term {
  text-decoration: underline dotted;
  text-decoration-thickness: 1.5px;
  text-underline-offset: 3px;
  text-decoration-color: var(--syntax-function);
  cursor: pointer;
  color: inherit;
}
.term:hover { background: rgba(111, 66, 193, 0.10); }
.term.active {
  background: var(--syntax-function);
  color: #fff;
  text-decoration-color: #fff;
  border-radius: 3px;
}
```

### Glossary panel HTML

You can also open/close it with the header toggle button (`#glossaryToggleBtn`, label "Glossary").

```html
<div class="glossary-panel" id="glossaryPanel">
  <div class="glossary-header">
    <h3>Glossary</h3>
    <button class="glossary-close-btn" id="glossaryCloseBtn" title="Close">&times;</button>
  </div>
  <div class="glossary-body" id="glossaryBody">
    <!-- Default display. Clicking a term replaces this content -->
    <p class="glossary-hint">Click an <span class="term-sample">underlined term</span> in the commentary to see its overview here.</p>
    <div class="glossary-list" id="glossaryList">
      <!-- JS generates the term-name list from GLOSSARY. Clicking shows the overview -->
    </div>
  </div>
</div>
```

### Glossary panel CSS

Fix it to the right edge with `position: fixed` and make it follow the scroll. In the multi-file case, lower `top` to 88px
(see the CSS in "Multi-file tab spec").

```css
.glossary-panel {
  position: fixed; right: 0; top: 60px;
  width: 340px; height: calc(100vh - 60px);
  background-color: var(--bg-secondary);
  border-left: 1px solid var(--border-color);
  display: flex; flex-direction: column;
  z-index: 998;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease-out;
  overflow: hidden;
}
.glossary-panel.hidden {
  transform: translateX(100%);
  box-shadow: none; pointer-events: none;
}
.main.glossary-open {
  margin-right: 340px;
  transition: margin-right 0.3s ease-out;
}
.glossary-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; border-bottom: 1px solid var(--border-color);
}
.glossary-header h3 { margin: 0; font-size: 14px; color: var(--fg-primary); }
.glossary-close-btn {
  background: none; border: none; cursor: pointer;
  font-size: 18px; color: var(--fg-secondary); line-height: 1;
}
.glossary-body { padding: 16px; overflow-y: auto; flex: 1; }
.glossary-hint { font-size: 13px; color: var(--fg-secondary); line-height: 1.7; }
.glossary-term-name { font-size: 16px; font-weight: 700; color: var(--syntax-function); margin: 0 0 8px; }
.glossary-term-desc { font-size: 13px; color: var(--fg-primary); line-height: 1.8; }
.glossary-list { margin-top: 16px; border-top: 1px solid var(--border-color); padding-top: 12px; }
.glossary-list h4 { font-size: 11px; color: var(--fg-secondary); margin: 0 0 8px; text-transform: uppercase; }
.glossary-list-item {
  display: block; padding: 5px 8px; margin-bottom: 2px; border-radius: 4px;
  font-size: 12px; color: var(--fg-primary); cursor: pointer; border: none;
  background: none; text-align: left; width: 100%;
}
.glossary-list-item:hover { background: var(--bg-tertiary); }
.glossary-list-item.active { background: var(--syntax-function); color: #fff; }

/* Hide by default on mobile, open via toggle */
@media (max-width: 768px) {
  .glossary-panel { width: 100%; }
  .main.glossary-open { margin-right: 0; }
}
```

### Term data (GLOSSARY)

Inside the `<script>` at the end of the HTML, define the overviews with the same keys as the terms you underlined in the commentary.
Always wrap the keys in `"..."`. Writing a key that contains a hyphen, such as `agentic-loop`, without quotes causes
a JS syntax error and halts the entire `<script>` (tab switching and the glossary panel stop working).

```javascript
const GLOSSARY = {
  "idempotent": {
    term: "Idempotent",
    desc: "A property whereby running the same operation any number of times does not change the result. Because retries do not cause double processing, it is emphasized in distributed systems and API design."
  },
  "backpressure": {
    term: "Backpressure",
    desc: "A mechanism that, when downstream processing cannot keep up, makes the upstream throttle the inflow of data. It prevents buffer overflow and memory exhaustion."
  }
  // Register here every term used in the commentary
};
```

### GlossarySystem class (JavaScript)

```javascript
class GlossarySystem {
  constructor() {
    this.panel = document.getElementById('glossaryPanel');
    this.body = document.getElementById('glossaryBody');
    this.main = document.getElementById('mainContent');
    this.activeTerm = null;

    // Receive .term clicks in the commentary via delegation (robust to dynamic generation)
    document.addEventListener('click', (e) => {
      const span = e.target.closest('.term');
      if (span && span.dataset.term) this.show(span.dataset.term, span);
    });

    // The header "Glossary" toggle / close button
    document.getElementById('glossaryToggleBtn')?.addEventListener('click', () => this.toggle());
    document.getElementById('glossaryCloseBtn')?.addEventListener('click', () => this.close());

    this.renderList();
    // Open by default on desktop. Keep it closed on narrow screens.
    if (window.matchMedia('(max-width: 768px)').matches) {
      this.panel.classList.add('hidden');
    } else {
      this.main.classList.add('glossary-open');
    }
  }

  // Generate the term list (bottom of the panel) from GLOSSARY
  renderList() {
    const list = document.getElementById('glossaryList');
    if (!list) return;
    list.innerHTML = '<h4>Term list</h4>';
    Object.keys(GLOSSARY).forEach(key => {
      const btn = document.createElement('button');
      btn.className = 'glossary-list-item';
      btn.dataset.term = key;
      btn.textContent = GLOSSARY[key].term;
      btn.addEventListener('click', () => this.show(key));
      list.appendChild(btn);
    });
  }

  // Show the term's overview in the panel and highlight the matching term
  show(key, span) {
    const entry = GLOSSARY[key];
    if (!entry) return;
    // Open the panel if it is closed
    this.panel.classList.remove('hidden');
    if (!window.matchMedia('(max-width: 768px)').matches) this.main.classList.add('glossary-open');

    this.body.innerHTML =
      '<p class="glossary-term-name"></p><p class="glossary-term-desc"></p>';
    this.body.querySelector('.glossary-term-name').textContent = entry.term;
    this.body.querySelector('.glossary-term-desc').textContent = entry.desc;

    // Highlight the same term throughout the body (reassign active)
    document.querySelectorAll('.term.active').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.term[data-term="' + key + '"]').forEach(el => el.classList.add('active'));
    this.activeTerm = key;
  }

  toggle() {
    const willHide = !this.panel.classList.contains('hidden');
    this.panel.classList.toggle('hidden');
    if (!window.matchMedia('(max-width: 768px)').matches) {
      this.main.classList.toggle('glossary-open', !willHide);
    }
  }

  close() {
    this.panel.classList.add('hidden');
    this.main.classList.remove('glossary-open');
  }
}

// Initialization (call it alongside the other initializations)
const glossary = new GlossarySystem();
```

## Checklist

- [ ] Technical terms in the commentary are underlined with `<span class="term" data-term="key">`
- [ ] Every underlined term is registered in `GLOSSARY` with a key, and has an overview text
- [ ] The `GLOSSARY` keys are wrapped in `"..."` (matching `data-term`; no syntax error even for hyphenated keys)
- [ ] The glossary panel `#glossaryPanel` is fixed to the right edge with `position: fixed` and follows the scroll
- [ ] Clicking a term shows the term name and overview in the panel body, and the same term in the body is highlighted with `active`
- [ ] Clicking a different term switches the display and highlight
- [ ] At the bottom of the panel there is a term list derived from `GLOSSARY`, and clicking shows the overview
- [ ] The header "Glossary" button opens/closes the panel, and the body's margin-right is adjusted when the glossary panel is shown
- [ ] At 768px and below it is closed by default and shown full width via toggle
- [ ] No API keys or external communication are included (the term data is self-contained in `GLOSSARY` within the HTML)
