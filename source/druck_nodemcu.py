"""Servo-Kästchen für ein großes NodeMCU-Board (LoLin/"V3"-Typ, ESP-12E + CH340, ca. 58 x 31 mm).
Außenmaße der Frontplatte, Servo-Ausschnitt und Hülsen wie in druck.py, das Kästchen ist links um 9 mm länger.
Das Board hängt an seinen 4 Befestigungslöchern auf Pfosten: Modulseite zur Frontplatte, Pins nach hinten,
USB-Buchse links (Kabelschlitz in der linken Wand, Stecker kommt von hinten).
Aufruf: python3 druck_nodemcu.py <Zielordner>"""
import sys
import numpy as np
from druck import *   # Helfer und Servo-Konstanten

# --- Board (nachmessen!) ---
NM_L, NM_W = 58.0, 31.0        # Länge inkl. USB-Buchse, Breite ohne Pins
HOLE_DX, HOLE_DY = 53.4, 25.4  # Abstand der Befestigungslöcher (Mitte-Mitte)
NM_X1 = -7.2                   # Board-Kante zum Servo (1,2 mm Luft zum Servogehäuse)
NM_Z0 = 9.5                    # Unterkante Board über der Plattenaußenseite (Platz für Bauteile + USB-Stecker darunter)
POST_D, PIN_D, PIN_H = 4.4, 2.5, 2.2   # Pfosten, Zapfen für das Loch (Ø2,5 für ca. Ø3-Loch), Zapfenhöhe über dem Pfosten
USB_SLOT = 16.0                # Breite Kabelschlitz
BX0 = -69.0                    # linke Außenkante des Kästchens (in druck.py -60)

def post(x, y):
    p = cyl(x, y, POST_D / 2, PLATE - 0.01, NM_Z0)
    tip = Manifold.cylinder(PIN_H, PIN_D / 2, PIN_D / 2 - 0.35, 32).translate([x, y, NM_Z0 - 0.01])
    return p + tip

def posts_xy():
    xc = NM_X1 - NM_L / 2
    return [(xc + sx * HOLE_DX / 2, sy * HOLE_DY / 2) for sx in (1, -1) for sy in (1, -1)]

def box_part_nodemcu():
    outer = rbox(BX0, Y0, X1, Y1, 0, DEPTH, R)
    inner = rbox(BX0 + WALL, Y0 + WALL, X1 - WALL, Y1 - WALL, PLATE, DEPTH + 1, R - WALL * 0.5)
    m = outer - inner
    bx0 = -SHAFT_FROM_END - CLR
    m = m - rbox(bx0, -BODY_W / 2 - CLR, bx0 + BODY_L + 2 * CLR, BODY_W / 2 + CLR, -1, PLATE + 1)
    bc = -SHAFT_FROM_END + BODY_L / 2
    for sx in (bc - HOLE_SPACING / 2, bc + HOLE_SPACING / 2):
        m = m - cyl(sx, 0, 0.9, PLATE - 3.5, PLATE + 1)
    tri = CrossSection([[[-3, Y0 - 0.1], [3, Y0 - 0.1], [0, Y0 + 1.6]]])
    m = m - Manifold.extrude(tri, 6).translate([-30, 0, DEPTH - 6])
    for (x, y) in posts_xy():
        m = m + post(x, y)
    # Kabelschlitz für das USB-Kabel in der linken Wand, nach hinten offen
    m = m - rbox(BX0 - 1, -USB_SLOT / 2, BX0 + WALL + 1, USB_SLOT / 2, PLATE, DEPTH + 1, 0)
    return m

def passprobe():
    """Kleine Probeplatte: nur die 4 Pfosten, um das Board in 10 Minuten anzustecken."""
    xc = NM_X1 - NM_L / 2
    base = rbox(-NM_L / 2 - 3, -NM_W / 2 - 3, NM_L / 2 + 3, NM_W / 2 + 3, 0, 1.2, 3.0)
    base = base - rbox(-NM_L / 2 + 8, -NM_W / 2 + 7, NM_L / 2 - 8, NM_W / 2 - 7, -1, 2, 2.0)   # Fenster, spart Material
    for (x, y) in posts_xy():
        base = base + cyl(x - xc, y, POST_D / 2, 1.19, 4.0) + Manifold.cylinder(PIN_H, PIN_D / 2, PIN_D / 2 - 0.35, 32).translate([x - xc, y, 3.99])
    return base

# --- Deckel: schließt das Kästchen hinten und umfasst es außen; wird durch die Haken-Hülsen zwischen Kästchen und Wand geklemmt ---
LID_FLOOR = 3.0       # Boden des Deckels (liegt an der Wand)
LID_RIM = 10.0        # Höhe des umfassenden Rands (deckt die hinteren 10 mm des Kästchens ab)
LID_GAP = 0.3         # Luft um das Kästchen
LID_WALL = 2.0        # Wandstärke des Rands
TOTAL_DEPTH = DEPTH + LID_FLOOR         # Abstand Grundplatte -> Wand (Hülsenlänge)

def lid_part():
    """Druckrichtung: Boden auf dem Bett (z = 0 ist die Wandseite), Rand zeigt nach oben."""
    g, w = LID_GAP, LID_WALL
    outer = rbox(BX0 - g - w, Y0 - g - w, X1 + g + w, Y1 + g + w, 0, LID_FLOOR + LID_RIM, R + g + w)
    inner = rbox(BX0 - g, Y0 - g, X1 + g, Y1 + g, LID_FLOOR, LID_FLOOR + LID_RIM + 1, R + g)
    m = outer - inner
    # vier kleine Klemmrippen innen an den langen Seiten: Deckel sitzt mit leichtem Druck auf dem Kästchen
    for sy in (-1, 1):
        yw = sy * (Y1 + g)                       # Innenfläche des Rands
        for px in (-45.0, 15.0):
            m = m + rbox(px, min(yw - sy * 0.4, yw + sy * 0.5), px + 2.0, max(yw - sy * 0.4, yw + sy * 0.5), LID_FLOOR - 0.5, LID_FLOOR + LID_RIM - 1.0)
    # Marke OBEN: kleine Kerbe im freien Rand über der oberen Wand
    tri = CrossSection([[[-3, Y0 - g - w - 0.1], [3, Y0 - g - w - 0.1], [0, Y0 - g - w + 1.5]]])
    m = m - Manifold.extrude(tri, 4).translate([-30, 0, LID_FLOOR + LID_RIM - 4])
    return m

# --- Haken-Hülsen (Schlüsselloch): Platte wird auf 4 Wandschrauben gehängt, keine Schrauben von vorn ---
H_D = 20.0          # Außendurchmesser (Schlüsselloch braucht Platz)
HEAD_D = 7.2        # Schraubenkopf, z. B. Linsen-/Halbrundkopf 3,5 x 30
HEAD_H = 2.6        # Kopfhöhe
H_SL = 7.0          # Schiebeweg (Platte wird nach dem Aufstecken 7 mm nach unten geschoben)
H_LIP = 2.4         # Lippe, die hinter dem Kopf greift (Wandseite)
H_CH = 3.4          # Kammer für den Kopf hinter der Lippe
H_ENTRY_D = HEAD_D + 1.2    # Einführloch
H_SLOT_W = 4.6      # Schlitz für den Schraubenschaft (Schaft 3,5 mm)
PIN_D2, PIN_L = 4.2, 7.6    # Zapfen für das Befestigungsloch Ø4,5 (Grundplatte 4 + Blende 4 mm, 0,4 mm zurückgesetzt)

def stadium(w, y0, y1, z0, z1):
    """Langloch mit Breite w zwischen den Mittelpunkten y0 und y1."""
    return cyl(0, y0, w / 2, z0, z1) + cyl(0, y1, w / 2, z0, z1) + rbox(-w / 2, min(y0, y1), w / 2, max(y0, y1), z0, z1)

def huelse_haken():
    """Druckrichtung: Wandseite (Schlüsselloch) auf dem Bett, Zapfen oben. Gesamtlänge 27 mm + Zapfen.
    Schlüsselloch: Einführloch unten (+y), Schlitz nach oben (-y). Kerbe am Rand = OBEN."""
    L = TOTAL_DEPTH
    m = cyl(0, 0, H_D / 2, 0, L)
    y_low, y_up = H_SL / 2, -H_SL / 2
    m = m - stadium(H_SLOT_W, y_low, y_up, -1, H_LIP + 0.01)                       # Lippe: nur Schlitz
    m = m - cyl(0, y_low, H_ENTRY_D / 2, -1, H_LIP + 0.01)                          # Einführloch durch die Lippe
    m = m - stadium(H_ENTRY_D, y_low, y_up, H_LIP, H_LIP + H_CH)                    # Kammer für den Kopf
    m = m + Manifold.cylinder(PIN_L, PIN_D2 / 2, PIN_D2 / 2 - 0.2, 32).translate([0, 0, L - 0.01])
    tri = CrossSection([[[-1.6, -H_D / 2 - 0.1], [1.6, -H_D / 2 - 0.1], [0, -H_D / 2 + 1.8]]])
    m = m - Manifold.extrude(tri, L - H_LIP - H_CH).translate([0, 0, H_LIP + H_CH])   # Kerbe OBEN
    return m

def spacer_long():
    return cyl(0, 0, 8.0, 0, TOTAL_DEPTH) - cyl(0, 0, 2.35, -1, TOTAL_DEPTH + 1)

def check_fit():
    """Prüft im zusammengebauten Zustand, dass Deckel und Kästchen sich nicht überschneiden."""
    box = box_part_nodemcu()
    lid = lid_part().mirror([0, 0, 1]).translate([0, 0, TOTAL_DEPTH])   # an die Wand klappen: z_lid = TOTAL_DEPTH - z_druck
    inter = (box ^ lid).volume()
    print('Überschneidung Kästchen/Deckel (mm³, soll ~0):', round(inter, 3))

if __name__ == '__main__':
    out = sys.argv[1]
    b = to_stl(box_part_nodemcu(), f'{out}/Servo_Kaestchen_NodeMCU_gross.stl')
    to_stl(passprobe(), f'{out}/Passprobe_NodeMCU_Bohrungen.stl')
    plate = box_part_nodemcu().translate([69, 26, 0])          # Kästchen: x 0..103, y 0..52
    for i in range(4):
        plate = plate + spacer().translate([8 + i * 22, 52 + 12 + 8, 0])
    p = to_stl(plate, f'{out}/Druckplatte_NodeMCU_gross_Kaestchen_und_4_Huelsen.stl')   # alte Version mit 24-mm-Hülsen
    check_fit()
    l = to_stl(lid_part(), f'{out}/Deckel_NodeMCU_Kaestchen.stl')
    hk = huelse_haken()
    to_stl(hk + hk.translate([24, 0, 0]) + hk.translate([0, 24, 0]) + hk.translate([24, 24, 0]), f'{out}/Haken_Huelsen_4x.stl')
    full = box_part_nodemcu().translate([69, 26, 0]) + lid_part().translate([71.3, 52 + 8 + 28.3, 0])
    for i in range(4):
        full = full + huelse_haken().translate([10 + i * 24, 52 + 8 + 56.6 + 12 + 10, 0])
    f = to_stl(full, f'{out}/Druckplatte_KOMPLETT_Kaestchen_Deckel_4_Huelsen27.stl')
    print('Deckel', np.round(l.extents, 1), '| Komplettplatte', np.round(f.extents, 1), '| Hülsenlänge', TOTAL_DEPTH)
    print('Kästchen', np.round(b.extents, 1), 'Volumen cm³', round(b.volume / 1000, 1), '| Platte', np.round(p.extents, 1))
