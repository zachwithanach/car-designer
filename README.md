# Coachbuilder

Design your own car in the browser. Rough out the proportions with sliders, then shape it by hand: drag handles, sculpt the body like clay, paint on windows and lights, and drag parts onto it. Test-drive it on a track, then export it for 3D printing or game engines.

## Run it

- **GitHub Pages / local:** open `index.html` (or serve the folder with `python3 -m http.server`). Everything runs in the browser. There is no backend.
- **Claude artifact:** publish `coachbuilder.html` as an artifact. The artifact version adds two features:
  - **Describe a car:** Claude sets the sliders and paint from a sentence.
  - **Shared gallery:** publish, browse, like and load other people's designs.

## Files

| File | Purpose |
|---|---|
| `coachbuilder.html` | The app source. It has no `<html>`/`<head>` wrapper because the artifact host adds one. |
| `index.html` | Generated standalone page for GitHub Pages. Do not edit it by hand. |
| `tools/build.py` | Wraps `coachbuilder.html` into `index.html`. Run it after every change. |

## Build tools

| Tool | What it does |
|---|---|
| Handles | Drag dots on the roofline, width and underside. Click a line to add a dot. Delete removes the selected dot. |
| Sculpt | Pull, push, smooth or erase the surface. Mirrors left and right by default. |
| Paint on | Paint glass, body color, stripe color, black trim, chrome, headlight, taillight or amber onto the body. |
| Parts | 20 parts, including wings, scoops, vents, fins, lamps, exhausts, mirrors, racks, bull bars, extra wheels and primitive shapes. Each part can be moved, sized, stretched, rotated, paired and recolored. |

Hand edits are stored in body-relative coordinates, so they stay in place when you move a slider. Undo and redo cover every change (Ctrl+Z, Ctrl+Shift+Z).

## Exports

- PNG screenshot
- GLB (game-ready, with materials)
- STL at 1:43, 1:24 or 1:18, Z-up, in millimetres

In the Claude viewer, STL and GLB files arrive inside a `.zip`, because the artifact sandbox only allows certain file types.

## Share codes

`CB2:` codes carry the whole design, including every hand edit. `CB1:` codes from version 1 still load.
