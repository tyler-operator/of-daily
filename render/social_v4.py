#!/usr/bin/env python3
"""OF daily carousel renderer. Brand v4. 1080x1350 JPEG."""
import base64, os, html
from fontTools.ttLib import TTFont

W, H = 1080, 1350
M = 80                      # page margin

# ---- Brand v4 palette (locked 2026-11-10) ----
DARK      = "#0C2A22"
DEEP      = "#081E18"
CREAM     = "#F6F3EC"
MINT      = "#4FF0A0"
IRIS      = "#7C6BE8"
ON_DARK   = "#F1F0E8"
ON_MUTED  = "#A8BDB2"
RULE      = "#4A5B52"

SANS  = "Space Grotesk"
SERIF = "Libre Caslon Text"

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
FONTDIR = os.path.join(ASSETS, "fonts")
LOCKUP = os.path.join(ASSETS, "of-lockup-white.png")

# ---------- text measurement ----------
class Metrics:
    def __init__(self, path):
        f = TTFont(path)
        self.upm = f["head"].unitsPerEm
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]
        self.gs = f.getGlyphSet()
    def width(self, text, size, tracking=0.0):
        total = 0
        for ch in text:
            gn = self.cmap.get(ord(ch))
            if gn is None:
                gn = self.cmap.get(ord(" "))
            adv = self.hmtx[gn][0] if gn in self.hmtx.metrics else self.upm // 2
            total += adv
        return total / self.upm * size + tracking * size * max(len(text) - 1, 0)

_M = {
    ("sans", 400):  Metrics(os.path.join(FONTDIR, "SpaceGrotesk-Regular.ttf")),
    ("sans", 500):  Metrics(os.path.join(FONTDIR, "SpaceGrotesk-Medium.ttf")),
    ("sans", 700):  Metrics(os.path.join(FONTDIR, "SpaceGrotesk-Bold.ttf")),
    ("serif", 400): Metrics(os.path.join(FONTDIR, "LibreCaslonText-Regular.ttf")),
    ("serif", 700): Metrics(os.path.join(FONTDIR, "LibreCaslonText-Bold.ttf")),
}

def measure(text, fam, size, weight=400, tracking=0.0):
    key = (fam, weight if (fam, weight) in _M else 400)
    return _M[key].width(text, size, tracking)

def wrap(text, fam, size, maxw, weight=400, tracking=0.0):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if measure(trial, fam, size, weight, tracking) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

# ---------- svg helpers ----------
def esc(s): return html.escape(str(s), quote=True)

def text(x, y, s, fam="sans", size=30, weight=400, fill=ON_DARK,
         anchor="start", tracking=0.0, upper=False, opacity=None):
    if upper: s = str(s).upper()
    f = SERIF if fam == "serif" else SANS
    ls = f' letter-spacing="{tracking*size:.2f}"' if tracking else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{f}" font-size="{size:.1f}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}{op}>{esc(s)}</text>')

def para(x, y, s, fam="sans", size=30, weight=400, fill=ON_MUTED,
         maxw=W-2*M, lh=1.5, tracking=0.0):
    out, yy = [], y
    for ln in wrap(s, fam, size, maxw, weight, tracking):
        out.append(text(x, yy, ln, fam, size, weight, fill, tracking=tracking))
        yy += size * lh
    return "\n".join(out), yy

def rect(x, y, w, h, fill, rx=0, opacity=None):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{op}/>'

def line(x1, y1, x2, y2, stroke=RULE, w=1, opacity=None, cap="butt", dash=None):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{w}" stroke-linecap="{cap}"{op}{da}/>')

def circle(cx, cy, r, fill="none", stroke=None, sw=2, opacity=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{st}{op}/>'

def tick(x, y, w=92, h=5, fill=MINT):
    return rect(x, y, w, h, fill)

def eyebrow(x, y, s):
    return text(x, y, s, "sans", 21, 700, MINT, tracking=0.16, upper=True)

# ---------- chrome ----------
_lock_b64 = None
def lockup_uri():
    global _lock_b64
    if _lock_b64 is None:
        with open(LOCKUP, "rb") as fh:
            _lock_b64 = base64.b64encode(fh.read()).decode()
    return "data:image/png;base64," + _lock_b64

def chrome(n, total=8):
    lw = 250
    lh = lw * 408 / 7027
    parts = [
        f'<image x="{M}" y="{M-lh/2-6:.1f}" width="{lw}" height="{lh:.1f}" '
        f'preserveAspectRatio="xMidYMid meet" href="{lockup_uri()}" opacity="0.92"/>',
        text(W-M, M+8, f"{n}/{total}", "sans", 22, 500, ON_MUTED, anchor="end", tracking=0.08),
        line(M, M+34, W-M, M+34, RULE, 1, opacity=0.55),
        text(M, H-M+4, "@operatorsfund", "sans", 19, 500, ON_MUTED, tracking=0.08),
        text(W-M, H-M+4, "ALL FIGURES CAD", "sans", 17, 500, ON_MUTED,
             anchor="end", tracking=0.14),
        line(M, H-M-30, W-M, H-M-30, RULE, 1, opacity=0.35),
    ]
    return "\n".join(parts)

def page(body, n):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{DARK}"/>
{body}
{chrome(n)}
</svg>'''

# ---------- art ----------
def art_disc(cx, cy, R, blades=28):
    """Turbine disc seen face on: hub, web, rim, blades."""
    import math
    o = [circle(cx, cy, R*0.30, "none", RULE, 3, opacity=0.9)]          # bore
    o.append(circle(cx, cy, R*0.62, "none", ON_MUTED, 2, opacity=0.5))  # web
    o.append(circle(cx, cy, R*0.78, "none", MINT, 4))                   # rim
    for i in range(blades):
        a = 2*math.pi*i/blades
        x1, y1 = cx + R*0.78*math.cos(a), cy + R*0.78*math.sin(a)
        x2, y2 = cx + R*1.02*math.cos(a), cy + R*1.02*math.sin(a)
        o.append(line(x1, y1, x2, y2, MINT, 7, opacity=0.5, cap="round"))
    o.append(circle(cx, cy, R*0.30, DARK))
    o.append(circle(cx, cy, R*0.30, "none", MINT, 3, opacity=0.8))
    return "\n".join(o)

def art_blockdown(x, y, w, h, keep=0.052):
    """Big forging block shrinking to a small finished part."""
    o = [rect(x, y, w, h, ON_MUTED, rx=6, opacity=0.18),
         rect(x, y, w, h, "none", rx=6)]
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{ON_MUTED}" stroke-width="2" opacity="0.55"/>')
    kh = h * keep ** 0.5
    kw = w * keep ** 0.5
    o.append(rect(x + (w-kw)/2, y + (h-kh)/2, kw, kh, MINT, rx=3))
    return "\n".join(o)

def art_steps(x, y, w, labels):
    """Horizontal numbered sequence strip."""
    n = len(labels)
    gap = 16
    bw = (w - gap*(n-1)) / n
    o = []
    for i, lab in enumerate(labels):
        bx = x + i*(bw+gap)
        active = i in (3, 4)
        o.append(rect(bx, y, bw, 6, MINT if active else RULE,
                      opacity=None if active else 0.8))
        o.append(text(bx, y+42, f"{i+1}", "serif", 30, 400,
                      MINT if active else ON_MUTED))
        for j, ln in enumerate(wrap(lab, "sans", 21, bw, 500)):
            o.append(text(bx, y+76+j*27, ln, "sans", 21, 500,
                          ON_DARK if active else ON_MUTED))
    return "\n".join(o)

# ---------- extra art ----------
def art_ladder(x, y, w, rows, active_idx=None):
    """Four stacked layers, widest at the bottom. Contracts down, parts up."""
    o = []
    n = len(rows)
    rh = 104
    gap = 14
    for i, lab in enumerate(rows):
        frac = 0.46 + 0.18 * i
        bw = w * frac
        bx = x + (w - bw) / 2
        by = y + i * (rh + gap)
        hot = (active_idx == i)
        o.append(rect(bx, by, bw, rh, MINT if hot else ON_MUTED, rx=8,
                      opacity=None if hot else 0.13))
        o.append(text(x + w/2, by + rh/2 + 12, lab, "sans", 32, 500,
                      DARK if hot else ON_DARK, anchor="middle", tracking=0.04))
    tot = n * rh + (n-1) * gap
    ax = x - 16
    o.append(line(ax, y + 10, ax, y + tot - 10, MINT, 2, opacity=0.5))
    o.append(f'<path d="M{ax-7},{y+tot-22} L{ax},{y+tot-8} L{ax+7},{y+tot-22}" fill="none" stroke="{MINT}" stroke-width="2" opacity="0.6"/>')
    bx2 = x + w + 16
    o.append(line(bx2, y + 10, bx2, y + tot - 10, IRIS, 2, opacity=0.6))
    o.append(f'<path d="M{bx2-7},{y+22} L{bx2},{y+8} L{bx2+7},{y+22}" fill="none" stroke="{IRIS}" stroke-width="2" opacity="0.7"/>')
    return "\n".join(o), y + tot

def bullets(x, y, items, size=29, lh=1.48, gap=40, maxw=None, fill=ON_MUTED):
    o, yy = [], y
    maxw = maxw or (W - 2*M - 44)
    for it in items:
        o.append(circle(x + 7, yy - 9, 5, MINT))
        p, y2 = para(x + 32, yy, it, "sans", size, 400, fill, maxw=maxw, lh=lh)
        o.append(p)
        yy = y2 + gap
    return "\n".join(o), yy

# ---------- slides ----------
def slide1():
    b = [eyebrow(M, M+110, "The machine series · No. 1")]
    y = M + 250
    for ln in ["Everyone is talking", "about defence spending."]:
        b.append(text(M, y, ln, "serif", 82, 400, ON_DARK)); y += 100
    y += 48
    for ln, col in [("Almost nobody can", ON_DARK), ("tell you who", ON_DARK),
                    ("actually builds it.", MINT)]:
        b.append(text(M, y, ln, "serif", 82, 400, col)); y += 100
    y += 48
    b.append(tick(M, y)); y += 96
    p, _ = para(M, y, "Four layers. The money behaves differently at every one.",
                "sans", 31, 400, ON_MUTED, maxw=W-2*M-40)
    b.append(p)
    return page("\n".join(b), 1)

def slide2():
    b = [eyebrow(M, M+110, "How it is built")]
    y = M + 185
    b.append(text(M, y, "Four layers", "serif", 74, 400, ON_DARK)); y += 56
    b.append(tick(M, y)); y += 96
    art, y = art_ladder(M + 40, y, W - 2*M - 80,
                        ["OEM", "TIER 1", "TIER 2", "TIER 3"])
    b.append(art)
    y += 80
    b.append(text(M, y, "CONTRACTS DOWN", "sans", 21, 700, MINT, tracking=0.14))
    b.append(text(W-M, y, "PARTS UP", "sans", 21, 700, IRIS,
                  anchor="end", tracking=0.14))
    y += 76
    b.append(line(M, y, W-M, y, RULE, 1, opacity=0.5)); y += 68
    p, _ = para(M, y, "Nobody at the top builds much. The layer that cuts the metal "
                      "sits at the bottom and sees none of the aircraft.",
                "sans", 29, 400, ON_DARK, maxw=W-2*M-20, lh=1.45)
    b.append(p)
    return page("\n".join(b), 2)

def slide3():
    b = [eyebrow(M, M+110, "Layer one · the OEM")]
    y = M + 185
    b.append(text(M, y, "Owns the customer", "serif", 62, 400, ON_DARK)); y += 50
    b.append(tick(M, y)); y += 62
    b.append(text(M, y, "Boeing · Airbus · Embraer · Bombardier",
                  "sans", 27, 500, MINT)); y += 94
    bl, y = bullets(M, y, [
        "Designs the aircraft and integrates it. Builds very little of it.",
        "Final assembly is roughly 10 to 20 percent of the airframe's value.",
        "Owns the type certificate, so it owns the programme for its life.",
        "Holds the order book and sets the payment terms for everyone below.",
    ])
    b.append(bl)
    y += 28
    b.append(line(M, y, W-M, y, RULE, 1, opacity=0.5)); y += 68
    p, _ = para(M, y, "Pays its Tier 1s in 90 to 120 days. That clock gets passed down "
                      "the chain unchanged.",
                "sans", 28, 400, ON_DARK, maxw=W-2*M-20, lh=1.45)
    b.append(p)
    return page("\n".join(b), 3)

def slide4():
    b = [eyebrow(M, M+110, "Layer two · Tier 1")]
    y = M + 185
    b.append(text(M, y, "Owns the system", "serif", 64, 400, ON_DARK)); y += 50
    b.append(tick(M, y)); y += 62
    b.append(text(M, y, "Pratt & Whitney Canada · Safran · GE · Collins",
                  "sans", 26, 500, MINT)); y += 94
    bl, y = bullets(M, y, [
        "Delivers a whole system. An entire engine, a complete gear set, the avionics suite.",
        "Hundreds of millions to billions in revenue.",
        "Risk-sharing partner. Funds the development, recovers it across decades of deliveries.",
        "Carries design authority for its system, and owns the supplier base beneath it.",
    ])
    b.append(bl)
    y += 28
    b.append(line(M, y, W-M, y, RULE, 1, opacity=0.5)); y += 68
    p, _ = para(M, y, "Canada has no large commercial OEM any more, but it has Tier 1s "
                      "feeding every global programme.",
                "sans", 28, 400, ON_DARK, maxw=W-2*M-20, lh=1.45)
    b.append(p)
    return page("\n".join(b), 4)

def slide5():
    b = [eyebrow(M, M+110, "Layers three and four")]
    y = M + 185
    b.append(text(M, y, "Build to print", "serif", 64, 400, ON_DARK)); y += 50
    b.append(tick(M, y)); y += 78
    blocks = [
        ("TIER 2", "$20M to $500M", "Sub-assemblies. A gearbox, an actuator, a wire harness, a wing rib assembly. Some process engineering of its own.", False),
        ("TIER 3", "$2M to $50M", "Single-process detail parts. Machining, forming, heat treat, surface finish. No design authority at all.", True),
    ]
    for lab, size, body, hi in blocks:
        if hi:
            b.append(rect(M-22, y-50, W-2*M+44, 212, MINT, rx=10, opacity=0.10))
            b.append(rect(M-22, y-50, 6, 212, MINT, rx=3))
        b.append(text(M, y, lab, "sans", 25, 700, MINT if hi else ON_MUTED, tracking=0.14))
        b.append(text(W-M, y, size, "serif", 32, 400, ON_DARK, anchor="end"))
        p, y2 = para(M, y+48, body, "sans", 26, 400, ON_MUTED, maxw=W-2*M-30, lh=1.45)
        b.append(p)
        y = y2 + 76
    y -= 20
    b.append(line(M, y, W-M, y, RULE, 1, opacity=0.5)); y += 54
    p, y = para(M, y, "Long-term agreements run three to ten years with price-down "
                      "clauses of two to three percent a year, written in.",
                "sans", 27, 400, ON_MUTED, maxw=W-2*M-20, lh=1.45)
    b.append(p); y += 22
    p2, _ = para(M, y, "A drawing, a forging and a due date.", "sans", 29, 500,
                 ON_DARK, maxw=W-2*M-20)
    b.append(p2)
    return page("\n".join(b), 5)

def slide6():
    b = [eyebrow(M, M+110, "Now pick up one part at the bottom")]
    y = M + 185
    b.append(text(M, y, "The disc", "serif", 72, 400, ON_DARK)); y += 54
    b.append(tick(M, y)); y += 64
    p, y = para(M, y, "The wheel that carries the blades. It holds them while they "
                      "spin at 10,000 rpm and takes the load.",
                "sans", 29, 400, ON_MUTED, maxw=W-2*M-30)
    b.append(p)
    b.append(art_disc(W/2, y+235, 205))
    y += 500
    b.append(line(M, y, W-M, y, RULE, 1, opacity=0.5)); y += 56
    b.append(text(M, y, "210 lb", "serif", 54, 400, ON_DARK))
    b.append(text(M+220, y, "forging goes in", "sans", 28, 400, ON_MUTED)); y += 92
    b.append(text(M, y, "11 lb", "serif", 54, 400, MINT))
    b.append(text(M+220, y, "finished disc comes out", "sans", 28, 400, ON_DARK))
    return page("\n".join(b), 6)

def slide7():
    b = [eyebrow(M, M+110, "The same part, climbing back up")]
    y = M + 180
    b.append(text(M, y, "Four rungs", "serif", 66, 400, ON_DARK)); y += 50
    b.append(tick(M, y)); y += 70
    rungs = [
        ("TIER 3", "Machines the disc", "$230 billed an hour. $193 to run the machine.", True),
        ("TIER 2", "Builds the rotor stage", "Stacks the discs, fits the blades, balances it.", False),
        ("TIER 1", "Builds and tests the engine", "Pratt & Whitney Canada, in Longueuil.", False),
        ("OEM", "Hangs it on the wing", "And sells the aircraft.", False),
    ]
    for i, (lab, what, note, hi) in enumerate(rungs):
        if hi:
            b.append(rect(M-22, y-44, W-2*M+44, 150, MINT, rx=10, opacity=0.10))
            b.append(rect(M-22, y-44, 6, 150, MINT, rx=3))
        b.append(text(M, y, lab, "sans", 24, 700, MINT if hi else ON_MUTED, tracking=0.14))
        b.append(text(M, y+48, what, "serif", 34, 400, ON_DARK))
        b.append(text(M, y+88, note, "sans", 24, 400, ON_MUTED))
        if i < len(rungs) - 1:
            b.append(f'<path d="M{W-M-26},{y+96} L{W-M-26},{y+44}" stroke="{IRIS}" stroke-width="2" opacity="0.55"/>')
            b.append(f'<path d="M{W-M-33},{y+58} L{W-M-26},{y+44} L{W-M-19},{y+58}" fill="none" stroke="{IRIS}" stroke-width="2" opacity="0.7"/>')
        y += 168
    y -= 16
    b.append(line(M, y, W-M, y, RULE, 1, opacity=0.5)); y += 54
    p, _ = para(M, y, "Every rung adds a certification the rung below cannot buy quickly.",
                "sans", 28, 500, ON_DARK, maxw=W-2*M-20, lh=1.45)
    b.append(p)
    return page("\n".join(b), 7)

def slide8():
    b = [eyebrow(M, M+110, "Part one of three")]
    y = M + 300
    for ln in ["Now you know", "who builds it."]:
        b.append(text(M, y, ln, "serif", 84, 400, ON_DARK)); y += 102
    y += 64
    for ln, col in [("Next: who", ON_DARK), ("keeps the money.", MINT)]:
        b.append(text(M, y, ln, "serif", 84, 400, col)); y += 102
    y += 50
    b.append(tick(M, y)); y += 96
    p, _ = para(M, y, "It is not the layer you would guess. The company whose name is "
                      "on the aircraft lost money on every one it delivered last quarter.",
                "sans", 29, 400, ON_MUTED, maxw=W-2*M-30, lh=1.5)
    b.append(p)
    return page("\n".join(b), 8)

SLIDES = [slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8]

def save(outdir):
    import cairosvg
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for i, fn in enumerate(SLIDES, 1):
        svg = fn()
        with open(os.path.join(outdir, f"slide{i}.svg"), "w") as fh: fh.write(svg)
        pp = os.path.join(outdir, f"slide{i}.png")
        cairosvg.svg2png(bytestring=svg.encode(), write_to=pp,
                         output_width=W, output_height=H, background_color=DARK)
        paths.append(pp)
    return paths

if __name__ == "__main__":
    for p in save(os.path.join(os.path.dirname(__file__), "..", "out")): print(p)
