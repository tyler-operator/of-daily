"""Illustrations for OF Daily Deck 002, the ice resurfacer. Original vector."""
from art import wrap, render, label, leader, INK, MUTED, MINT, STEEL, FONT

ICE = "#DCE9EC"
WATER = "#A8D8E0"


def arrow_defs():
    return (f'<defs>'
            f'<marker id="za" markerWidth="9" markerHeight="9" refX="7" refY="4.5" '
            f'orient="auto"><path d="M0 0 L9 4.5 L0 9 z" fill="{INK}"/></marker>'
            f'<marker id="zm" markerWidth="8" markerHeight="8" refX="6" refY="4" '
            f'orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{MUTED}"/></marker>'
            f'</defs>')


# --------------------------------------------------------------- the machine
def resurfacer():
    """Side section of an ice resurfacer, labelled. Driving left to right."""
    W, H = 760, 450
    s = []

    # ice sheet
    s.append(f'<rect x="20" y="352" width="720" height="26" fill="{ICE}" '
             f'stroke="{INK}" stroke-width="1.6"/>')
    s.append(label(34, 370, "ICE", 10.5, "start", "#6E8C93", "700"))

    # fresh water film laid behind (left of travel direction = trailing)
    s.append(f'<path d="M60 352 L300 352" stroke="{WATER}" stroke-width="7" '
             f'stroke-linecap="round"/>')

    # ---- chassis
    s.append(f'<path d="M150 318 L150 206 L300 206 L316 150 L470 150 L470 206 '
             f'L640 206 L640 318 Z" fill="{STEEL}" fill-opacity="0.45" '
             f'stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>')

    # snow tank, the big box up front (right)
    s.append(f'<path d="M470 206 L470 150 L316 150 L300 206 Z" fill="{STEEL}" '
             f'fill-opacity="0.2" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<rect x="322" y="216" width="292" height="88" fill="{MINT}" '
             f'fill-opacity="0.22" stroke="{INK}" stroke-width="2" '
             f'stroke-dasharray="5 3"/>')
    s.append(label(468, 262, "SNOW TANK", 12, "middle", INK, "700"))
    s.append(label(468, 280, "2.8 m3. Dumped on the ramp", 10.5, "middle"))

    # water tank
    s.append(f'<rect x="172" y="226" width="130" height="78" fill="{WATER}" '
             f'fill-opacity="0.5" stroke="{INK}" stroke-width="2"/>')
    s.append(label(237, 258, "WATER", 11.5, "middle", INK, "700"))
    s.append(label(237, 275, "1,000 L", 11.5, "middle", INK, "700"))
    s.append(label(237, 291, "at 62 C", 10.5, "middle"))

    # driver seat and wheel
    s.append(f'<path d="M352 150 L352 112 L392 112 L392 150" fill="none" '
             f'stroke="{INK}" stroke-width="2.4"/>')
    s.append(f'<path d="M396 128 L432 112" stroke="{INK}" stroke-width="2.6"/>')
    s.append(f'<circle cx="436" cy="110" r="9" fill="none" stroke="{INK}" stroke-width="2.4"/>')

    # wheels
    for cx in (216, 576):
        s.append(f'<circle cx="{cx}" cy="330" r="30" fill="{STEEL}" fill-opacity="0.8" '
                 f'stroke="{INK}" stroke-width="2.6"/>')
        s.append(f'<circle cx="{cx}" cy="330" r="10" fill="none" stroke="{INK}" stroke-width="2"/>')

    # ---- the conditioner, trailing at the back left
    s.append(f'<path d="M86 300 L150 300 L150 348 L86 348 Z" fill="{MINT}" '
             f'fill-opacity="0.9" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>')
    # blade
    s.append(f'<path d="M92 344 L144 344 L144 352 L92 352 Z" fill="{INK}"/>')
    # auger spiral hint
    s.append(f'<path d="M96 320 Q108 310 120 320 Q132 330 142 320" fill="none" '
             f'stroke="{INK}" stroke-width="2"/>')

    # travel direction
    s.append(f'<path d="M560 92 L660 92" stroke="{INK}" stroke-width="2.6" '
             f'marker-end="url(#za)"/>')
    s.append(label(610, 80, "travel", 11.5, "middle", INK, "700"))

    # ---- labels
    s.append(label(42, 276, "CONDITIONER", 12, "start", INK, "700"))
    s.append(label(42, 292, "blade + auger", 10.5, "start"))
    s.append(leader(96, 296, 112, 300))
    s.append(label(86, 404, "The blade shaves. The auger lifts the snow up and forward into the tank.",
                   11, "start"))


    s.append(label(656, 330, "2,500 lb of snow", 10.5, "start"))
    s.append(label(656, 345, "off every pass", 10.5, "start"))
    s.append(f'<path d="M158 294 Q246 182 338 214" fill="none" stroke="{MUTED}" '
             f'stroke-width="2" stroke-dasharray="4 3" marker-end="url(#zm)"/>')

    s.append(label(400, 424, "4,423 kg empty. 5,148 kg full. It gets heavier as it works.",
                   11.5, "middle"))

    return wrap(W, H, arrow_defs() + "".join(s))


# ------------------------------------------------------------ four steps
def resurface_steps():
    """Shave, collect, wash, lay. Four cross-sections through the ice."""
    W, H = 1180, 240
    s = []
    steps = [
        ("Shave", "A 77 inch blade takes off the chewed-up top layer"),
        ("Collect", "An auger lifts the snow forward into the tank"),
        ("Wash", "Water floods the grooves and gets vacuumed back"),
        ("Lay", "Hot water spreads behind a towel and freezes clear"),
    ]
    for i, (name, blurb) in enumerate(steps):
        ox = 24 + i * 290
        cx = ox + 112

        # ice block
        s.append(f'<rect x="{ox}" y="96" width="224" height="46" fill="{ICE}" '
                 f'stroke="{INK}" stroke-width="1.8"/>')

        if i == 0:
            # rough surface being cut
            s.append(f'<path d="M{ox} 96 L{ox+30} 90 L{ox+58} 97 L{ox+86} 89 '
                     f'L{ox+112} 96" fill="none" stroke="{INK}" stroke-width="2"/>')
            s.append(f'<path d="M{ox+112} 96 L{ox+224} 96" stroke="{MINT}" stroke-width="3.5"/>')
            s.append(f'<path d="M{cx} 60 L{cx} 90" stroke="{INK}" stroke-width="2.6" '
                     f'marker-end="url(#za)"/>')
            s.append(f'<rect x="{cx-6}" y="46" width="60" height="16" fill="{INK}"/>')
        elif i == 1:
            s.append(f'<path d="M{ox} 96 L{ox+224} 96" stroke="{INK}" stroke-width="2"/>')
            for k in range(4):
                xx = ox + 28 + k * 34
                s.append(f'<circle cx="{xx}" cy="{84 - k*9}" r="7" fill="{STEEL}" '
                         f'stroke="{INK}" stroke-width="1.6"/>')
            s.append(f'<path d="M{ox+24} 88 Q{ox+110} 34 {ox+192} 52" fill="none" '
                     f'stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 3" '
                     f'marker-end="url(#zm)"/>')
        elif i == 2:
            s.append(f'<path d="M{ox} 96 L{ox+224} 96" stroke="{INK}" stroke-width="2"/>')
            s.append(f'<path d="M{ox+16} 96 L{ox+208} 96" stroke="{WATER}" stroke-width="8" '
                     f'stroke-linecap="round"/>')
            for k in range(5):
                xx = ox + 30 + k * 40
                s.append(f'<path d="M{xx} 70 L{xx} 88" stroke="{WATER}" stroke-width="3" '
                         f'stroke-linecap="round"/>')
            s.append(f'<path d="M{ox+186} 88 L{ox+186} 62" stroke="{INK}" stroke-width="2.2" '
                     f'marker-end="url(#za)"/>')
        else:
            s.append(f'<path d="M{ox} 96 L{ox+224} 96" stroke="{INK}" stroke-width="2"/>')
            s.append(f'<path d="M{ox+10} 93 L{ox+214} 93" stroke="{MINT}" stroke-width="6" '
                     f'stroke-linecap="round"/>')
            s.append(f'<rect x="{cx-40}" y="68" width="80" height="12" fill="{INK}" '
                     f'fill-opacity="0.7"/>')
            s.append(label(cx, 60, "towel", 10, "middle"))

        s.append(label(cx, 174, f"{i+1}. {name}", 14, "middle", INK, "700"))
        s.append(label(cx, 198, blurb, 11, "middle"))
        if i < 3:
            s.append(f'<path d="M{ox+242} 116 L{ox+272} 116" stroke="{MUTED}" '
                     f'stroke-width="2" marker-end="url(#zm)"/>')

    return wrap(W, H, arrow_defs() + "".join(s))


# ------------------------------------------------------------ three eras
def eras():
    """Model A, propane, electric. The machine's three lives."""
    W, H = 1400, 212
    s = []

    def body(ox, w, h, cab_h, fill, dashed=False):
        out = []
        y0 = 150 - h
        da = ' stroke-dasharray="5 3"' if dashed else ''
        out.append(f'<path d="M{ox} 150 L{ox} {y0} L{ox+w*0.56} {y0} '
                   f'L{ox+w*0.56} {y0-cab_h} L{ox+w*0.86} {y0-cab_h} '
                   f'L{ox+w} {y0} L{ox+w} 150 Z" fill="{fill}" fill-opacity="0.55" '
                   f'stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"{da}/>')
        for cx in (ox + w * 0.22, ox + w * 0.8):
            out.append(f'<circle cx="{cx:.0f}" cy="158" r="15" fill="{STEEL}" '
                       f'stroke="{INK}" stroke-width="2"/>')
        return "".join(out)

    s.append(body(120, 190, 54, 34, STEEL))
    s.append(label(215, 190, "1949, Model A", 13.5, "middle", INK, "700"))
    s.append(label(215, 204, "A war surplus chassis in a California rink", 12, "middle"))

    s.append(body(560, 250, 80, 42, STEEL))
    s.append(f'<rect x="700" y="52" width="40" height="18" rx="9" fill="{STEEL}" '
             f'stroke="{INK}" stroke-width="2"/>')
    s.append(label(685, 190, "Propane", 13.5, "middle", INK, "700"))
    s.append(label(685, 204, "The arena standard. A tank on the back", 12, "middle"))

    s.append(body(1040, 250, 80, 42, MINT))
    s.append(f'<rect x="1176" y="48" width="34" height="22" fill="{MINT}" '
             f'fill-opacity="0.9" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<path d="M1188 52 L1182 62 L1194 62 L1188 70" fill="none" '
             f'stroke="{INK}" stroke-width="2"/>')
    s.append(label(1165, 190, "Electric", 13.5, "middle", INK, "700"))
    s.append(label(1165, 204, "18% of Ontario operators. 45% switching in five years", 12, "middle"))

    return wrap(W, H, "".join(s))


# ------------------------------------------------------------ cost bar
def cost_compare():
    """What a resurface costs against what the ice sells for."""
    W, H = 660, 290
    s = []
    x0, y0 = 150, 230
    bar_h = 54
    maxv = 400.0
    plot_w = 340

    rows = [
        ("One resurface", 14, MINT, "modeled"),
        ("One hour of ice", 385.95, INK, "Oakville 2026, adult prime"),
    ]
    yy = 64
    for name, v, col, note in rows:
        w = max(6, (v / maxv) * plot_w)
        s.append(f'<rect x="{x0}" y="{yy}" width="{w:.0f}" height="{bar_h}" fill="{col}" '
                 f'fill-opacity="0.9" stroke="{INK}" stroke-width="2"/>')
        s.append(label(x0 - 12, yy + 26, name, 12.5, "end", INK, "700"))
        s.append(label(x0 - 12, yy + 43, note, 10, "end"))
        tx = x0 + w + 12
        s.append(label(tx, yy + 34, f"${v:,.0f}" if v >= 100 else f"${v:.0f}",
                       19, "start", INK, "700"))
        yy += 96

    s.append(f'<path d="M{x0} 48 L{x0} 248" stroke="{INK}" stroke-width="1.8"/>')
    s.append(label(x0, 272, "The resurface is about 4% of what the hour sells for.",
                   11.5, "start", MUTED))
    return wrap(W, H, "".join(s))


if __name__ == "__main__":
    render(resurfacer(), "z_machine.png")
    render(resurface_steps(), "z_steps.png")
    render(eras(), "z_eras.png")
    render(cost_compare(), "z_cost.png")
    print("rendered 4")
