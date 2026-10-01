"""Builds the profile SVGs in assets/ and rewrites README.md to point at them.

Filenames carry a short content hash so GitHub's image proxy can't serve a
stale copy after an edit. Run from the repo root:  python scripts/build.py
"""
import hashlib
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

BG, EDGE, FG, MUTED, DIM = "#0b0f17", "#1e2633", "#e6edf3", "#8b949e", "#9aa4b2"
ACCENT, GOLD, GREEN = "#a78bfa", "#f5b544", "#3fb950"

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } .rm-hide { display: none; } }"


def esc(s):
    return html.escape(s, quote=True)


def mono_w(s, size):
    return round(len(s) * size * 0.6, 1)


# --------------------------------------------------------------------- header

def header():
    name = "Maadhav"
    tags = ["making models smaller without making them wrong",
            "finding things in SEM images that don't want to be found"]
    W, H, T = 860, 260, 14.0

    # (x, y, label, label anchor)
    nodes = [(556, 92, "weights", "top"), (650, 54, "int8", "top"),
             (770, 70, "kernels", "top"), (812, 150, "runtime", "below"),
             (740, 212, "SEM", "right"), (628, 200, "layouts", "below"),
             (560, 172, "evals", "left")]
    hub = (690, 136, "fast ∧ correct")
    path = nodes + [hub[:2] + (hub[2], "below")]

    def pct(t):
        return f"{t / T * 100:.3f}%"

    css = [
        ".hello { animation: fade .6s ease .05s both; }",
        ".name { animation: rise .9s cubic-bezier(.2,.8,.2,1) .25s both; }",
        ".bar { transform-box: fill-box; transform-origin: left center; animation: grow .7s cubic-bezier(.2,.8,.2,1) .9s both; }",
        ".meta { animation: fade .8s ease .7s both; }",
        ".tag { opacity: 0; animation: tag 6s ease-in-out infinite both; }",
        ".tag.t0 { opacity: 1; }",
        ".dot { animation: blink 1.2s steps(2, jump-none) infinite; }",
        ".ping { transform-box: fill-box; transform-origin: center; animation: ping 2.2s cubic-bezier(0,0,.2,1) infinite; }",
        f".ringfade {{ animation: ringfade {T}s linear infinite; }}",
        "@keyframes fade { from { opacity: 0; } to { opacity: 1; } }",
        "@keyframes rise { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }",
        "@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }",
        "@keyframes tag { 0% { opacity: 0; transform: translateY(10px); } 8%, 42% { opacity: 1; transform: none; } 50%, 100% { opacity: 0; transform: translateY(-10px); } }",
        "@keyframes blink { 0% { opacity: 1; } 100% { opacity: .15; } }",
        "@keyframes ping { 0% { opacity: .8; transform: scale(1); } 75%, 100% { opacity: 0; transform: scale(2.6); } }",
        f"@keyframes ringfade {{ 0%, {pct(.3)} {{ opacity: 0; }} {pct(.6)}, {pct(12.6)} {{ opacity: 1; }} {pct(13.2)}, 100% {{ opacity: 0; }} }}",
    ]

    # the reticle hops node to node; each hop lights the next node and draws the edge
    first, step, move = 1.0, 1.3, 0.45
    arrive = [first + 0.0]
    hop = [f"0% {{ transform: translate({path[0][0]}px, {path[0][1]}px); }}"]
    for i in range(1, len(path)):
        leave = first + (i - 1) * step + (step - move)
        at = leave + move
        arrive.append(at)
        x0, y0 = path[i - 1][:2]
        x1, y1 = path[i][:2]
        hop.append(f"{pct(leave)} {{ transform: translate({x0}px, {y0}px); }}")
        hop.append(f"{pct(at)} {{ transform: translate({x1}px, {y1}px); }}")
    hop.append(f"100% {{ transform: translate({path[-1][0]}px, {path[-1][1]}px); }}")
    css.append(f".hop {{ animation: hop {T}s cubic-bezier(.65,0,.35,1) infinite; }}")
    css.append("@keyframes hop { " + " ".join(hop) + " }")

    edges = []
    for i in range(1, len(path)):
        edges.append((path[i - 1][:2], path[i][:2], arrive[i] - move, arrive[i], .7))
    # spokes from the hub once the loop closes
    for j, n in enumerate([0, 1, 2, 4]):
        s = arrive[-1] + .25 + j * .25
        edges.append((hub[:2], nodes[n][:2], s, s + .5, .25))

    edge_svg = []
    for k, ((x0, y0), (x1, y1), s, e, op) in enumerate(edges):
        L = round(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5, 1)
        css.append(f".e{k} {{ stroke-dasharray: {L} {L}; animation: e{k} {T}s ease-in-out infinite; }}")
        css.append(f"@keyframes e{k} {{ 0%, {pct(s)} {{ stroke-dashoffset: {L}; opacity: 1; }} "
                   f"{pct(e)}, {pct(12.6)} {{ stroke-dashoffset: 0; opacity: 1; }} {pct(13.2)}, 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}")
        edge_svg.append(f'<path class="e{k}" d="M{x0} {y0}L{x1} {y1}" stroke="{ACCENT}" stroke-opacity="{op}" stroke-width="1.4" fill="none"/>')

    node_svg = []
    for i, (x, y, label, where) in enumerate(path):
        hubnode = i == len(path) - 1
        col = GOLD if hubnode else ACCENT
        t = arrive[i]
        css.append(f".n{i} {{ transform-box: fill-box; transform-origin: center; animation: n{i} {T}s ease-out infinite; }}")
        css.append(f"@keyframes n{i} {{ 0%, {pct(t - .05)} {{ opacity: 0; transform: scale(1.9); }} {pct(t + .3)}, {pct(12.6)} {{ opacity: 1; transform: scale(1); }} {pct(13.2)}, 100% {{ opacity: 0; transform: scale(1); }} }}")
        css.append(f".l{i} {{ animation: l{i} {T}s linear infinite; }}")
        css.append(f"@keyframes l{i} {{ 0%, {pct(t - .05)} {{ fill-opacity: .4; }} {pct(t + .15)}, {pct(12.6)} {{ fill-opacity: 1; }} {pct(13.2)}, 100% {{ fill-opacity: .4; }} }}")
        lx, ly, anchor = {"top": (x, y - 16, "middle"), "below": (x, y + 22, "middle"),
                          "right": (x + 12, y + 4, "start"), "left": (x - 12, y + 4, "end")}[where]
        ring = (f'<circle class="ping rm-hide" cx="{x}" cy="{y}" r="5" fill="none" stroke="{GOLD}" stroke-width="1.2"/>'
                if hubnode else "")
        node_svg.append(
            f'{ring}<circle cx="{x}" cy="{y}" r="4.5" fill="{BG}" stroke="{GOLD if hubnode else "#3a4556"}" stroke-width="1.4"/>\n'
            f'<circle class="n{i}" cx="{x}" cy="{y}" r="4.5" fill="{col}"/>\n'
            f'<text class="l{i}" x="{lx}" y="{ly}" text-anchor="{anchor}" font-family="{MONO}" font-size="11" fill="{GOLD if hubnode else FG}">{esc(label)}</text>')

    tag_svg = "\n".join(
        f'<text x="64" y="188" class="tag t{i}" font-family="{MONO}" font-size="17" fill="{FG}" '
        f'textLength="{mono_w(t, 17)}" lengthAdjust="spacing" style="animation-delay:{1.2 + 3 * i}s">{esc(t)}</text>'
        for i, t in enumerate(tags))

    status = "usually mid-experiment"
    sw = mono_w(status, 11)
    sx = W - 34 - sw

    alt = f"{name}. " + ". ".join(t.capitalize() for t in tags) + ". ECE by training, ML and systems by habit."
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}">
<style>
{chr(10).join(css)}
{REDUCED}
</style>
<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
  <radialGradient id="glow"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".14"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
  <clipPath id="cardclip"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{EDGE}"/>
<g clip-path="url(#cardclip)">
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <circle cx="{hub[0]}" cy="{hub[1]}" r="190" fill="url(#glow)"/>
</g>
<text class="hello" x="40" y="70" font-family="{MONO}" font-size="14" fill="{MUTED}">hey, i'm</text>
<text class="name" x="38" y="130" font-family="{SANS}" font-size="64" font-weight="700" letter-spacing="-1.5" fill="{FG}">{name}</text>
<rect class="bar" x="42" y="146" width="64" height="3" rx="1.5" fill="{ACCENT}"/>
<text x="40" y="188" font-family="{MONO}" font-size="17" fill="{ACCENT}">›</text>
{tag_svg}
<text class="meta" x="40" y="226" font-family="{SANS}" font-size="13" fill="{MUTED}">ECE by training. ML and systems by habit.</text>
{"".join(edge_svg)}
{chr(10).join(node_svg)}
<g class="ringfade rm-hide"><g class="hop" transform="translate({path[0][0]} {path[0][1]})">
  <circle r="11" fill="none" stroke="{ACCENT}" stroke-width="1.3"/>
  <path d="M-19 0H-14M14 0H19M0 -19V-14M0 14V19" stroke="{ACCENT}" stroke-width="1.3"/>
</g></g>
<circle class="dot" cx="{sx - 11:.1f}" cy="238" r="3.5" fill="{GREEN}"/>
<text x="{sx:.1f}" y="242" font-family="{MONO}" font-size="11" fill="{MUTED}" textLength="{sw}" lengthAdjust="spacing">{status}</text>
</svg>
'''


# ------------------------------------------------------------------- terminal

def terminal():
    # (command, [(color, text), ...] output)
    session = [
        ("whoami", [(DIM, "ece student who kept ending up in the inference code.")]),
        ("cat now.txt", [(DIM, "a local inference runtime · int8 calibration · SEM patch matching")]),
        ("git log --oneline -1", [(GOLD, "a41c09e "), (GREEN, "fix: "),
                                  (DIM, "int8 was fine. calibration set was 12 images.")]),
    ]
    T = 17.0
    pct = lambda t: f"{t / T * 100:.3f}%"
    css = [f".all {{ animation: out {T}s linear infinite; }}",
           f"@keyframes out {{ 0%, {pct(16)} {{ opacity: 1; }} {pct(16.6)}, 100% {{ opacity: 0; }} }}",
           ".cur { animation: blink 1s steps(2, jump-none) infinite; }",
           "@keyframes blink { 0% { opacity: .9; } 100% { opacity: 0; } }"]
    body = []
    t, y, k = 0.5, 74, 0
    cw = 8.4
    for cmd, out in session:
        # prompt line appears, then the cursor-mask slides right one char at a time
        n = len(cmd)
        typing = n * 0.07
        css.append(f".a{k} {{ animation: a{k} {T}s linear infinite; }}")
        css.append(f"@keyframes a{k} {{ 0%, {pct(t - .01)} {{ opacity: 0; }} {pct(t)}, 100% {{ opacity: 1; }} }}")
        css.append(f".c{k} {{ animation: c{k} {T}s linear infinite; }}")
        css.append(f"@keyframes c{k} {{ 0% {{ transform: translateX(0); }} {pct(t + .35)} {{ transform: translateX(0); animation-timing-function: steps({n}, end); }} "
                   f"{pct(t + .35 + typing)}, 100% {{ transform: translateX({n * cw:.1f}px); }} }}")
        css.append(f".k{k} {{ animation: k{k} {T}s linear infinite; }}")
        css.append(f"@keyframes k{k} {{ 0%, {pct(t + .65 + typing)} {{ opacity: .85; }} {pct(t + .66 + typing)}, 100% {{ opacity: 0; }} }}")
        body.append(
            f'<g class="a{k}"><text x="30" y="{y}" font-family="{MONO}" font-size="14" fill="{GREEN}">$</text>'
            f'<text x="46.8" y="{y}" font-family="{MONO}" font-size="14" fill="{FG}" textLength="{n * cw:.1f}" lengthAdjust="spacing">{esc(cmd)}</text>\n'
            f'  <g class="c{k} rm-hide"><rect x="45.8" y="{y - 15}" width="{n * cw + 4:.1f}" height="21" fill="{BG}"/>'
            f'<rect class="k{k}" x="46.8" y="{y - 13}" width="8.4" height="17" fill="{FG}"/></g></g>')
        t += .85 + typing
        k += 1
        y += 25
        css.append(f".a{k} {{ animation: a{k} {T}s linear infinite; }}")
        css.append(f"@keyframes a{k} {{ 0%, {pct(t - .01)} {{ opacity: 0; }} {pct(t)}, 100% {{ opacity: 1; }} }}")
        spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for c, s in out)
        body.append(f'<g class="a{k}"><text x="30" y="{y}" font-family="{MONO}" font-size="14">{spans}</text></g>')
        t += .7
        k += 1
        y += 25
    css.append(f".a{k} {{ animation: a{k} {T}s linear infinite; }}")
    css.append(f"@keyframes a{k} {{ 0%, {pct(t - .01)} {{ opacity: 0; }} {pct(t)}, 100% {{ opacity: 1; }} }}")
    body.append(f'<g class="a{k}"><text x="30" y="{y}" font-family="{MONO}" font-size="14" fill="{GREEN}">$</text>'
                f'<rect class="cur" x="46.8" y="{y - 13}" width="8.4" height="17" fill="{FG}"/></g>')

    W, H = 860, y + 29
    alt = "Terminal. " + " ".join(f"{c}: {''.join(s for _, s in o)}" for c, o in session)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}">
<style>
{chr(10).join(css)}
{REDUCED}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{EDGE}"/>
<circle cx="24" cy="22" r="5.5" fill="#ff5f57"/><circle cx="42" cy="22" r="5.5" fill="#febc2e"/><circle cx="60" cy="22" r="5.5" fill="#28c840"/>
<text x="{W / 2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">maadhav@localhost: ~</text>
<path d="M1 42H{W - 1}" stroke="{EDGE}"/>
<g class="all">
{chr(10).join(body)}
</g>
</svg>
'''


# -------------------------------------------------------------------- divider

def divider(label):
    W = 860
    half = 16 + 5.1 * len(label)
    l, r = W / 2 - half, W / 2 + half
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="34" viewBox="0 0 {W} 34" role="img" aria-label="{label.lower()}">
<style>
.p1 {{ animation: p1 2.8s cubic-bezier(.5,0,.75,0) infinite; }}
.p2 {{ animation: p2 2.8s cubic-bezier(.5,0,.75,0) infinite; }}
@keyframes p1 {{ from {{ transform: translateX(0); }} to {{ transform: translateX({l + 110:.1f}px); }} }}
@keyframes p2 {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{l + 110:.1f}px); }} }}
.node {{ animation: node 2.8s ease-out infinite; }}
@keyframes node {{ 0%, 88% {{ fill-opacity: .35; }} 96% {{ fill-opacity: 1; }} 100% {{ fill-opacity: .35; }} }}
{REDUCED}
</style>
<defs>
<linearGradient id="pl"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset="1" stop-color="{ACCENT}"/></linearGradient>
<linearGradient id="pr"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>
<clipPath id="cl"><rect x="0" y="15" width="{l:.1f}" height="4"/></clipPath>
<clipPath id="cr"><rect x="{r:.1f}" y="15" width="{l:.1f}" height="4"/></clipPath>
</defs>
<path d="M0 17H{l:.1f}M{r:.1f} 17H{W}" stroke="{MUTED}" stroke-opacity=".35"/>
<g clip-path="url(#cl)"><rect class="p1 rm-hide" x="-110" y="16" width="110" height="2" fill="url(#pl)"/></g>
<g clip-path="url(#cr)"><rect class="p2 rm-hide" x="{W}" y="16" width="110" height="2" fill="url(#pr)"/></g>
<circle class="node" cx="{l:.1f}" cy="17" r="3" fill="{ACCENT}"/>
<circle class="node" cx="{r:.1f}" cy="17" r="3" fill="{ACCENT}"/>
<text x="{W / 2}" y="21.5" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{MUTED}">{label}</text>
</svg>
'''


# ---------------------------------------------------------------------- stack

STACK = [
    [("Python", "#60a5fa"), ("C", "#60a5fa"), ("Java", "#60a5fa"), ("TypeScript", "#60a5fa"),
     ("PyTorch", "#fb923c"), ("NumPy", "#fb923c"), ("OpenCV", "#fb923c"), ("Hugging Face", "#fb923c"),
     ("Jupyter", "#fb923c")],
    [("int8 / PTQ", ACCENT), ("SEM imagery", ACCENT), ("GDSII", ACCENT), ("TF-IDF", ACCENT),
     ("Docker", "#34d399"), ("Linux", "#34d399"), ("Git", "#34d399"), ("Bash", "#34d399")],
]


def stack():
    W, H = 860, 104
    css, rows = [], []
    for i, items in enumerate(STACK):
        def pills(items, x0):
            out, x = [], x0
            for name, dot in items:
                tw = mono_w(name, 14)
                w = round(30 + tw + 16, 1)
                out.append(f'<g transform="translate({x:.1f} {10 + 50 * i})"><rect width="{w}" height="34" rx="17.0" fill="#0f1520" stroke="#263043"/>'
                           f'<circle cx="18" cy="17.0" r="4" fill="{dot}"/><text x="30" y="22.0" font-family="{MONO}" font-size="14" fill="#c9d1d9" '
                           f'textLength="{tw}" lengthAdjust="spacing">{esc(name)}</text></g>')
                x += w + 10
            return out, x
        # repeat the set until one copy is wider than the card, then draw it twice for a seamless loop
        seq = list(items)
        _, span = pills(seq, 0)
        while span < W + 40:
            seq += items
            _, span = pills(seq, 0)
        a, _ = pills(seq, 0)
        b, _ = pills(seq, span)
        dur = round(span / 32, 1)
        css.append(f".m{i} {{ animation: m{i} {dur}s linear infinite {'reverse' if i else 'normal'}; }}")
        css.append(f"@keyframes m{i} {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{span:.1f}px); }} }}")
        rows.append(f'<g class="m{i}"><g>{"".join(a)}</g><g>{"".join(b)}</g></g>')
    alt = "Stack: " + ", ".join(n for row in STACK for n, _ in row)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}">
<style>
{chr(10).join(css)}
{REDUCED}
</style>
<defs><linearGradient id="fg"><stop offset="0" stop-color="#000"/><stop offset=".07" stop-color="#fff"/><stop offset=".93" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="fade"><rect width="{W}" height="{H}" fill="url(#fg)"/></mask></defs><g mask="url(#fade)">{"".join(rows)}</g>
</svg>
'''


# ----------------------------------------------------------------------- work

# (title, one-liner, pill, highlight)
WORK = [
    ("semicon-driftsense", "1 µm patch, ~10 µm SEM frame, unknown zoom and rotation",
     "runner-up · SEMICON '26", True),
    ("neka-rt", "local-first inference engine. nothing leaves the machine.", "in progress", False),
    ("quantization-lab", "post-training quantization, worked out by hand before trusting a library", "ongoing", False),
    ("hiver-email-suggested-response", "retrieval-grounded reply drafts, plus a harness that scores them", "python", False),
    ("SarvamBatchTranscriber", "CLI for Sarvam's batch speech-to-text API", "cli", False),
    ("ForgeBoard", "project / task management backend", "java", False),
    ("karpathy-zero-to-hero", "one neuron up to a GPT, every step typed out", "notebooks", False),
]


def work():
    W = 860
    H = 14 + 58 * len(WORK)
    css = """.row { animation: slide .6s cubic-bezier(.2,.8,.2,1) both; }
@keyframes slide { from { opacity: 0; transform: translateX(-18px); } to { opacity: 1; transform: none; } }
.shine { animation: shine 3.6s ease-in-out infinite; }
@keyframes shine { 0% { transform: translateX(-34px) skewX(-20deg); } 28%, 100% { transform: translateX(34px) skewX(-20deg); } }
.ping { transform-box: fill-box; transform-origin: center; animation: ping 2.4s cubic-bezier(0,0,.2,1) 1s infinite; }
@keyframes ping { 0% { opacity: .8; transform: scale(1); } 75%, 100% { opacity: 0; transform: scale(2); } }
.glow { animation: glow 2.4s ease-in-out 1s infinite; }
@keyframes glow { 0%, 100% { stroke-opacity: .35; } 50% { stroke-opacity: 1; } }"""
    defs, rows = [], []
    for i, (title, line, pill, star) in enumerate(WORK):
        cy = 43 + 58 * i
        col = GOLD if star else MUTED
        if star:
            defs.append(f'<clipPath id="m{i}"><circle cx="46" cy="{cy}" r="15"/></clipPath>'
                        f'<radialGradient id="g{i}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".55"/>'
                        f'<stop offset=".45" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD}" stop-opacity=".7"/></radialGradient>')
            mark = (f'<circle class="ping rm-hide" cx="46" cy="{cy}" r="15" fill="none" stroke="{GOLD}" stroke-width="1.5"/>'
                    f'<circle cx="46" cy="{cy}" r="15" fill="url(#g{i})"/><g clip-path="url(#m{i})"><rect class="shine rm-hide" x="41" y="{cy - 20}" width="9" height="40" fill="#fff" fill-opacity=".55" style="animation-delay:1.2s"/></g>'
                    f'<text x="46" y="{cy + 5}" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="800" fill="#1a1205">2</text>')
        else:
            mark = (f'<circle cx="46" cy="{cy}" r="13" fill="none" stroke="{MUTED}" stroke-opacity=".6" stroke-width="1.5"/>'
                    f'<circle cx="46" cy="{cy}" r="3.5" fill="{MUTED}" fill-opacity=".7"/>')
        tw = round(len(pill) * 7.8, 1)
        pw = tw + 26
        px = 832 - pw
        rows.append(
            f'<g class="row" style="animation-delay:{.15 + .12 * i:.2f}s">{mark}\n'
            f'  <text x="84" y="{cy - 3}" font-family="{SANS}" font-size="16" font-weight="600" fill="{FG}">{esc(title)}</text>\n'
            f'  <text x="84" y="{cy + 16}" font-family="{SANS}" font-size="13" fill="{MUTED}">{esc(line)}</text>\n'
            f'  <rect{" class=\"glow\"" if star else ""} x="{px:.1f}" y="{cy - 14}" width="{pw:.1f}" height="28" rx="14" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".45"/>'
            f'<text x="{px + 13:.1f}" y="{cy + 4.5}" font-family="{MONO}" font-size="13" fill="{col}" textLength="{tw}" lengthAdjust="spacing">{esc(pill)}</text></g>'
            + (f'<path d="M84 {cy + 29}H832" stroke="{EDGE}"/>' if i < len(WORK) - 1 else ""))
    alt = "Work: " + "; ".join(f"{t}: {l} ({p})" for t, l, p, _ in WORK)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}">
<style>
{css}
{REDUCED}
</style>
<defs>{"".join(defs)}</defs><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{EDGE}"/>{chr(10).join(rows)}
</svg>
'''


# --------------------------------------------------------------------- readme

def write(stem, svg):
    h = hashlib.sha1(svg.encode()).hexdigest()[:8]
    name = f"{stem}.{h}.svg"
    (ASSETS / name).write_text(svg, encoding="utf-8")
    return f"assets/{name}"


def main():
    ASSETS.mkdir(exist_ok=True)
    for old in ASSETS.glob("*.svg"):
        old.unlink()
    a = {
        "header": write("header", header()),
        "terminal": write("terminal", terminal()),
        "div_stack": write("divider-stack", divider("STACK")),
        "stack": write("stack", stack()),
        "div_work": write("divider-work", divider("WORK")),
        "work": write("work", work()),
    }
    user = "vhmaadhav"
    links = " &nbsp;·&nbsp; ".join(f'<a href="https://github.com/{user}/{t}">{t}</a>'
                                   for t, *_ in WORK if t != "neka-rt")
    readme = f'''<p align="center">
  <img src="{a["header"]}" width="100%" alt="Maadhav. Making models smaller without making them wrong. ECE by training, ML and systems by habit.">
</p>

<p align="center">
  <img src="{a["terminal"]}" width="100%" alt="whoami: ece student who kept ending up in the inference code. now: a local inference runtime, int8 calibration, SEM patch matching. last commit: int8 was fine, the calibration set was 12 images.">
</p>

<p align="center">
  <img src="{a["div_stack"]}" width="100%" alt="">
  <img src="{a["stack"]}" width="100%" alt="Stack: {", ".join(n for row in STACK for n, _ in row)}">
</p>

<p align="center">
  <img src="{a["div_work"]}" width="100%" alt="">
  <img src="{a["work"]}" width="100%" alt="Work: semicon-driftsense (1st runner-up, Applied Materials track, SEMICON India 2026), neka-rt, quantization-lab, hiver-email-suggested-response, SarvamBatchTranscriber, ForgeBoard, karpathy-zero-to-hero.">
</p>

<p align="center"><sub>{links}</sub></p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/{user}/{user}/output/github-snake-dark.svg">
    <img src="https://raw.githubusercontent.com/{user}/{user}/output/github-snake.svg" width="100%" alt="contribution graph being eaten by a snake">
  </picture>
</p>

<p align="center"><sub>
  <a href="https://orcid.org/0009-0002-9269-7337">orcid</a> &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/in/vhmaadhav">linkedin</a> &nbsp;·&nbsp;
  <a href="https://x.com/maadh3v">x</a> &nbsp;·&nbsp;
  <a href="mailto:sid.maadhav@gmail.com">email</a>
</sub></p>
'''
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
