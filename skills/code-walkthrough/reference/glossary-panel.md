# Code Walkthrough — Glossary panel

Underline technical terms in the commentary; clicking one shows its overview in the fixed right-hand panel. The panel's HTML/CSS/JS (`GlossarySystem`) is already in `assets/template.html` — you provide only the underlines and the `GLOSSARY` entries.

## What to underline

- Terms that even a general engineer would find hard to understand without specialized knowledge (e.g., idempotency, backpressure, memoization, vector embeddings)
- Do not underline common words (variables, functions, loops, etc.)

## Term underline (commentary side)

```html
<p>This segment is implemented as an <span class="term" data-term="idempotent">idempotent</span> operation,
and takes <span class="term" data-term="backpressure">backpressure</span> into account.</p>
```

- `data-term` is the key used to look up the overview in `GLOSSARY`
- When the same term appears multiple times, give every occurrence the same `data-term` key (define the overview once)

## Term data (GLOSSARY)

Fill the `GLOSSARY` object in the template's script with the same keys as the underlined terms. Always wrap the keys in `"..."` — an unquoted hyphenated key such as `agentic-loop` is a JS syntax error that halts the entire script.

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
  // Register here every term underlined in the commentary
};
```

Write `term` and `desc` in the language of the user's request.

## Checklist

- [ ] Technical terms in the commentary are underlined with `<span class="term" data-term="key">`
- [ ] Every underlined term has a `GLOSSARY` entry with the same key; no entry is unused
- [ ] All `GLOSSARY` keys are wrapped in `"..."`
- [ ] `term`/`desc` are written in the request language
- [ ] The term data is self-contained in `GLOSSARY` (no external communication)
