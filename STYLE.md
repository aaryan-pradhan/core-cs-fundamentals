# Note style guide

These notes are the revision sheet for an SDE-1 interview round of 45 to 50 minutes. There is no separate revision sheet. A reader should finish any file in 10 to 20 minutes. The basics must be stable, clear and correct.

The model files are `hld/04` (concept), `hld/16` (design rules) and `hld/26` (design). When a rule here is unclear, copy what they do.

## 1. Content

- **Source only:** Use only the subject's own notes (`os/src/`, `dbms/src/`, `hld/slides/`). Add nothing from outside them.
- **Basics only:** Cover every topic the source teaches, but keep only its basics. Cut anything an SDE-1 interview would not ask, even when the source has it.
- **Correct facts:** Fix a wrong fact. Never keep it.
- **No code:** Leave out code unless one line is itself the answer, such as a SQL query. LLD notes keep their code.
- **No extras:** Add no quizzes, recaps or meta remarks like "this lecture". The "Likely questions" section is the only drill.

## 2. Sentences

- **Full sentences:** Every bullet, prose table cell and answer is a complete sentence. Short is fine. Cells that hold data (field names, numbers, code, product names) may stay short.
- **Define before use:** Give each term a brief definition at its first use, in the Key terms table or inline. Never use a term before it is defined.
- **Define once:** Never repeat a definition. A later file points back instead, for example "(topic 14)".
- **Plain English:** Write one idea per sentence, in active voice, with common words. Do not shorten words ("mgmt", "HW", "w/").
- **No arrows in text:** Write "so", "then" or "gives" instead. Arrows are fine inside diagrams.
- **No analogies or stories:** State what the thing is and how it works. Keep an example's name in a few words, such as "TikTok and PUBG".
- **Bold labels:** Start a bullet with its key term in bold and a colon. Bold at most about 30% of the text.

## 3. Concept file layout

Use these sections in this order. Drop a section only when the source has nothing for it.

1. **Title:** `# N. Topic name`.
2. **Intro:** One to three sentences say what the topic is and why it matters.
3. **Key terms:** A table of `Term | Meaning`. Each meaning is a full sentence, such as "Latency is the time one request takes."
4. **How it works:** A numbered chain. Each step names a problem in bold, then its fix. When the topic is a process, number the steps of the process instead.
5. **Diagram:** One diagram shows the structure or flow, if the topic has one.
6. **Trade-offs:** A table compares the options. Use a table for every comparison.
7. **Numbers:** One line gives the numbers the source states.
8. **Interview:** One `> **Interview:**` callout gives the line to say in the interview.
9. **Likely questions:** Four or five bold questions, each with a one- or two-sentence answer.

## 4. Design file layout (HLD only)

Follow the 7 steps in `hld/16`. Each design covers only the basics, like the handwritten Rapido design.

1. **FR:** Write three "User should be able to ..." lines. Then one sentence lists what is out of scope.
2. **NFR:** Choose CAP and give one latency target.
3. **Estimates:** Work out DAU, users per second (DAU / 10^5), and read and write QPS with a peak of 5 times. One sentence says what the numbers mean.
4. **Entities:** A table lists each entity and its key fields.
5. **APIs:** Write one endpoint per FR, each as a sentence.
6. **Basic diagram:** Draw it, then end with "With this design, FRs are satisfied."
7. **Problems:** Fix three or four problems. Each starts with the problem in bold, then its fix. A final diagram shows the fixed design.

End with the Interview callout and four likely questions.

## 5. Diagrams

- **Mermaid:** Draw flows, states and architectures as Mermaid blocks. Use at most two per file.
- **Labels:** Quote every label, and label every arrow as `-->|"label"|`. Do not put `#` or `;` in a label. Do not use `end` as a node id.
- **Images:** Keep an `img/` image only when it shows a basic.

### DBMS ER diagrams

- ER diagrams use Chen notation, drawn with PlantUML `@startchen`. Keep the source in `dbms/img/src/<lec>-<name>.puml`. Render it to `dbms/img/<lec>-<name>.svg` and embed the SVG.
- Chen mode cannot draw an is-a triangle, an aggregation box, a dashed partial-key underline or a double total-participation line. For those, write Graphviz DOT inside `@startdot` in the same `.puml` file.
- Render with `plantuml -tsvg dbms/img/src/*.puml -o ..`. `@startdot` needs Graphviz (`dot`) installed.
