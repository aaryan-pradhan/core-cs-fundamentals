# Note style guide

These are revision notes. The reader has already studied the topic. They read a note top to bottom on GitHub and explain it aloud to a friend. Every note must be fast to scan, clear, and still exhaustive.

## 1. Skeleton

- The source PDF (`<subject>/src/`) is the skeleton. Keep its order, sections and `1.` / `a.` numbering.
- Rewrite the PDF's own lines into short, simple, complete sentences too. Split a long sentence into a few short ones or a bullet list. Keep every fact.
- Each section heading in the PDF becomes a `##` heading.
- Put lecture extras as short sub-points under the PDF line they explain.

## 2. No fact is lost

- Every fact in the old note must appear in the new note.
- Cut only wording: repetition, recaps, transitions ("Before X, we must..."), and filler.
- Delete an extra only if it repeats the PDF line above it.

## 3. Plain English

- One idea per sentence.
- Short, complete sentences. No sentence fragments ("Bulky and complex app." becomes "Apps become bulky and complex."). A bold label before a colon is fine.
- Active voice.
- Common words. No shortcuts like "mgmt", "HW", "w/".
- No arrows or symbols in text. Write the word instead ("so", "then", "gives").
- Write like the source PDF: simple, short, direct.

## 4. Stories and examples

- Keep the fact a story proves. Drop the storytelling.
- Keep the names of the example in a few words (e.g. "TikTok and PUBG") so the example is still recognizable.
- If a story shows a structure (memory layout, a flow, a hierarchy), draw a small diagram instead.

## 5. Analogies

- Keep each analogy as one line, e.g. "**Analogy:** a bank clerk. You ask the clerk, the clerk goes to the vault."

## 6. Interview remarks

- Keep them. Put them in a callout:

  > **Interview:** An OS does two things. It hides hardware complexity, and it manages resources.

## 7. Layout (GitHub rendering)

- Start each bullet with its key term in bold, then a colon: "**Memory protection:** ...".
- Bold at most about 30% of text. Reading only the bold should still give the main points.
- Use a table for every comparison (A vs B, list of types with properties).
- Leave a blank line between groups. No walls of text.
- At most two levels of nesting below a PDF point.

## 8. Diagrams, code, images

- Keep existing ASCII diagrams, code blocks, and `img/` images.
- Arrows are fine inside diagrams.

## 9. Do not add

- No recall questions or quizzes.
- No meta remarks like "this lecture" or "every later lecture uses this". Keep any fact attached to them.
