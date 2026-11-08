"""Wrap the artifact source (coachbuilder.html, no document skeleton) into a standalone index.html for GitHub Pages / local use.

The artifact keeps its jsDelivr +esm imports. The standalone page imports the plain npm files of
three.js r170 from jsDelivr through an import map that pins each file's SHA-384 hash, so a changed
file fails to load. It also ships a Content-Security-Policy that allows only jsDelivr for scripts,
its own inline scripts (by hash), and Google Fonts.

To move to another three.js version: download the npm package (npm pack three@<version>), set
THREE_VERSION, and replace each hash with: openssl dgst -sha384 -binary <file> | openssl base64 -A
"""
import base64
import hashlib
import json
import pathlib
import re

THREE_VERSION = "0.170.0"
BASE = f"https://cdn.jsdelivr.net/npm/three@{THREE_VERSION}"
# Module specifier -> (path inside the npm package, SHA-384 of that file).
FILES = {
    "three": ("build/three.module.min.js", "sha384-IDC7sAMAIMB/TZ6dgKKPPAKZ2bXXXP8+FBMBC8cU319eBhKITx+PaalhfDkDNH28"),
    "three/addons/controls/OrbitControls.js": ("examples/jsm/controls/OrbitControls.js", "sha384-aJoe4qqS/DgF2jh9njAuvA6QIveJYoCuYOfYjdFY8P3eawzmc9bEQ40jq2TvOyuP"),
    "three/addons/exporters/GLTFExporter.js": ("examples/jsm/exporters/GLTFExporter.js", "sha384-cmiUVRZWWohnebNbGOmBZ2huvu6QROAG9Q2MkU7WyFkieWzfb6CX/UCQTpNCv95/"),
    "three/addons/exporters/STLExporter.js": ("examples/jsm/exporters/STLExporter.js", "sha384-asFNg7wL3Pl1xb8Wnx91cfhJVpmwKWIfOBKZaXNqPDWTLajmNiNQWXd5sP71UzcR"),
    "three/addons/environments/RoomEnvironment.js": ("examples/jsm/environments/RoomEnvironment.js", "sha384-9ItPPH2vgKbkvgrqTKq7ptGYe+WuAnqlZtlqleJW4/CJjnM5R7C+efD6iS7ADPJ9"),
}
# CDN import in coachbuilder.html -> module specifier for the standalone page.
IMPORTS = {
    "`${CDN}/+esm`": "three",
    "`${CDN}/examples/jsm/controls/OrbitControls.js/+esm`": "three/addons/controls/OrbitControls.js",
    "`${CDN}/examples/jsm/exporters/GLTFExporter.js/+esm`": "three/addons/exporters/GLTFExporter.js",
    "`${CDN}/examples/jsm/exporters/STLExporter.js/+esm`": "three/addons/exporters/STLExporter.js",
    "`${CDN}/examples/jsm/environments/RoomEnvironment.js/+esm`": "three/addons/environments/RoomEnvironment.js",
}

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "coachbuilder.html").read_text(encoding="utf-8")
if f'const V = "{THREE_VERSION}";' not in src:
    raise SystemExit(f"coachbuilder.html does not use three.js {THREE_VERSION}; update THREE_VERSION and the hashes")
for old, spec in IMPORTS.items():
    if src.count(old) != 1:
        raise SystemExit(f"expected exactly one {old} in coachbuilder.html, found {src.count(old)}")
    src = src.replace(old, json.dumps(spec))

importmap = json.dumps(
    {
        "imports": {spec: f"{BASE}/{path}" for spec, (path, _) in FILES.items()},
        "integrity": {f"{BASE}/{path}": digest for path, digest in FILES.values()},
    },
    separators=(",", ":"),
)


def script_hash(body: str) -> str:
    return "'sha256-" + base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode() + "'"


inline = [importmap] + re.findall(r"<script[^>]*>(.*?)</script>", src, flags=re.S)
csp = "; ".join([
    "default-src 'none'",
    "script-src https://cdn.jsdelivr.net " + " ".join(script_hash(body) for body in inline),
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src https://fonts.gstatic.com",
    "img-src 'self' data: blob:",
    "connect-src 'self' data: blob:",
    "base-uri 'none'",
    "form-action 'none'",
    "object-src 'none'",
])

head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta http-equiv="Content-Security-Policy" content="{csp}">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><link rel="icon" href="data:,">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
        f'<script type="importmap">{importmap}</script></head><body>')
(root / "index.html").write_text(head + "\n" + src + "\n</body></html>\n", encoding="utf-8")
print("wrote index.html")
