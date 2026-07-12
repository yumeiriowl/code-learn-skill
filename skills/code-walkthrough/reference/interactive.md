# Code Walkthrough — Interactive features

## Interactive features

### 1. Fixed sidebar TOC

- Fixed on the left at 280px (on desktop)
- Links to each segment (with the color code of the segment-type badge)
- Highlight the currently visible segment with IntersectionObserver
- On mobile, open/close it via a hamburger menu

Fix the sidebar with `position: fixed`. Do not use `position: sticky` or normal flow, because the table of contents would be dragged along with the body scroll and move together with it (align it with the glossary panel's same `position: fixed`). Since it is fixed and overlaps the page content, add `margin-left: 280px` to `.main` to make room for the body.

```css
.sidebar{
  position: fixed; top: 60px; left: 0;   /* top is the header height. 88px in the multi-file case */
  width: 280px; height: calc(100vh - 60px);
  overflow-y: auto;                      /* If the TOC is long, scroll only within the sidebar */
}
.main{ margin-left: 280px; }             /* Make room for the width of the fixed sidebar */
@media (max-width: 768px){
  .sidebar{ display: none; }
  .main{ margin-left: 0; }
}
```

### 1b. TOC display toggle

Open/close the sidebar with the "Contents" button (`#tocToggleBtn`) in the header. When closed, reset `.main`'s `margin-left` to 0 to make the body full width. The initial state on desktop is shown.

```css
.sidebar.hidden{ display: none; }
.main.toc-hidden{ margin-left: 0; }
```

```javascript
document.getElementById('tocToggleBtn').addEventListener('click', () => {
  document.getElementById('sidebar').classList.toggle('hidden');
  document.getElementById('mainContent').classList.toggle('toc-hidden');
});
```

### 2. Scroll-linked progress bar

- Fixed at the very top of the page
- The width changes according to the scroll position

### 3. View mode switching

Three modes: "Code + Explanation" (default) / "Code Only" / "Explanation Only"

### 4. Expand all / collapse all

Individual toggle by clicking each segment's header + a bulk button

### 5. Copy button

A copy button at the top right of each code block. Uses `navigator.clipboard.writeText()`.

### 6. Smooth scrolling

`html { scroll-behavior: smooth; }` + `scrollIntoView({ behavior: 'smooth' })`
