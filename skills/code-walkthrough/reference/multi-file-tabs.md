# Code Walkthrough — Multi-file tab spec

Additional spec for combining multiple source files into a single HTML. Does not apply to the single-file case. The tab CSS/JS (`setTab`, `scrollToSeg`, active-tab scoping) is already in `assets/template.html`.

## Template steps

1. Uncomment the `MULTI-FILE ONLY` tab-bar block and add one `<div class="tab">` per file (only the first has `active`)
2. Set the CSS variable `tabs-h` from `0px` to `44px` (the sidebar, glossary panel, and body offset follow automatically)
3. Wrap each file's segments in a tab panel at the `SEGMENTS INSERTION POINT`:
   ```html
   <div class="tab-panel active" data-tab="a">
     <div class="intro">
       <h2>file_a (role)</h2>
       <p>What this tab covers and its relationship to the other tabs, in 2–3 sentences.</p>
     </div>
     <!-- segments of file a -->
   </div>
   <div class="tab-panel" data-tab="b">...</div>
   ```
4. Split the TOC into one `toc-group` per tab at the `TOC INSERTION POINT`:
   ```html
   <div class="toc-group active" data-file="a">
     <a class="toc-link toc-link-imports" href="#seg-a-1-hdr"
        onclick="event.preventDefault(); scrollToSeg('seg-a-1-hdr', 'a');">1. Title</a>
   </div>
   <div class="toc-group" data-file="b">...</div>
   ```

## Naming rules

- One file = one tab. Tab IDs are alphabet letters (`a`, `b`, `c`, ...)
- Tab label: the base file name (without extension). When names collide, such as `main.py`, prefix the parent folder name (e.g., `08_rlm_real/main`)
- Segment DOM IDs have the form `seg-<tab>-<idx>-<key>` (e.g., `seg-a-3-llm`) so they do not collide across tabs
- The glossary panel is shared across all tabs: one unified `GLOSSARY` for the whole HTML
- Output file name: `walkthrough-<a>-<b>[-...].html`; if it exceeds 80 characters, `walkthrough-multi-<N>files.html`

## Checklist

- [ ] Two or more source files are integrated into one HTML with tabs (not one HTML per file)
- [ ] The tab bar block is uncommented, with one `.tab` per file linked via `data-tab`
- [ ] `tabs-h` is set to `44px`
- [ ] Each file's segments are wrapped in a `.tab-panel`; only the first has `active`
- [ ] Segment IDs use `seg-<tab>-<idx>-<key>` with no collisions
- [ ] The TOC is split into per-tab `toc-group`s; links call `scrollToSeg(id, tab)`
- [ ] `GLOSSARY` is one unified object for the whole HTML
- [ ] An intro block (short file description) is placed at the top of each tab
