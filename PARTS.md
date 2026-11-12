# Parts and tools

No prices or shops on purpose: buy where you like. Quantities are for one indicator.

## Material

| Qty | Part | Used for |
|---|---|---|
| 2 | Plywood 4 mm, about 380 × 290 mm | Base plate, bezel, pointer, rosette |
| – | Wood glue (D3), 2-component epoxy or mounting adhesive | Wood on wood / printed parts on wood |
| – | Wood stain (walnut), gold wax, hard-wax oil or matt varnish | Surface (optional) |
| 1 | Chicago screw (binding post) Ø 5 mm, brass, 12–14 mm | Pointer pivot (original wood-only design; the servo version does not need it) |
| – | PETG or ASA filament, about 100 g | Servo box, lid, hook sleeves |
| 4 | Wall screws with matching wall plugs | Hanging (see `laser/wall-hook-drill-template.svg`) |

## Electronics

| Qty | Part | Notes |
|---|---|---|
| 1 | NodeMCU (ESP8266, ESP-12E, CH340), about 58 × 31 mm | Or a Wemos D1 mini (use the `legacy` box) |
| 1 | Servo MG90S | Check the real swing angle: the pointer needs about 115° |
| 1 | Electrolytic capacitor 470–1000 µF, ≥ 10 V | Prevents resets and jitter on weak supplies |
| 1 | USB power supply 5 V / 2 A and a USB cable | Cable length as needed, flat cable hides well |
| 3 | Dupont wires F2M (or solder directly) | Servo to board |
| 1 | Presence / occupancy sensor known to Home Assistant | e.g. a Zigbee mmWave sensor. Radar can see through thin doors: tune the range |
| 1 | Optional speaker known to Home Assistant | For the elevator "ding" |

## Tools

Laser cutter (tested: 10 W diode laser), 3D printer, soldering iron, heat-shrink tubing, drill with 3, 6 and about 8 mm bits, 12 mm Forstner bit, clamps, sandpaper (P240), spirit level, wire/pipe detector, hammer drill (for the wall).

## Files you need

| Part | File |
|---|---|
| Base plate, bezel + pointer | `laser/01_base-plate.svg`, `laser/02_bezel-pointer.svg` |
| Wall template | `laser/wall-hook-drill-template.svg` |
| Print: box, lid, sleeves | `3d-print/servo-box-nodemcu.stl`, `lid-nodemcu.stl`, `hook-sleeves-4x.stl` (or all on one plate) |
| Fit test | `3d-print/fit-test-nodemcu.stl` (print first and check the board holes) |
| Firmware | `home-assistant/elevator-indicator-nodemcu.yaml` + your `secrets.yaml` |
| Automation | `home-assistant/automation.yaml` |
