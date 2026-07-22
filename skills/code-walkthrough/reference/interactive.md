# Code Walkthrough — Interactive features

All interactive behavior is already implemented in `assets/template.html`. Do not re-implement or remove it. This file lists the expected behavior so you can verify the output.

| Feature | Behavior |
|---|---|
| Fixed sidebar TOC | Fixed left at 280px (`position: fixed`, does not scroll with the body). The visible segment is highlighted via IntersectionObserver. Hidden at 768px and below; opened via the hamburger button |
| TOC toggle | The "Contents" header button hides/shows the sidebar; the body becomes full width when hidden |
| Progress bar | Fixed at the very top; width follows the scroll position |
| View modes | "Code + Explanation" (default) / "Code Only" / "Explanation Only" |
| Expand/collapse | Clicking a segment header toggles it; "Expand"/"Collapse" buttons toggle all segments (active tab only in multi-file mode) |
| Copy button | Top right of each code block; copies the code text to the clipboard |
| Smooth scrolling | TOC links scroll smoothly; segments have `scroll-margin-top` so anchors land below the fixed header |

What you still provide:

- Static TOC links at the `TOC INSERTION POINT` (one per segment; multi-file links use `scrollToSeg`, see `reference/multi-file-tabs.md`)
- The initial expand state: render every `segment-body` expanded (no `collapsed` class)
