"""Portrait 1080x1350 carousel slides for Instagram. SVG -> JPEG, no pptx."""
import cairosvg, io, os

HERE = os.path.dirname(os.path.abspath(__file__))


def img(path):
    import base64
    with open(os.path.join(HERE, path), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()
from PIL import Image

W, H = 1080, 1350
M = 76                      # side margin

INK = "#0F2920"
BODY = "#303D37"
MUTED = "#7A8C83"
GREY = "#8A9690"
MINT = "#52F5A0"
VIOLET = "#7366E0"
BG = "#FAFAFA"
PANEL = "#F0F3F1"
RULE = "#D9E1DC"
ICE = "#DCE9EC"
WATER = "#A8D8E0"
STEEL = "#C9D3CE"
WHITE = "#FFFFFF"

SANS = "Inter, Helvetica, Arial, sans-serif"
SERIF = "Lora, Georgia, serif"

HANDLE = "@operatorsfund"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=30, fill=BODY, anchor="start", weight="400", font=SANS, ls=None):
    extra = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}"{extra}>{esc(s)}</text>')


def wrap_lines(lines, x, y, size, lh, **kw):
    out = []
    for i, ln in enumerate(lines):
        out.append(T(x, y + i * lh, ln, size, **kw))
    return "".join(out)


def dash(x, y, label, w=56):
    return (f'<rect x="{x}" y="{y-11}" width="{w}" height="5" fill="{MINT}"/>'
            + T(x + w + 18, y, label.upper(), 21, GREY, weight="700", ls="1.4"))


def highlight(x, y, text, size, pad_w, h=None):
    """Mint marker behind a serif line."""
    hh = h or int(size * 1.05)
    return (f'<rect x="{x-8}" y="{y-size*0.80:.0f}" width="{pad_w}" height="{hh}" fill="{MINT}"/>'
            + T(x, y, text, size, INK, font=SERIF))


def chrome(idx, total=8, tag=None):
    """Header mark, slide counter, footer handle."""
    s = []
    s.append(f'<image x="{M}" y="54" width="286" height="17" preserveAspectRatio="xMinYMin meet" xlink:href="{img("logo_alt.png")}"/>')
    s.append(T(W - M, 86, f"{idx}/{total}", 22, GREY, "end", "700", SANS, "1.2"))
    s.append(f'<rect x="{M}" y="120" width="{W-2*M}" height="2" fill="{RULE}"/>')
    if tag:
        tw = 36 + 13 * len(tag)
        s.append(f'<rect x="{M}" y="144" width="{tw}" height="44" rx="22" fill="{INK}"/>')
        s.append(T(M + tw / 2, 173, tag, 19, WHITE, "middle", "700", SANS, "1.2"))
    s.append(f'<rect x="{M}" y="{H-104}" width="{W-2*M}" height="2" fill="{RULE}"/>')
    s.append(T(M, H - 62, HANDLE, 21, GREY, weight="700", ls="1.2"))
    s.append(T(W - M, H - 62, "ALL FIGURES CAD", 19, GREY, "end", "700", SANS, "1.2"))
    return "".join(s)


def page(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>{body}</svg>')


def save(svg, path):
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=W, output_height=H,
                           background_color=BG)
    im = Image.open(io.BytesIO(png)).convert("RGB")
    im.save(path, "JPEG", quality=92, optimize=True)


# ============================== PORTRAIT ART ==============================

def steps_grid():
    """Four bend/resurface steps as a 2x2 grid, portrait friendly."""
    GW, GH = 920, 620
    s = []
    steps = [("1. Shave", "A 77 inch blade takes the chewed-up top layer off"),
             ("2. Collect", "An auger lifts the snow forward into the tank"),
             ("3. Wash", "Water floods the grooves and is vacuumed straight back"),
             ("4. Lay", "Hot water spreads behind a towel and freezes clear")]
    for i, (name, blurb) in enumerate(steps):
        cx = 20 + (i % 2) * 470
        cy = 10 + (i // 2) * 316
        s.append(f'<rect x="{cx}" y="{cy}" width="430" height="292" fill="{PANEL}"/>')
        bx, by = cx + 48, cy + 196
        s.append(f'<rect x="{bx}" y="{by}" width="334" height="54" fill="{ICE}" '
                 f'stroke="{INK}" stroke-width="2.4"/>')
        mx = bx + 167
        if i == 0:
            s.append(f'<path d="M{bx} {by} L{bx+46} {by-10} L{bx+88} {by+2} '
                     f'L{bx+130} {by-11} L{mx} {by}" fill="none" stroke="{INK}" stroke-width="3"/>')
            s.append(f'<path d="M{mx} {by} L{bx+334} {by}" stroke="{MINT}" stroke-width="5"/>')
            s.append(f'<rect x="{mx-16}" y="{by-78}" width="92" height="22" fill="{INK}"/>')
            s.append(f'<path d="M{mx+30} {by-52} L{mx+30} {by-14}" stroke="{INK}" '
                     f'stroke-width="3.4" marker-end="url(#sa)"/>')
        elif i == 1:
            for k in range(4):
                s.append(f'<circle cx="{bx+42+k*52}" cy="{by-18-k*14}" r="11" fill="{STEEL}" '
                         f'stroke="{INK}" stroke-width="2.2"/>')
            s.append(f'<path d="M{bx+32} {by-14} Q{mx} {by-110} {bx+300} {by-70}" fill="none" '
                     f'stroke="{MUTED}" stroke-width="3" stroke-dasharray="6 5" '
                     f'marker-end="url(#sm)"/>')
        elif i == 2:
            s.append(f'<path d="M{bx+22} {by} L{bx+312} {by}" stroke="{WATER}" '
                     f'stroke-width="12" stroke-linecap="round"/>')
            for k in range(5):
                s.append(f'<path d="M{bx+50+k*58} {by-44} L{bx+50+k*58} {by-14}" '
                         f'stroke="{WATER}" stroke-width="4.5" stroke-linecap="round"/>')
            s.append(f'<path d="M{bx+278} {by-16} L{bx+278} {by-58}" stroke="{INK}" '
                     f'stroke-width="3.4" marker-end="url(#sa)"/>')
        else:
            s.append(f'<path d="M{bx+14} {by-4} L{bx+320} {by-4}" stroke="{MINT}" '
                     f'stroke-width="9" stroke-linecap="round"/>')
            s.append(f'<rect x="{mx-62}" y="{by-56}" width="124" height="18" fill="{INK}" '
                     f'fill-opacity="0.72"/>')
            s.append(T(mx, by - 68, "towel", 17, MUTED, "middle"))
        s.append(T(cx + 30, cy + 58, name, 28, INK, weight="700"))
        words, line, lines = blurb.split(), "", []
        for wd in words:
            if len(line + " " + wd) > 38:
                lines.append(line); line = wd
            else:
                line = (line + " " + wd).strip()
        lines.append(line)
        s.append(wrap_lines(lines, cx + 30, cy + 94, 20, 27, fill=MUTED))

    defs = (f'<defs><marker id="sa" markerWidth="9" markerHeight="9" refX="7" refY="4.5" '
            f'orient="auto"><path d="M0 0 L9 4.5 L0 9 z" fill="{INK}"/></marker>'
            f'<marker id="sm" markerWidth="8" markerHeight="8" refX="6" refY="4" '
            f'orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{MUTED}"/></marker></defs>')
    return GW, GH, defs + "".join(s)


def cost_bars(ox, oy, width=928):
    """Cost per resurface, stacked bars."""
    s = []
    rows = [("Operator, 10 min", 6.67, VIOLET), ("Machine capital", 2.27, INK),
            ("Heating the water", 2.26, INK), ("Water itself", 1.66, INK),
            ("Fuel or charge", 1.00, INK)]
    lblw, plot, maxv = 330, width - 330 - 150, 7.0
    for i, (name, v, col) in enumerate(rows):
        y = oy + i * 66
        if i % 2 == 0:
            s.append(f'<rect x="{ox}" y="{y-34}" width="{width}" height="60" fill="{PANEL}"/>')
        s.append(T(ox + lblw - 24, y + 4, name, 25, INK, "end", "600"))
        bw = (v / maxv) * plot
        s.append(f'<rect x="{ox+lblw}" y="{y-20}" width="{bw:.0f}" height="32" fill="{col}"/>')
        s.append(T(ox + lblw + bw + 20, y + 8, f"${v:.2f}", 30, INK, font=SERIF))
    y = oy + len(rows) * 66
    s.append(f'<path d="M{ox} {y-24} L{ox+width} {y-24}" stroke="{INK}" stroke-width="2.6"/>')
    s.append(T(ox + lblw - 24, y + 18, "Total", 26, INK, "end", "700"))
    s.append(T(ox + lblw + 8, y + 26, "$13.86", 50, INK, font=SERIF))
    s.append(T(ox + lblw + 200, y + 22, "per resurface", 22, GREY))
    return s


# ============================== THE EIGHT SLIDES ==============================

def slide1():
    s = [chrome(1, tag="MACHINE")]
    s.append(T(M, 282, "Three thousand", 78, INK, font=SERIF))
    s.append(T(M, 366, "Canadian arenas", 78, INK, font=SERIF))
    s.append(T(M, 450, "run one.", 78, INK, font=SERIF))
    s.append(highlight(M, 556, "Only some are Zambonis.", 60, 700))
    s.append(T(M, 634, "The ice resurfacer, counted properly. Eight slides.", 27, MUTED))
    s.append(f'<image x="100" y="672" width="880" height="574" '
             f'preserveAspectRatio="xMidYMid meet" xlink:href="{img("z_machine.png")}"/>')
    return page("".join(s))


def slide2():
    s = [chrome(2, tag="WHAT IT IS")]
    s.append(T(M, 268, "You cannot call it", 62, INK, font=SERIF))
    s.append(T(M, 340, "a Zamboni. Legally.", 62, INK, font=SERIF))
    s.append(dash(M, 430, "The trademark"))
    body = ["ZAMBONI has been a registered trademark",
            "since 1965, and so has the shape of the",
            "machine. The generic word is ice resurfacer.",
            "",
            "Olympia, Engo and Okay Elektra build them",
            "too. The company sends letters."]
    s.append(wrap_lines(body, M, 500, 31, 46, fill=BODY))
    s.append(f'<rect x="{M}" y="800" width="{W-2*M}" height="2" fill="{RULE}"/>')
    s.append(T(M, 884, "14,000+", 72, INK, font=SERIF))
    s.append(T(M, 928, "machines delivered worldwide since 1949", 26, GREY))
    s.append(T(M, 1046, "4,423", 72, INK, font=SERIF))
    s.append(T(M + 212, 1046, "kg", 40, GREY, font=SERIF))
    s.append(T(M, 1090, "empty. 5,148 kg full. It gets heavier as it works", 26, GREY))
    return page("".join(s))


def slide3():
    s = [chrome(3, tag="WHAT IT COSTS")]
    s.append(T(M, 272, "A new one is", 62, INK, font=SERIF))
    s.append(highlight(M, 352, "$117,944.", 62, 322))
    s.append(dash(M, 452, "Minto, Ontario, 2024"))
    s.append(f'<rect x="{M}" y="500" width="{W-2*M}" height="300" fill="{PANEL}"/>')
    rows = [("New, Olympia", "$117,944", "Minto tender, 2024"),
            ("New, electric", "$155,600", "Napanee quote, 2023"),
            ("Used, 2010 electric", "$46,000", "Municibid auction, 2025")]
    for i, (a, b, c) in enumerate(rows):
        y = 572 + i * 86
        s.append(T(M + 40, y, a, 28, INK, weight="600"))
        s.append(T(M + 40, y + 34, c, 21, GREY))
        s.append(T(W - M - 40, y + 14, b, 42, INK, "end", font=SERIF))
    s.append(T(M, 884, "The electric costs about $50,000 more", 30, BODY))
    s.append(T(M, 928, "and saves up to 80% on fuel. Kingston", 30, BODY))
    s.append(T(M, 972, "runs two.", 30, BODY))
    s.append(f'<rect x="{M}" y="1030" width="{W-2*M}" height="140" fill="{INK}"/>')
    s.append(T(M + 40, 1092, "18%", 54, MINT, font=SERIF))
    s.append(T(M + 160, 1086, "of Ontario operators run electric.", 26, WHITE))
    s.append(T(M + 160, 1126, "Another 45% switch within five years.", 26, WHITE))
    return page("".join(s))


def slide4():
    gw, gh, art = steps_grid()
    s = [chrome(4, tag="THE SPINE")]
    s.append(T(M, 272, "Four passes.", 62, INK, font=SERIF))
    s.append(highlight(M, 352, "Ten minutes.", 62, 408))
    s.append(f'<g transform="translate({(W-gw)/2:.0f}, 440)">{art}</g>')
    s.append(T(M, 1136, "Every pass takes 2,500 lb of snow off the ice", 29, BODY))
    s.append(T(M, 1180, "and lays 665 litres of water behind it.", 29, BODY))
    return page("".join(s))


def slide5():
    s = [chrome(5, tag="WHY HOT")]
    s.append(T(M, 280, "The water goes", 64, INK, font=SERIF))
    s.append(T(M, 358, "down at", 64, INK, font=SERIF))
    s.append(highlight(M + 268, 358, "62 degrees.", 64, 372))
    s.append(dash(M, 452, "Not a detail. The whole trick."))
    body = ["Hot water melts into the layer underneath",
            "instead of sitting on top of it, so the two",
            "freeze as one sheet.",
            "",
            "Cold water sets as a skin and chips off by",
            "the second period."]
    s.append(wrap_lines(body, M, 524, 32, 48, fill=BODY))
    s.append(T(M, 846, "1.7 million litres", 46, INK, font=SERIF))
    s.append(T(M, 888, "of hot water per sheet, per season", 26, GREY))
    s.append(f'<rect x="{M}" y="930" width="{W-2*M}" height="200" fill="{PANEL}"/>')
    bx, by = M + 60, 1052
    s.append(f'<rect x="{bx}" y="{by}" width="{W-2*M-120}" height="56" fill="{ICE}" '
             f'stroke="{INK}" stroke-width="3"/>')
    s.append(f'<path d="M{bx+16} {by-5} L{bx+W-2*M-136} {by-5}" stroke="{MINT}" '
             f'stroke-width="11" stroke-linecap="round"/>')
    s.append(f'<rect x="{bx+240}" y="{by-62}" width="200" height="24" fill="{INK}" '
             f'fill-opacity="0.75"/>')
    s.append(T(bx + 340, by - 80, "the towel drags it flat", 22, MUTED, "middle"))
    
    return page("".join(s))


def slide6():
    s = [chrome(6, tag="WHEN IT GOT CHEAP")]
    s.append(T(M, 276, "One patent made", 60, INK, font=SERIF))
    s.append(T(M, 350, "it ordinary.", 60, INK, font=SERIF))
    tl = [("1949", "Frank Zamboni finishes the Model A", "A war surplus chassis in a California rink", False),
          ("1954", "The Boston Bruins buy one", "The NHL never looks back", False),
          ("1964", "The HD series lands the vertical auger", "Still the standard sixty years on", True),
          ("1967", "Andy Schlupp builds his first in Ontario", "Olympia, out of Elmira", False),
          ("1989", "Olympia goes direct electric", "Twenty years before anyone followed", False)]
    y = 460
    for d, head, sub, mark in tl:
        if mark:
            s.append(f'<rect x="{M-14}" y="{y-46}" width="{W-2*M+28}" height="132" fill="{PANEL}"/>')
        s.append(T(M, y, d, 46, VIOLET if not mark else INK, font=SERIF))
        s.append(T(M + 160, y - 6, head, 28, INK, weight="600"))
        s.append(T(M + 160, y + 30, sub, 23, GREY))
        y += 146
    s.append(T(M, 1214, "Hydraulics in 1968 put one in every small rink.", 27, BODY))
    return page("".join(s))


def slide7():
    s = [chrome(7, tag="THE OPERATOR'S CUT")]
    s.append(T(M, 272, "It costs", 60, INK, font=SERIF))
    s.append(highlight(M + 244, 272, "$13.86", 60, 218))
    s.append(T(M, 346, "to resurface a sheet.", 60, INK, font=SERIF))
    s.append(dash(M, 436, "Where it goes"))
    s += cost_bars(M, 510)
    s.append(f'<rect x="{M}" y="968" width="{W-2*M}" height="2" fill="{RULE}"/>')
    s.append(T(M, 1032, "Labour is half of it,", 30, BODY))
    s.append(T(M, 1074, "and nobody bills for it.", 30, INK, weight="700"))
    s.append(T(W - M, 1046, "[modeled]", 22, VIOLET, "end"))
    return page("".join(s))


def slide8():
    s = [chrome(8, tag="THE CLOSE")]
    s.append(T(M, 278, "The hour that", 62, INK, font=SERIF))
    s.append(T(M, 354, "clean sheet buys", 62, INK, font=SERIF))
    s.append(highlight(M, 432, "sells for $385.95.", 62, 530))
    bx, bw = M, W - 2 * M
    s.append(T(M, 540, "", 10))
    s.append(f'<rect x="{bx}" y="566" width="{bw}" height="74" fill="{INK}"/>')
    s.append(f'<rect x="{bx}" y="566" width="{bw*13.86/385.95:.0f}" height="74" fill="{MINT}"/>')
    s.append(T(bx, 690, "$13.86", 40, INK, font=SERIF))
    s.append(T(bx, 726, "the resurface", 23, GREY))
    s.append(T(bx + bw, 690, "$385.95", 40, INK, "end", font=SERIF))
    s.append(T(bx + bw, 726, "one prime hour, Oakville 2026", 23, GREY, "end"))
    s.append(f'<rect x="{M}" y="786" width="56" height="5" fill="{MINT}"/>')
    s.append(T(M + 74, 798, "3.6% OF THE HOUR", 25, INK, weight="700", ls="1.3"))
    s.append(dash(M, 896, "And one last thing"))
    s.append(T(M, 964, "Nearly every resurfacer in Canada", 31, BODY))
    s.append(T(M, 1006, "is built in Canada. Olympia in Elmira.", 31, BODY))
    s.append(T(M, 1048, "Zamboni in Brantford. Okay Elektra", 31, BODY))
    s.append(T(M, 1090, "in Terrebonne.", 31, BODY))
    s.append(f'<rect x="{M}" y="1136" width="{W-2*M}" height="80" fill="{INK}"/>')
    s.append(T(M + 36, 1186, "Count the ten minutes between the fifty you sell.",
               27, MINT, weight="700"))
    return page("".join(s))


if __name__ == "__main__":
    import os
    os.makedirs("ig", exist_ok=True)
    for i, fn in enumerate([slide1, slide2, slide3, slide4,
                            slide5, slide6, slide7, slide8], 1):
        save(fn(), f"ig/zamboni_{i:02d}.jpg")
    print("rendered 8 slides")
