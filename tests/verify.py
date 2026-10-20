"""Check links, sections, branding, forms, and custom layouts in both builds."""
import re
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

source, output, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
config = tomllib.loads((source / "hugo.toml").read_text())
front = (source / "content/_index.md").read_text().split("+++", 2)[1]
home = tomllib.loads(front)

class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.sections = []
        self.forms = []
        self.inputs = []
        self.nav = []
        self.in_nav = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "nav" and values.get("class") == "site-nav":
            self.in_nav = True
        if tag == "section" and values.get("id"):
            self.sections.append(values["id"])
        if tag == "form":
            self.forms.append(values)
        if tag in ("input", "textarea"):
            self.inputs.append(values.get("name"))
        if tag == "a" and self.in_nav:
            self.nav.append(values.get("href"))
        for attr in ("href", "src"):
            value = values.get(attr)
            if value and not value.startswith(("#", "mailto:", "tel:", "data:")):
                self.references.append(value)

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_nav = False

pages = {}
for path in output.rglob("*.html"):
    parser = Elements()
    parser.feed(path.read_text())
    pages[path] = parser
    for reference in parser.references:
        parsed = urlparse(reference)
        if parsed.scheme or parsed.netloc:
            continue
        target = output / parsed.path.lstrip("/")
        if target.is_dir():
            target = target / "index.html"
        elif not target.suffix:
            target = target / "index.html"
        assert target.exists(), f"{path}: missing {reference}"

index = (output / "index.html").read_text()
main = pages[output / "index.html"]
assert config["params"]["business_name"] in index
assert "nav-toggle" in index and "site-nav" in index
assert len(main.nav) == len(config["menu"]["main"])
assert (output / config["params"]["custom_css"]).exists()
assert (output / config["params"]["favicon"]).exists()
expected = [item for item in home["sections"] if home[item]["enabled"]]
assert main.sections == expected, (main.sections, expected)
assert "--button-radius:" in index and "--color-accent:" in index
contact = pages[output / "contact/index.html"]
assert len(contact.forms) == 1
assert contact.forms[0]["action"] == config["params"]["contact"]["form_endpoint"]
assert contact.forms[0]["method"] == "post"
assert {"name", "email", "message"}.issubset(contact.inputs)
for path in (
    "portfolio/field-guide/index.html",
    "projects/wayfinding/index.html",
    "project_areas/index.html",
    "project_areas/north/index.html",
    "project_areas/north/community-hub/index.html",
):
    assert (output / path).exists(), path
assert "project-gallery" in (output / "project_areas/north/community-hub/index.html").read_text()
assert "Northern area" in (output / "project_areas/index.html").read_text()
assert "Community hub" in (output / "project_areas/north/index.html").read_text()
assert "project-gallery" in (output / "projects/wayfinding/index.html").read_text()
assert "Wayfinding" in (output / "projects/index.html").read_text()
assert "Field Guide" in (output / "portfolio/index.html").read_text()
css = (output / "css/theme.css").read_text()
assert "@media(max-width:800px)" in css and "@media(max-width:540px)" in css
assert ".nav-toggle:checked~.site-nav" in css
if name == "muted":
    assert "filter: grayscale(1)" in (output / "css/site.css").read_text()
    assert "id=\"team\"" not in index
print(f"{name}: {len(pages)} pages, links, images, sections, form, layouts, and responsive styles passed")
