import asyncio
import os
from pathlib import Path

SLIDES_DIR = Path(__file__).parent.parent / "slides"
WIDTH, HEIGHT = 1280, 720


async def screenshot_slide(name, html_path, out_path):
    from playwright.async_api import async_playwright

    out_path.parent.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        await page.goto(f"file://{html_path.resolve()}", wait_until="networkidle", timeout=30000)
        await page.screenshot(path=str(out_path), type="jpeg", quality=85)
        await browser.close()
    print(f"  generated: {name}")


async def main():
    jobs = []
    for folder in sorted(SLIDES_DIR.iterdir()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        thumb = folder / "assets" / "thumbnail.jpeg"
        if thumb.exists():
            continue
        for candidate in ("index.html", "talk.html"):
            html = folder / candidate
            if html.exists():
                jobs.append((folder.name, html, thumb))
                break

    if not jobs:
        print("All thumbnails already exist, nothing to do.")
        return

    for name, html, thumb in jobs:
        try:
            await screenshot_slide(name, html, thumb)
        except Exception as e:
            print(f"  skipped {name}: {e}")


asyncio.run(main())
