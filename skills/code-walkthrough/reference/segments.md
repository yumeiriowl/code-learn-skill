# Code Walkthrough — Segment splitting and structure of each segment

## Segment splitting rules

Split the code from the top in order, into the following processing units.

### List of segment types

| Segment type | Badge color | Description |
|---|---|---|
| `imports` | `#61afef` (blue) | Blocks of import / require / include statements |
| `constants` | `#d19a66` (orange) | Constant definitions, config values, enums, prompt templates |
| `types` | `#c678dd` (purple) | Type definitions, interface, type alias, struct |
| `class` | `#e5c07b` (yellow) | Class definitions (including all methods) |
| `function` | `#98c379` (green) | Function/method definitions |
| `main` | `#e06c75` (red) | Main logic, entry point, if __name__, etc. |
| `config` | `#56b6c2` (cyan) | Config files, decorators, middleware registration |
| `other` | `#abb2bf` (gray) | Code not covered by the above |

### Basic splitting policy

- Read the code from the top in order, and split it by semantic groupings
- Combine consecutive import statements into a single `imports` segment
- Make a class definition a single segment for the whole class (do not split methods into separate segments)
- As a rule, one function per `function` segment
- Merge short segments of fewer than 3 lines into the related segment before or after
- Include blank lines and comment-only lines in the segment that immediately follows
- Include the file's leading doc comment in the `imports` segment

### Language-specific hints

- **Python**: `import`, `from ... import`, `def`, `class`, `if __name__`, decorators (`@`)
- **JavaScript/TypeScript**: `import`, `require`, `export`, `function`, `class`, top-level `const`/`let`
- **Java**: `import`, `package`, `public class`, method definitions, `public static void main`
- **Go**: `import`, `type`, `func`, `func main`

## Structure of each segment

Compose each segment from the following elements.

### 1. Segment header

- Segment-type badge (using the color codes above)
- Segment title (a concise title that captures the content, in the language of the user's request)
- Line-number range (e.g., `L1-15`)
- Expand/collapse toggle

### 2. Code block

- Display the original source code in full, exactly as is. Do not omit or excerpt
- Preserve indentation
- With line numbers
- Apply CSS-based simple syntax highlighting
- With a copy button

### 3. Commentary

Write the commentary at a level of detail where the reader can concretely picture what the code does.

- Explain in detail what that segment does, in the language of the user's request (e.g., English for an English request, Japanese for a Japanese request)
- Key points of important logic, algorithms, and design decisions
- Data flow (input → processing → output)
- Relationships with other segments (e.g., "this function is called from the class defined in segment 3")
- Caveats and room for improvement
- At least 5 sentences per segment. For classes or complex functions, 10 or more
- When the processing flow is complex, insert an SVG diagram (see "SVG diagram generation rules")
- For technical terms that even a general engineer would find hard to understand without specialized knowledge (e.g., idempotency, backpressure, memoization, vector embeddings, etc.), underline them with `<span class="term" data-term="key">term</span>` and register the overview in `GLOSSARY` (see "Glossary panel"). Do not attach it to common words (variables, functions, loops, etc.)

## Checklist

### Code embedding

- [ ] Include the full code in the HTML. Do not omit or excerpt
- [ ] Embed the code as static HTML inside `<pre><code>` tags. Do not use JS template literals (backticks)
- [ ] Escape `<`, `>`, `&`, `"` into HTML entities
- [ ] Write all line numbers inside `<pre>`, separated by newlines

### Commentary

- [ ] Write the commentary in the language of the user's request (match the request language)
- [ ] At least 5 sentences per segment. Commentary that is too short is not allowed
- [ ] Insert an SVG flow diagram for complex processing
- [ ] Describe the data flow (input → processing → output) concretely
- [ ] Underline technical terms that require specialized knowledge with `<span class="term">`, and register their overviews in `GLOSSARY` (see "Glossary panel")
