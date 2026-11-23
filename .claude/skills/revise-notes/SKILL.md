---
name: revise-notes
description: Rewrites lecture notes in core-cs-fundamentals (hld, os, dbms, and any new subject such as computer networks) to the repo's SDE-1 revision style. The style keeps source-only basics, uses full sentences, defines each term once, and follows a fixed concept layout and a 7-step HLD design layout. Use when asked to revise, rewrite, cut, simplify or convert a note or a whole subject folder, or to write a new note in this repo.
---

# Revise notes

The rules live in `STYLE.md` at the repo root. The model files are `hld/04-performance-throughput-load-balancing.md` (concept), `hld/16-interview-framework.md` (design rules) and `hld/26-whatsapp.md` (design). Read all four before writing anything.

## Setup (once per machine)

```sh
cd .claude/skills/revise-notes/scripts && npm install
```

## Whole subject

- [ ] **Plan first:** Propose the cheapest plan in a few lines: which files, which source pages, inline or agents, which model. Start only after the user agrees.
- [ ] **Map sources:** Pair each note file with its source pages. The source is the truth. `hld/slides/` is gitignored, so never commit it.
- [ ] **Glossary:** Walk the files in order and list where each term is first defined. A later file must not define it again.
- [ ] **Pilot:** Rewrite one concept file (plus one design file in HLD). Commit it and stop for the user's review.
- [ ] **Roll out:** After approval, agents may write files in parallel. Give each agent `STYLE.md`, the model files, its file, its source pages and the glossary. The main session runs the checks and commits each file, so git locks never clash.
- [ ] **README:** Update the subject README when a title changes.
- [ ] **Push:** Push once at the end.

## One file

1. **Pick the basics:** List what the source teaches on this topic. Drop anything an SDE-1 round would not ask.
2. **List the terms:** Every term not defined in an earlier file goes in Key terms or gets an inline definition at first use.
3. **Fill the layout:** Use the concept layout or the design layout from `STYLE.md`. Write full sentences.
4. **Check:** Run both scripts. Fix every flagged line.

   ```sh
   S=.claude/skills/revise-notes/scripts
   python3 $S/prose.py <file> && node $S/mermaid.mjs <file>
   ```

5. **Read it as the learner:** Every term is defined before it is used. Every number adds up. The file reads in 10 to 20 minutes.
6. **Commit:** Commit the one file to main with a subject like "Cut OS topic 9 to basics". Add no Claude attribution.

## Checks the scripts cannot do

- **Undefined terms:** Search the file for each acronym. Confirm that it, or an earlier file, defines it.
- **Facts:** Each fact matches the source. Fix a wrong fact; never invent a new one.
- **Size:** A concept file runs about 60 lines. A design file runs about 80 lines.
