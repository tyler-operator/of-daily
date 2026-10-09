"""Technical line illustrations for the OF daily deck. Original vector, no stock."""
import cairosvg

INK = "#0F2920"
MUTED = "#7A8C83"
MINT = "#52F5A0"
STEEL = "#C9D3CE"
BG = "none"

FONT = "Inter, Helvetica, Arial, sans-serif"


def wrap(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{body}</svg>')


def render(svg, path, scale=3):
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path, scale=scale,
                     background_color="#FAFAFA")


def label(x, y, t, size=12, anchor="start", color=MUTED, weight="400"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{t}</text>')


def leader(x1, y1, x2, y2):
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{MUTED}" stroke-width="1" '
            f'stroke-dasharray="3 3" fill="none"/>')


# ---------------------------------------------------------------- press brake
def press_brake():
    """Side section through a CNC press brake. The classic diagram."""
    W, H = 720, 470
    s = []

    # --- C frame, drawn as a closed profile (side section)
    frame = ("M120 40 L470 40 L470 120 L250 120 L250 250 L470 250 L470 300 "
             "L470 400 L120 400 Z")
    s.append(f'<path d="{frame}" fill="{STEEL}" fill-opacity="0.4" stroke="{INK}" '
             f'stroke-width="2.6" stroke-linejoin="round"/>')

    # --- bed, the fixed lower beam
    s.append(f'<rect x="250" y="300" width="300" height="48" fill="{STEEL}" '
             f'fill-opacity="0.75" stroke="{INK}" stroke-width="2.4"/>')

    # --- ram, the moving part, in mint
    s.append(f'<rect x="300" y="120" width="190" height="54" rx="2" fill="{MINT}" '
             f'fill-opacity="0.9" stroke="{INK}" stroke-width="2.4"/>')
    # cylinder above it
    s.append(f'<rect x="368" y="76" width="54" height="46" fill="{STEEL}" fill-opacity="0.85" '
             f'stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<path d="M382 86 L382 112 M408 86 L408 112" stroke="{INK}" stroke-width="1.4"/>')

    # --- punch hanging off the ram
    s.append(f'<path d="M368 174 L422 174 L402 236 L395 250 L388 236 Z" fill="{INK}" '
             f'stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')

    # --- sheet
    s.append(f'<rect x="282" y="288" width="268" height="8" fill="{INK}" fill-opacity="0.8"/>')

    # --- V die seated in the bed
    s.append(f'<rect x="326" y="296" width="138" height="34" fill="{STEEL}" fill-opacity="0.85" '
             f'stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<path d="M370 330 L395 296 L420 330" fill="#FAFAFA" stroke="{INK}" '
             f'stroke-width="2.2" stroke-linejoin="round"/>')

    # --- backgauge finger behind the die
    s.append(f'<rect x="492" y="246" width="14" height="46" fill="{INK}" fill-opacity="0.8"/>')
    s.append(f'<rect x="492" y="236" width="74" height="12" fill="{INK}" fill-opacity="0.5"/>')
    s.append(f'<path d="M520 224 L566 224" stroke="{INK}" stroke-width="2" '
             f'marker-end="url(#ar)"/>')
    s.append(f'<path d="M520 224 L486 224" stroke="{INK}" stroke-width="2" '
             f'marker-start="url(#ar2)"/>')

    # --- stroke arrow
    s.append(f'<path d="M330 192 L330 262" stroke="{INK}" stroke-width="2.6" '
             f'marker-end="url(#ar)"/>')

    # --- labels, all outside the machine
    s.append(label(292, 104, "RAM", 13, "end", INK, "700"))
    s.append(leader(296, 100, 330, 128))
    s.append(label(444, 100, "Hydraulic cylinder", 11.5, "start"))
    s.append(leader(440, 96, 416, 92))

    s.append(label(300, 212, "10 mm/s", 11.5, "end", INK, "700"))
    s.append(label(300, 228, "through steel", 11, "end"))

    s.append(label(450, 190, "PUNCH", 12.5, "start", INK, "700"))
    s.append(leader(446, 186, 412, 198))

    s.append(label(592, 254, "Backgauge", 12, "start", INK, "700"))
    s.append(label(592, 270, "sets how deep", 11, "start"))
    s.append(label(592, 285, "the sheet goes in", 11, "start"))

    s.append(label(258, 292, "Sheet", 11.5, "end"))
    s.append(leader(262, 290, 286, 291))

    s.append(label(300, 376, "V DIE", 12.5, "end", INK, "700"))
    s.append(leader(304, 372, 334, 334))

    s.append(label(160, 432, "C-frame. The whole machine is one casting.", 11.5, "start"))
    s.append(label(160, 64, "Crown", 11.5, "start"))

    defs = (f'<defs>'
            f'<marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
            f'<path d="M0 0 L9 4.5 L0 9 z" fill="{INK}"/></marker>'
            f'<marker id="ar2" markerWidth="9" markerHeight="9" refX="2" refY="4.5" '
            f'orient="auto"><path d="M9 0 L0 4.5 L9 9 z" fill="{INK}"/></marker>'
            f'</defs>')
    return wrap(W, H, defs + "".join(s))


# ------------------------------------------------------------- three versions
def versions():
    """Three machine generations, to scale against each other."""
    W, H = 1400, 236
    s = []

    def housing(ox, w, h, top, mint_ram=False):
        out = []
        y0 = 170 - h
        out.append(f'<rect x="{ox}" y="{y0}" width="{w}" height="{h}" fill="{STEEL}" '
                   f'fill-opacity="0.45" stroke="{INK}" stroke-width="2"/>')
        out.append(f'<rect x="{ox}" y="{y0}" width="{w}" height="{top}" fill="{STEEL}" '
                   f'fill-opacity="0.7" stroke="{INK}" stroke-width="2"/>')
        rc = MINT if mint_ram else STEEL
        out.append(f'<rect x="{ox+10}" y="{y0+top+10}" width="{w-20}" height="{max(10, h*0.12)}" '
                   f'fill="{rc}" fill-opacity="0.85" stroke="{INK}" stroke-width="1.8"/>')
        out.append(f'<rect x="{ox}" y="158" width="{w}" height="12" fill="{STEEL}" '
                   f'fill-opacity="0.7" stroke="{INK}" stroke-width="2"/>')
        return "".join(out)

    # 1. manual box and pan brake, small
    s.append(housing(140, 150, 72, 13))
    s.append(f'<path d="M162 116 L162 94 L198 94" stroke="{INK}" stroke-width="2.4" fill="none"/>')
    s.append(label(215, 198, "Manual box and pan", 13.5, "middle", INK, "700"))
    s.append(label(215, 218, "Hand lever. 1882 to today, still in every sheet metal shop", 12, "middle"))

    # 2. hydraulic CNC, mid
    s.append(housing(560, 250, 130, 23, mint_ram=True))
    s.append(label(685, 198, "Hydraulic CNC", 13.5, "middle", INK, "700"))
    s.append(label(685, 218, "The workhorse. 1968 onward. 30 to 3,000 tons", 12, "middle"))

    # 3. servo electric, tall slim
    s.append(housing(1070, 190, 152, 21))
    for x in (1100, 1192):
        s.append(f'<circle cx="{x}" cy="{60}" r="11" fill="none" stroke="{INK}" stroke-width="2.2"/>')
        s.append(f'<path d="M{x} 49 L{x} 71 M{x-11} 60 L{x+11} 60" stroke="{INK}" stroke-width="1.6"/>')
    s.append(label(1166, 198, "Servo electric", 13.5, "middle", INK, "700"))
    s.append(label(1166, 218, "Belts and ballscrews, no oil. Usually under 300 tons", 12, "middle"))

    return wrap(W, H, "".join(s))


# ------------------------------------------------------------- bend sequence
def bend_sequence():
    """Four frames: approach, contact, bend, springback."""
    W, H = 880, 210
    s = []
    frames = [
        ("Approach", 0, 0),
        ("Contact", 1, 0),
        ("Bottom", 2, 0),
        ("Springback", 3, 0),
    ]
    for name, i, _ in frames:
        ox = 20 + i * 220
        cx = ox + 90
        # die
        s.append(f'<path d="M{ox+28} 140 L{cx-26} 140 L{cx} 112 L{cx+26} 140 L{ox+152} 140 '
                 f'L{ox+152} 160 L{ox+28} 160 Z" fill="{STEEL}" fill-opacity="0.85" '
                 f'stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')

        if i == 0:
            punch_y = 36
            s.append(f'<path d="M{ox+40} 140 L{ox+140} 140" stroke="{INK}" stroke-width="5" '
                     f'stroke-linecap="round"/>')
        elif i == 1:
            punch_y = 86
            s.append(f'<path d="M{ox+40} 140 L{ox+140} 140" stroke="{INK}" stroke-width="5" '
                     f'stroke-linecap="round"/>')
        elif i == 2:
            punch_y = 104
            s.append(f'<path d="M{ox+40} 118 L{cx} 134 L{ox+140} 118" stroke="{INK}" '
                     f'stroke-width="5" fill="none" stroke-linejoin="round" '
                     f'stroke-linecap="round"/>')
        else:
            punch_y = 46
            s.append(f'<path d="M{ox+42} 112 L{cx} 134 L{ox+138} 112" stroke="{INK}" '
                     f'stroke-width="5" fill="none" stroke-linejoin="round" '
                     f'stroke-linecap="round"/>')
            s.append(f'<path d="M{ox+40} 120 L{cx} 134 L{ox+140} 120" stroke="{MINT}" '
                     f'stroke-width="2.4" fill="none" stroke-dasharray="4 3" '
                     f'stroke-linejoin="round"/>')

        # punch wedge
        s.append(f'<path d="M{cx-34} {punch_y} L{cx+34} {punch_y} L{cx+7} {punch_y+58} '
                 f'L{cx} {punch_y+70} L{cx-7} {punch_y+58} Z" fill="{MINT}" fill-opacity="0.9" '
                 f'stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')

        s.append(label(cx, 190, name, 13, "middle", INK, "700"))
        if i < 3:
            s.append(f'<path d="M{ox+176} 100 L{ox+206} 100" stroke="{MUTED}" '
                     f'stroke-width="2" marker-end="url(#ar3)"/>')

    defs = (f'<defs><marker id="ar3" markerWidth="8" markerHeight="8" refX="6" refY="4" '
            f'orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{MUTED}"/></marker></defs>')
    return wrap(W, H, defs + "".join(s))


# ------------------------------------------------------------- depreciation
def depreciation():
    """Real asking prices against age, CAD. MachineTools.com listings, Oct 2026."""
    W, H = 560, 300
    pad_l, pad_b, pad_t, pad_r = 52, 46, 20, 16
    x0, y0 = pad_l, H - pad_b
    pw, ph = W - pad_l - pad_r, H - pad_b - pad_t
    maxp, maxa = 140000, 32

    def px(age):
        return x0 + (age / maxa) * pw

    def py(p):
        return y0 - (p / maxp) * ph

    s = []
    # grid
    for v in (0, 35000, 70000, 105000, 140000):
        y = py(v)
        s.append(f'<path d="M{x0} {y} L{x0+pw} {y}" stroke="{STEEL}" stroke-width="1"/>')
        s.append(label(x0 - 8, y + 4, f"${v//1000}k", 10.5, "end"))
    for a in (0, 10, 20, 30):
        s.append(label(px(a), y0 + 20, f"{a}", 10.5, "middle"))
    s.append(label(x0 + pw / 2, y0 + 38, "Age of machine, years", 11, "middle"))

    pts = [
        (0, 129921, "New 112t"),
        (22, 56272, "2004"),
        (28, 46300, "1998"),
        (30, 46300, "1996"),
    ]
    path = " ".join(("M" if i == 0 else "L") + f"{px(a):.1f} {py(p):.1f}"
                    for i, (a, p, _) in enumerate(pts))
    s.append(f'<path d="{path}" stroke="{INK}" stroke-width="2.6" fill="none" '
             f'stroke-linejoin="round"/>')
    # floor band
    s.append(f'<path d="M{px(20)} {py(47500)} L{px(32)} {py(47500)}" stroke="{MINT}" '
             f'stroke-width="3" stroke-dasharray="6 4"/>')
    s.append(label(px(32), py(47500) - 10, "the floor, about $46k", 10.5, "end", "#0A7A45", "700"))

    for a, p, t in pts:
        s.append(f'<circle cx="{px(a):.1f}" cy="{py(p):.1f}" r="5" fill="{MINT}" '
                 f'stroke="{INK}" stroke-width="2"/>')
    s.append(label(px(0) + 10, py(129921) - 8, "$129,900 new", 11, "start", INK, "700"))
    s.append(label(px(30) - 6, py(46300) + 34, "a 1996 machine still asks $46,300",
                   10.5, "end"))

    # axes
    s.append(f'<path d="M{x0} {pad_t} L{x0} {y0} L{x0+pw} {y0}" stroke="{INK}" '
             f'stroke-width="1.6" fill="none"/>')
    return wrap(W, H, "".join(s))


# ------------------------------------------------------------- tooling shapes
def tooling():
    """Three punch profiles."""
    W, H = 560, 170
    s = []
    shapes = [
        ("Standard 88 deg", "M{0} 24 L{1} 24 L{2} 92 L{3} 104 L{4} 92 Z"),
        ("Gooseneck", None),
        ("Acute 30 deg", "M{0} 24 L{1} 24 L{2} 96 L{3} 110 L{4} 96 Z"),
    ]
    for i, (name, _) in enumerate(shapes):
        cx = 100 + i * 180
        if i == 1:
            s.append(f'<path d="M{cx-34} 24 L{cx+34} 24 L{cx+34} 48 L{cx+6} 54 '
                     f'L{cx+22} 74 L{cx+6} 96 L{cx} 108 L{cx-6} 96 L{cx-20} 74 '
                     f'L{cx-6} 54 L{cx-34} 48 Z" fill="{MINT}" fill-opacity="0.9" '
                     f'stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
        else:
            spread = 10 if i == 0 else 5
            s.append(f'<path d="M{cx-34} 24 L{cx+34} 24 L{cx+spread} 92 L{cx} 106 '
                     f'L{cx-spread} 92 Z" fill="{MINT}" fill-opacity="0.9" '
                     f'stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')
        s.append(label(cx, 136, name, 12, "middle", INK, "700"))
    s.append(label(280, 158, "A starter tooling set runs $2,850. A full one is $21,400 and up.",
                   11, "middle"))
    return wrap(W, H, "".join(s))


if __name__ == "__main__":
    render(press_brake(), "img_brake.png")
    render(versions(), "img_versions.png")
    render(bend_sequence(), "img_bend.png")
    render(depreciation(), "img_depreciation.png")
    render(tooling(), "img_tooling.png")
    print("rendered 5")
