# Code Walkthrough — SVG diagram generation rules

## SVG diagram generation rules

For complex processing flows, architectures, and data flows, insert inline SVG diagrams into the commentary.

### Mandatory rules

1. **Explicitly set `fill="none"` on every `<path>` element**. Because SVG paths default to `fill: black`, without this a black rectangle is drawn
2. **Place a target element at the tip of every arrow**. An arrow must not point at nothing. Even the Yes/No paths of a branch must always have a destination box
3. **Support theming with CSS variables**: `stroke="var(--syntax-function)"`, `fill="var(--bg-tertiary)"`, `fill="var(--fg-primary)"`
4. **Set `viewBox` to a size that fits all elements**. When adding elements, expand the viewBox too
5. **Define arrowheads with marker-end**:
   ```html
   <defs>
     <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
       <polygon points="0 0, 10 3, 0 6" fill="var(--syntax-function)" />
     </marker>
   </defs>
   ```
6. When there are multiple SVGs in the same HTML, make the marker ids unique (`arrowhead1`, `arrowhead2`, etc.)
7. **Draw loop-back arrows dashed** with `stroke-dasharray="5,5"` to distinguish them from forward flow

### SVG CSS class definitions (write in each SVG's `<style>`)

```css
.svg-box { fill: var(--bg-tertiary); stroke: var(--border-color); stroke-width: 2; }
.svg-text { font-size: 12px; fill: var(--fg-primary); }
.svg-arrow { fill: none; stroke: var(--syntax-function); stroke-width: 2; marker-end: url(#arrowhead); }
.svg-phase { fill: var(--syntax-decorator); stroke: var(--border-color); stroke-width: 2; }
.svg-decision { fill: var(--bg-tertiary); stroke: var(--border-color); stroke-width: 2; }
```

Always include `fill: none;` in `.svg-arrow`.

### SVG verification phase (always run immediately after creating each SVG)

Once you have created one SVG diagram, run this phase before moving on to the next segment. Check at the coordinate level whether the arrows connect correctly to their targets, and fix any misalignment.

1. **Read the end coordinates of each arrow**. For a `<line>`, that is `x2,y2`; for a `<path>`, the last coordinate (the end of `L x y` / `C ... x y`).
2. **Confirm that the boundary of the target element lands at the end point**. Match the coordinate of the target's edge (rect / polygon / circle / text) against the arrow's end point.
   - For a vertical arrow, does the end point coincide with the target rect's top edge `y` (the `y` attribute) or bottom edge `y + height`
   - For a horizontal arrow, does the end point coincide with the target rect's left edge `x` or right edge `x + width`
   - If misaligned, align the arrow's end coordinate to the target's edge (or move the target box)
3. **Leave room for the arrowhead**. Since the `marker-end` arrowhead is drawn outward from the end point, place the end point right at — or a few px before — the target's edge. Do not let it dig into the target.
4. **Confirm the start point also emerges from the edge of the origin element** (that it does not sprout from some halfway position).
5. **Confirm there is not a single arrow pointing into empty space**. Check that every exit of a branch (diamond), such as Yes / No, has a destination box.
6. **Confirm that all elements fit within the viewBox**, that no text overflows, and that the `marker` ids are unique within the HTML.
7. **Rendering check**: In an environment where a browser / screenshots are available, display the SVG and visually confirm that the arrows connect to their targets.

If you find any misalignment or disconnection, fix it, and **repeat 1–7 until all arrows connect to their targets**. Move on to the next segment only after you have confirmed the connections.

## Checklist

- [ ] Explicitly set `fill="none"` on every `<path>` (specifying it via a CSS class is fine)
- [ ] There is a target element (rect, polygon, circle, text, etc.) at the tip of every arrow
- [ ] Every exit (Yes/No) of a branch (diamond) has a destination
- [ ] Loop-back arrows are dashed with `stroke-dasharray="5,5"`
- [ ] The viewBox fits all elements, and no text overflows
- [ ] The marker ids are unique within the HTML
- [ ] Theming is supported with CSS variables
- [ ] After creating each SVG, the "SVG verification phase" was run and all arrows were confirmed to connect to their targets
