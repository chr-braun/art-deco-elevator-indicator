"""3D-Druckteile für die Servo-Nachrüstung der Elevator Indicator.
Koordinaten mm, Ursprung = Servowelle (Drehpunkt). x nach rechts, y nach UNTEN (wie Blatt),
z = 0 ist die Vorderseite, die auf die Grundplatte geklebt wird (liegt beim Druck auf dem Bett)."""
import sys
import numpy as np
from manifold3d import Manifold, CrossSection, JoinType
import trimesh

# --- MG90S (an deinem Servo nachmessen!) ---
BODY_L, BODY_W = 22.8, 12.2
SHAFT_FROM_END = 6.0
HOLE_SPACING = 27.8
CLR = 0.35
# --- Kästchen ---
X0, X1, Y0, Y1 = -60.0, 34.0, -26.0, 26.0
DEPTH = 24.0          # Abstand Grundplatte -> Wand
PLATE = 4.0           # Frontplatte (Servo-Oberteil steckt darin)
WALL = 2.4
R = 3.0
# --- D1 mini (hochkant, USB nach unten) ---
D1_W, D1_L = 25.6, 34.2
D1_X0, D1_Y1 = -50.0, 16.2     # linke Kante, USB-Kante (unten)

def rbox(x0, y0, x1, y1, z0, z1, r=0.0):
    sq = CrossSection.square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]).translate([x0 + r, y0 + r])
    if r > 0: sq = sq.offset(r, JoinType.Round, circular_segments=32)
    return Manifold.extrude(sq, z1 - z0).translate([0, 0, z0])

def cyl(x, y, r, z0, z1):
    return Manifold.cylinder(z1 - z0, r, r, 48).translate([x, y, z0])

def box_part():
    outer = rbox(X0, Y0, X1, Y1, 0, DEPTH, R)
    inner = rbox(X0 + WALL, Y0 + WALL, X1 - WALL, Y1 - WALL, PLATE, DEPTH + 1, R - WALL * 0.5)
    m = outer - inner
    # Servo-Ausschnitt durch die Frontplatte
    bx0 = -SHAFT_FROM_END - CLR
    m = m - rbox(bx0, -BODY_W / 2 - CLR, bx0 + BODY_L + 2 * CLR, BODY_W / 2 + CLR, -1, PLATE + 1)
    # Sacklöcher für die Servo-Schrauben (von innen, 3,5 mm tief, Ø1,8)
    bc = -SHAFT_FROM_END + BODY_L / 2
    for sx in (bc - HOLE_SPACING / 2, bc + HOLE_SPACING / 2):
        m = m - cyl(sx, 0, 0.9, PLATE - 3.5, PLATE + 1)
    # Kabelaustritt unten (offen zur Wand): USB-Stecker passt durch
    ux = D1_X0 + D1_W / 2
    m = m - rbox(ux - 7.5, Y1 - WALL - 1, ux + 7.5, Y1 + 1, PLATE, DEPTH + 1, 0)
    # Anschläge für den D1 mini (L-Ecken, 3 mm hoch)
    stops = []
    for (cx, cy, sxn, syn) in [(D1_X0, D1_Y1 - D1_L, 1, 1), (D1_X0 + D1_W, D1_Y1 - D1_L, -1, 1)]:
        g = 0.4
        x = cx - sxn * g; y = cy - syn * g
        stops.append(rbox(min(x, x - sxn * 1.6), min(y, y + syn * 6), max(x, x - sxn * 1.6), max(y, y + syn * 6), PLATE, PLATE + 3))
        stops.append(rbox(min(x, x + sxn * 6), min(y, y - syn * 1.6), max(x, x + sxn * 6), max(y, y - syn * 1.6), PLATE, PLATE + 3))
    for (cx, sxn) in [(D1_X0, 1), (D1_X0 + D1_W, -1)]:   # seitliche Führungen unten (USB-Ende bleibt frei)
        x = cx - sxn * 0.4
        stops.append(rbox(min(x, x - sxn * 1.6), D1_Y1 - 8, max(x, x - sxn * 1.6), D1_Y1 - 2, PLATE, PLATE + 3))
    for s in stops: m = m + s
    # Markierung OBEN: Kerbe in der oberen Wand-Kante + Pfeil-Rippe innen
    tri = CrossSection([[[ -3, Y0 - 0.1], [3, Y0 - 0.1], [0, Y0 + 1.6]]])
    m = m - Manifold.extrude(tri, 6).translate([-30, 0, DEPTH - 6])
    # Klebefläche vergrößern: kleiner Kragen nicht nötig – Frontplatte ist vollflächig
    return m

def spacer():
    return cyl(0, 0, 8.0, 0, DEPTH) - cyl(0, 0, 2.35, -1, DEPTH + 1)

def to_stl(m, path):
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts), process=False)
    # y-Achse zurückdrehen (Blatt-y nach unten -> rechtshändig spiegeln würde Volumen umdrehen), daher Spiegelung + Normalen fixen
    pass  # Koordinatensystem ist bereits rechtshaendig (x rechts, y unten, z zur Wand)
    print(path.split('/')[-1], 'Status manifold:', m.status(), 'Körper:', len(tm.split(only_watertight=False)), 'wasserdicht:', tm.is_watertight, 'Normalen ok:', tm.is_winding_consistent and tm.volume > 0)
    assert tm.is_watertight, path
    tm.export(path)
    return tm

if __name__ == '__main__':
    out = sys.argv[1]
    b = to_stl(box_part(), f'{out}/Servo_Kaestchen.stl')
    s4 = spacer()
    s4 = s4 + spacer().translate([20, 0, 0]) + spacer().translate([0, 20, 0]) + spacer().translate([20, 20, 0])
    s = to_stl(s4, f'{out}/Abstandshuelsen_4x.stl')
    print('Kästchen', np.round(b.extents, 1), 'Volumen cm³', round(b.volume / 1000, 1))
    print('Hülsen', np.round(s.extents, 1), 'Volumen cm³', round(s.volume / 1000, 1))
