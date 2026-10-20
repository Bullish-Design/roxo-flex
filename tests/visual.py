"""Render desktop and mobile pages with Chromium and check responsive behavior."""
import http.server
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

root = Path(sys.argv[1])
shots = Path(os.environ.get("ROXO_SCREENSHOT_DIR", root / "_screenshots"))
shots.mkdir(parents=True, exist_ok=True)

probe = '''<script>
window.addEventListener("load", function () {
  const nav = document.querySelector(".site-nav");
  const label = document.querySelector(".nav-toggle-label");
  const toggle = document.querySelector(".nav-toggle");
  const body = document.body;
  body.dataset.width = window.innerWidth;
  body.dataset.overflow = document.documentElement.scrollWidth - window.innerWidth;
  body.dataset.navClosed = getComputedStyle(nav).display;
  body.dataset.fontBody = getComputedStyle(body).fontFamily;
  body.dataset.fontHeading = getComputedStyle(document.querySelector("h1")).fontFamily;
  const icon = document.querySelector(".site-icon");
  body.dataset.iconMask = icon ? getComputedStyle(icon).maskImage : "none";
  const button = document.querySelector(".button");
  const buttonIcon = button && button.querySelector(".site-icon");
  body.dataset.buttonColor = button ? getComputedStyle(button).color : "none";
  body.dataset.buttonIconColor = buttonIcon ? getComputedStyle(buttonIcon).backgroundColor : "none";
  const menuIcon = document.querySelector(".menu-icon");
  const closeIcon = document.querySelector(".menu-close-icon");
  body.dataset.menuIconClosed = menuIcon ? getComputedStyle(menuIcon).display : "none";
  body.dataset.closeIconClosed = closeIcon ? getComputedStyle(closeIcon).display : "none";
  body.dataset.label = getComputedStyle(label).display;
  toggle.checked = true;
  body.dataset.navOpen = getComputedStyle(nav).display;
  body.dataset.menuIconOpen = menuIcon ? getComputedStyle(menuIcon).display : "none";
  body.dataset.closeIconOpen = closeIcon ? getComputedStyle(closeIcon).display : "none";
});
</script></body>'''
for site in ("neutral", "muted"):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(root / site), **kwargs)
        def log_message(self, *_args):
            pass
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    try:
        source = (root / site / "index.html").read_text()
        (root / site / "probe.html").write_text(source.replace("</body>", probe))
        for viewport, width, height in (("desktop", 1440, 900), ("mobile", 390, 844)):
            url = f"http://127.0.0.1:{port}/probe.html"
            with tempfile.TemporaryDirectory() as profile:
                base = ["chromium", "--headless", "--no-sandbox", "--disable-gpu",
                        "--disable-dev-shm-usage", "--no-first-run", "--hide-scrollbars",
                        f"--user-data-dir={profile}", f"--window-size={width},{height}",
                        "--virtual-time-budget=1000"]
                result = subprocess.run(base + ["--dump-dom", url], capture_output=True,
                                        text=True, timeout=30)
                assert result.returncode == 0, result.stderr[-1000:]
                html = result.stdout
                import re
                def value(key):
                    match = re.search(rf'data-{key}="([^"]+)"', html)
                    assert match, (site, viewport, key)
                    return match.group(1)
                assert int(value("overflow")) <= 1, (site, viewport, value("overflow"))
                assert "Georgia" in value("font-heading")
                assert ("Arial" if site == "muted" else "system-ui") in value("font-body")
                assert "/icons/" in value("icon-mask"), (site, viewport, value("icon-mask"))
                assert value("button-color") == value("button-icon-color")
                if viewport == "desktop":
                    assert value("nav-closed") == "flex"
                    assert value("label") == "none"
                else:
                    assert value("nav-closed") == "none"
                    assert value("nav-open") == "flex"
                    assert value("label") == "flex"
                    if site == "muted":
                        assert value("menu-icon-closed") == "block"
                        assert value("close-icon-closed") == "none"
                        assert value("menu-icon-open") == "none"
                        assert value("close-icon-open") == "block"
                image = shots / f"{site}-{viewport}.png"
                result = subprocess.run(base + [f"--screenshot={image}",
                                        f"http://127.0.0.1:{port}/"],
                                        capture_output=True, timeout=30)
                assert result.returncode == 0, result.stderr[-1000:]
                with image.open("rb") as file:
                    header = file.read(24)
                assert header[:8] == b"\x89PNG\r\n\x1a\n"
                actual_width, actual_height = struct.unpack(">II", header[16:24])
                assert actual_width >= width - 100 and actual_height >= height - 100
                print(f"{site} {viewport}: {actual_width}x{actual_height}, no overflow, navigation passed")
        for page in ("contact", "project_areas/north/community-hub"):
            target = root / site / page
            source = (target / "index.html").read_text()
            (target / "probe.html").write_text(source.replace("</body>", probe))
            with tempfile.TemporaryDirectory() as profile:
                base = ["chromium", "--headless", "--no-sandbox", "--disable-gpu",
                        "--disable-dev-shm-usage", f"--user-data-dir={profile}",
                        "--window-size=390,844", "--virtual-time-budget=1000"]
                result = subprocess.run(base + ["--dump-dom",
                    f"http://127.0.0.1:{port}/{page}/probe.html"],
                    capture_output=True, text=True, timeout=30)
                assert result.returncode == 0, result.stderr[-1000:]
                import re
                overflow = re.search(r'data-overflow="(-?\d+)"', result.stdout)
                assert overflow and int(overflow.group(1)) <= 1, (site, page)
                expected = "<form" if page == "contact" else "project-gallery"
                assert expected in result.stdout, (site, page)
                print(f"{site} mobile {page}: no overflow, content passed")
        preview_page = "projects/wayfinding"
        preview_source = (root / site / preview_page / "index.html").read_text()
        preview_probe = '''<script>
window.addEventListener("load", function () {
  const preview = document.querySelector(".link-preview");
  const link = preview.querySelector("a");
  const toggle = preview.querySelector(".link-preview__toggle");
  const card = preview.querySelector(".link-preview__card");
  const body = document.body;
  const columns = document.querySelector(".content-columns");
  body.dataset.columnCount = getComputedStyle(columns).gridTemplateColumns.split(" ").length;
  body.dataset.previewLink = link.getAttribute("href");
  body.dataset.previewReady = !toggle.hidden && card.hidden;
  preview.dispatchEvent(new PointerEvent("pointerenter", {pointerType: "mouse"}));
  body.dataset.previewHover = !card.hidden;
  preview.dispatchEvent(new PointerEvent("pointerleave", {pointerType: "mouse"}));
  setTimeout(function () {
    body.dataset.previewLeft = card.hidden;
    preview.dispatchEvent(new PointerEvent("pointerenter", {pointerType: "touch"}));
    body.dataset.previewTouch = card.hidden;
    toggle.click();
    body.dataset.previewClick = !card.hidden && toggle.getAttribute("aria-expanded") === "true";
    body.dataset.previewPosition = getComputedStyle(card).position;
    body.dataset.previewOverflow = document.documentElement.scrollWidth - window.innerWidth;
    card.querySelector(".link-preview__close").click();
    body.dataset.previewClose = card.hidden;
    toggle.click();
    document.dispatchEvent(new KeyboardEvent("keydown", {key: "Escape"}));
    body.dataset.previewEscape = card.hidden && toggle.getAttribute("aria-expanded") === "false";
  }, 200);
});
</script></body>'''
        (root / site / preview_page / "probe.html").write_text(
            preview_source.replace("</body>", preview_probe)
        )
        for viewport, width, height in (("desktop", 1440, 900), ("mobile", 390, 844)):
            with tempfile.TemporaryDirectory() as profile:
                base = ["chromium", "--headless", "--no-sandbox", "--disable-gpu",
                        "--disable-dev-shm-usage", f"--user-data-dir={profile}",
                        f"--window-size={width},{height}", "--virtual-time-budget=1000"]
                result = subprocess.run(base + ["--dump-dom",
                    f"http://127.0.0.1:{port}/{preview_page}/probe.html"],
                    capture_output=True, text=True, timeout=30)
                assert result.returncode == 0, result.stderr[-1000:]
                for field in ("ready", "hover", "left", "touch", "click", "close", "escape"):
                    assert f'data-preview-{field}="true"' in result.stdout, (site, viewport, field)
                assert 'data-preview-link="/portfolio/field-guide/"' in result.stdout
                expected_columns = 1 if viewport == "mobile" else 2
                assert f'data-column-count="{expected_columns}"' in result.stdout
                assert 'data-preview-position="fixed"' in result.stdout
                match = re.search(r'data-preview-overflow="(-?\d+)"', result.stdout)
                assert match and int(match.group(1)) <= 1, (site, viewport, "preview overflow")
                open_script = '''<script>
window.addEventListener("load", function () {
  document.querySelector(".link-preview__toggle").click();
});
</script></body>'''
                (root / site / preview_page / "open.html").write_text(
                    preview_source.replace("</body>", open_script)
                )
                image = shots / f"{site}-{viewport}-preview.png"
                shot = subprocess.run(base + [f"--screenshot={image}",
                    f"http://127.0.0.1:{port}/{preview_page}/open.html"],
                    capture_output=True, timeout=30)
                assert shot.returncode == 0, shot.stderr[-1000:]
                with image.open("rb") as file:
                    assert file.read(8) == b"\x89PNG\r\n\x1a\n"
                print(f"{site} {viewport} preview: hover, click, Escape, link, and fit passed")
    finally:
        server.shutdown()
