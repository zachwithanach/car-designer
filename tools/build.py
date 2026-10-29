"""Wrap the artifact source (coachbuilder.html, no document skeleton) into a standalone index.html for GitHub Pages / local use."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "coachbuilder.html").read_text(encoding="utf-8")
head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><link rel="icon" href="data:,">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')
(root / "index.html").write_text(head + "\n" + src + "\n</body></html>\n", encoding="utf-8")
print("wrote index.html")
