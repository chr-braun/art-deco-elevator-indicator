# Elevator Indicator

An art-deco floor indicator that shows **FREI** (free) or **BESETZT** (occupied) instead of floors. A servo swings the pointer, Home Assistant drives it from a presence sensor, and an optional elevator "ding" announces the change.

Animated project page: open [`index.html`](index.html) (or publish it with GitHub Pages).
Full build guide (German, with pictures): [`docs/anleitung.html`](docs/anleitung.html). Parts list: [`PARTS.md`](PARTS.md). Deutsche Version: [`README.de.md`](README.de.md).

![Assembled preview](docs/previews/assembled.png)

## At a glance

| | |
|---|---|
| Size | about 366 × 275 mm, 3 plywood layers (4 mm each) |
| Wood | 4 mm plywood, 2 laser sheets (378 × 288 mm each) |
| Print | servo box + lid + 4 hook sleeves, PETG/ASA |
| Electronics | ESP8266 (NodeMCU or D1 mini), servo MG90S, 5 V USB |
| Software | ESPHome + Home Assistant |
| License | CC BY-NC-SA 4.0 |

## Repository layout

| Folder | Content |
|---|---|
| `laser/` | SVG files for the laser (black = engrave fill, red = cut), wall drill template, optional laser-cut servo layers |
| `3d-print/` | STL files for the NodeMCU version, `legacy/` for the D1 mini + screw-mount version |
| `home-assistant/` | ESPHome configs, automation, `secrets.yaml.example` |
| `source/` | Python scripts that generate the 3D parts (dimensions are constants at the top) |
| `docs/` | Build guide and pictures |

## Quick build

1. Laser `laser/01_base-plate.svg` and `laser/02_bezel-pointer.svg` (4 mm plywood). Engrave first, then cut, do not move the board in between.
2. Drill the pivot hole of the base plate from the front to 12 mm. Glue the bezel on the base plate (the plate stands out 3 mm on every side).
3. Print `fit-test-nodemcu.stl` first and check your board, then print the box, lid and hook sleeves (or `plate-complete-...stl`).
4. Copy `home-assistant/secrets.yaml.example` to `secrets.yaml`, fill it in, flash `elevator-indicator-nodemcu.yaml` with ESPHome (first flash by USB **without** the servo).
5. Mount the servo, wire it: brown/GND to `G`, red to `VIN` (5 V), orange to `D5`, capacitor across 5 V and ground.
6. Glue the pointer on the servo horn and calibrate in Home Assistant with the two sliders "Zeiger FREI" and "Zeiger BESETZT".
7. Hang it on the wall using `laser/wall-hook-drill-template.svg`, add the automation (`home-assistant/automation.yaml`).

## Calibration

The sliders run from -100 to 100 (about -90° to +90°). The defaults in the YAML (-63 / +63) are a rough start. The original build ended up at **FREI = 100** and **BESETZT = -50**, but this depends on how the horn sits on the servo. If the pointer runs the wrong way, swap the signs.

## Behaviour (automation)

* Presence detected: pointer to BESETZT immediately.
* No presence for **5 seconds**: pointer back to FREI. New presence within those 5 s cancels the return.
* Optional ding 2 s after the switch (the servo takes 1.5 s). **Do not use `announce: true`** with `media_player.play_media`: a HomePod behind Music Assistant stayed silent with it.
* Put your own `elevator-ding.mp3` into Home Assistant under *Media → Local media*. No sound file is included in this repository.

## Notes and known limits

* Measure your servo before printing: the STLs assume shaft 6.0 mm from the housing end, tab hole distance 27.8 mm. Change the constants in `source/druck_nodemcu.py` and regenerate (`pip install numpy trimesh manifold3d`, then `python3 druck_nodemcu.py <outdir>`).
* The NodeMCU box was designed from estimated board dimensions: print the fit test first.
* Servo from the board's 5 V pin can brown out the ESP on weak supplies. Use a capacitor, a better supply or a separate 5 V supply for the servo with common ground.
* The build guide is German and describes the original D1 mini + screws-from-the-front variant in steps 6, 12 and 13; the repository files use the newer hook mounting and the NodeMCU.

## License and credits

CC BY-NC-SA 4.0, see [`LICENSE`](LICENSE). Fonts: Limelight and Cinzel Decorative, SIL OFL 1.1. Ornaments are constructed from scratch.
