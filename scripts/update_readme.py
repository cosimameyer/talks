import os
import re

BASE_URL = "https://cosimameyer.github.io/talks/slides"
SKIP = {".github", ".git", "scripts"}

def to_title(name):
    return name.replace("-", " ").replace("_", " ").title()

talks = sorted(
    d for d in os.listdir(".")
    if os.path.isdir(d)
    and not d.startswith(".")
    and d not in SKIP
    and os.path.exists(os.path.join(d, "index.html"))
)

rows = "\n".join(
    f"| 🎤 **{to_title(t)}** | [`{t}`]({BASE_URL}/{t}/) |"
    for t in talks
)

block = (
    "<!-- TALKS_START -->\n"
    "_Auto-generated — do not edit this section manually._\n\n"
    "| Talk | Slides |\n"
    "|:-----|:------:|\n"
    f"{rows}\n\n"
    "<!-- TALKS_END -->"
)

with open("README.md", "r") as f:
    readme = f.read()

updated = re.sub(
    r"<!-- TALKS_START -->.*?<!-- TALKS_END -->",
    block,
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w") as f:
    f.write(updated)