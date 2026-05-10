import os
import re

BASE_URL = "https://cosimameyer.github.io/talks/slides"
SLIDES_DIR = os.path.join(os.path.dirname(__file__), "..", "slides")

def to_title(name):
    parts = name.replace("-", " ").replace("_", " ").split()
    stop = {"a", "an", "the", "and", "or", "of", "in", "at", "for", "to"}
    return " ".join(
        p.upper() if p.isdigit() or (len(p) <= 4 and p.lower() in {"wids", "nlp", "ml", "ai", "r", "py"})
        else p.capitalize() if i == 0 or p.lower() not in stop
        else p
        for i, p in enumerate(parts)
    )

talks = sorted(
    d for d in os.listdir(SLIDES_DIR)
    if os.path.isdir(os.path.join(SLIDES_DIR, d))
    and not d.startswith(".")
    and os.path.exists(os.path.join(SLIDES_DIR, d, "index.html"))
)

rows = []
for t in talks:
    title = to_title(t)
    url = f"{BASE_URL}/{t}/"
    thumb_rel = f"slides/{t}/assets/thumbnail.jpeg"
    thumb_abs = os.path.join(SLIDES_DIR, t, "assets", "thumbnail.jpeg")
    if os.path.exists(thumb_abs):
        img = f'<img src="{thumb_rel}" width="160" alt="{title} thumbnail">'
        rows.append(
            f"| {img} | **[{title}]({url})** |"
        )
    else:
        rows.append(f"| | **[{title}]({url})** |")

table = "\n".join(rows)

block = (
    "<!-- TALKS_START -->\n"
    "_Auto-generated — do not edit this section manually._\n\n"
    "| Preview | Talk |\n"
    "|:-------:|:-----|\n"
    f"{table}\n\n"
    "<!-- TALKS_END -->"
)

readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
with open(readme_path, "r") as f:
    readme = f.read()

updated = re.sub(
    r"<!-- TALKS_START -->.*?<!-- TALKS_END -->",
    block,
    readme,
    flags=re.DOTALL,
)

with open(readme_path, "w") as f:
    f.write(updated)

print(f"Updated README with {len(talks)} talk(s).")
