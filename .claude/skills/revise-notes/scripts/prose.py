"""Flag prose that breaks STYLE.md. Usage: python3 prose.py file.md [...]

Checks text outside code blocks: bullets that are not full sentences, long
table cells without a full stop, arrows in text, sentences over 25 words.
Short cells and cells with numbers or code are data, so they pass.
Exit 1 if anything is flagged.
"""
import re
import sys

END = (".", "?", "!", ":")


def strip(s):
    return re.sub(r"`[^`]*`", "X", s).strip()


def check(path):
    hits, code = [], False
    for n, line in enumerate(open(path, encoding="utf8"), 1):
        if line.startswith("```"):
            code = not code
            continue
        if code or not line.strip() or line.startswith("#"):
            continue
        t = strip(line)
        if re.search(r"→|->|=>|⇒", t):
            hits.append((n, "arrow in text"))
        if t.startswith("|"):
            if re.fullmatch(r"[|\s:-]+", t):
                continue
            for c in t.strip("|").split("|"):
                c = c.strip()
                data = re.search(r"[×=^/\d]", c) or c.count("X") >= 2
                if not data and len(c.split()) >= 5 and not c.endswith(END):
                    hits.append((n, f"cell is not a full sentence: {c[:50]}"))
            continue
        body = re.sub(r"^\s*(?:[-*]|\d+\.|>)\s*", "", t)
        if body != t and body and not body.rstrip("*\"')").endswith(END):
            hits.append((n, f"bullet is not a full sentence: {body[:50]}"))
        for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\*\*[^*]+\*\*", "", body)):
            if len(s.split()) > 25:
                hits.append((n, f"sentence over 25 words: {s[:50]}"))
    for n, msg in hits:
        print(f"{path}:{n}: {msg}")
    return not hits


if __name__ == "__main__":
    ok = all([check(p) for p in sys.argv[1:]])
    print("prose OK" if ok else "prose: fix the lines above")
    sys.exit(0 if ok else 1)
