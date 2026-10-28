"""Build the hub into one page for publishing as a claude.ai artifact.

Usage:  python build.py            -> dist/housemade-hub.html

hub.dc.html stays the source: it runs as-is from a local server with
support.js (python -m http.server, then open /hub.dc.html). The built page:
  - inlines the stylesheet and the runtime, so nothing else is fetched;
  - ships the template inside a <script type="text/x-dc-template"> so the
    browser's HTML parser can't rewrite it (it drops <sc-for> inside <select>);
  - runs the logic as an ordinary script instead of through new Function;
  - is a page fragment (no doctype/html/head/body), as artifacts expect.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
TITLE = "Housemade Design Hub"


def patch_runtime(js):
    """Teach support.js about the pre-built template and logic. Each patch
    must match exactly once, so a runtime update can't silently skip one."""
    patches = [
        ("      template: dc.innerHTML,",
         "      template: (doc.querySelector('script[type=\"text/x-dc-template\"]') || dc).textContent || dc.innerHTML,"),
        ("  function evalDcLogic(src) {\n",
         "  function evalDcLogic(src) {\n"
         "    if (window.__dcLogicFactory) return window.__dcLogicFactory(StreamableLogic, StreamableLogic, getReact());\n"),
    ]
    for old, new in patches:
        if js.count(old) != 1:
            raise SystemExit(f"runtime patch did not match exactly once: {old.strip()[:60]!r}")
        js = js.replace(old, new)
    return js


def main():
    src = (HERE / "hub.dc.html").read_text(encoding="utf-8")
    css = (HERE / "styles" / "housemade.css").read_text(encoding="utf-8")
    css = re.sub(r"^@import[^\n]*\n", "", css, flags=re.M)  # the helmet's font link loads these
    runtime = patch_runtime((HERE / "support.js").read_text(encoding="utf-8"))

    open_tag = re.search(r"<x-dc(?:\s[^>]*)?>", src)
    template = src[open_tag.end():src.rindex("</x-dc>")]
    template = template.replace('<link rel="stylesheet" href="styles/housemade.css">\n', "")
    script = re.search(r'(<script type="text/x-dc" data-dc-script[^>]*>)(.*?)</script>', src, re.S)
    props_tag, logic = script.group(1), script.group(2)

    for name, text in (("template", template), ("logic", logic), ("runtime", runtime)):
        if re.search(r"</script|<!--", text, re.I):
            raise SystemExit(f"{name} contains </script or <!-- and can't be inlined in a script tag")

    page = "\n".join([
        f"<title>{TITLE}</title>",
        f"<style>{css}</style>",
        "<script>window.__resources = {};</script>",
        "<script>window.__dcLogicFactory = function (DCLogic, StreamableLogic, React) {\n"
        + logic + "\n;return Component;\n};</script>",
        f"<script>{runtime}</script>",
        "<x-dc></x-dc>",
        f'<script type="text/x-dc-template">{template}</script>',
        f"{props_tag}// Logic is pre-built into window.__dcLogicFactory above.</script>",
    ])
    out = HERE / "dist" / "housemade-hub.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out.relative_to(HERE)} ({len(page) // 1024} KB)")


if __name__ == "__main__":
    main()
