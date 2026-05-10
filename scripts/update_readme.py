import json
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

def get_title(folder_path, folder_name):
    meta = os.path.join(folder_path, "meta.json")
    if os.path.exists(meta):
        with open(meta) as f:
            data = json.load(f)
        if "title" in data:
            return data["title"]
    return to_title(folder_name)

def find_talks(slides_dir):
    entries = []
    for d in sorted(os.listdir(slides_dir)):
        path = os.path.join(slides_dir, d)
        if not os.path.isdir(path) or d.startswith("."):
            continue
        if os.path.exists(os.path.join(path, "index.html")):
            entries.append((d, "index"))
        elif os.path.exists(os.path.join(path, "talk.html")):
            entries.append((d, "talk"))
    return entries

talks = find_talks(SLIDES_DIR)

rows = []
for t, html_type in talks:
    title = get_title(os.path.join(SLIDES_DIR, t), t)
    url = f"{BASE_URL}/{t}/" if html_type == "index" else f"{BASE_URL}/{t}/talk.html"
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
