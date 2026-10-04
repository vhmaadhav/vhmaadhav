"""Builds the profile SVGs in assets/ and rewrites README.md to point at them.

Every card is rendered twice (light and dark) and served through <picture>, so
it matches whichever GitHub theme the viewer uses. Filenames carry a short
content hash so GitHub's image proxy can't serve a stale copy after an edit.
Run from the repo root:  python scripts/build.py
"""
import hashlib
import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
USER = "vhmaadhav"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

# GitHub's own surface colours, so the cards sit flush with the page
THEMES = {
    "light": dict(bg="#ffffff", edge="#d0d7de", fg="#1f2328", muted="#59636e", faint="#afb8c1",
                  accent="#8250df", gold="#9a6700", gold_bg="#fff8c5", green="#1a7f37"),
    "dark": dict(bg="#0d1117", edge="#30363d", fg="#e6edf3", muted="#9198a1", faint="#3d444d",
                 accent="#a78bfa", gold="#d29922", gold_bg="#2e2410", green="#3fb950"),
}

LANG = {"Python": "#3572A5", "Jupyter": "#DA5B0B", "Java": "#b07219"}

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def esc(s):
    return html.escape(s, quote=True)


def svg(w, h, label, body, css=""):
    style = f"<style>\n{css}\n{REDUCED}\n</style>\n" if css else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(label)}">\n{style}{body}\n</svg>\n')


# --------------------------------------------------------------------- header

TAGLINE = "Making models smaller without making them wrong."
META = "ECE · ML systems · quantization · SEM imagery"


def header(c):
    W, H = 860, 200

    # motif: a smooth fp32 signal and its 4-bit sample-and-hold reconstruction
    x0, x1, yc, amp = 560, 820, 100, 52

    def f(t):
        return .62 * math.sin(2 * math.pi * 1.15 * t + .3) + .32 * math.sin(2 * math.pi * 2.9 * t + 1.1)

    smooth = " ".join(f"{'M' if i == 0 else 'L'}{x0 + i:.0f} {yc - amp * f(i / (x1 - x0)):.1f}"
                      for i in range(x1 - x0 + 1))
    steps, levels = 20, 7
    dx = (x1 - x0) / steps
    q = lambda v: round(v * levels) / levels
    ys = [yc - amp * q(f((k + .5) / steps)) for k in range(steps)]
    stair = f"M{x0} {ys[0]:.1f}" + "".join(
        f"H{x0 + (k + 1) * dx:.1f}" + (f"V{ys[k + 1]:.1f}" if k + 1 < steps else "") for k in range(steps))
    pts = [(x0 + i, yc - amp * f(i / (x1 - x0))) for i in range(x1 - x0 + 1)]
    wave_len = round(sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) + 1, 1)
    stair_len = round((x1 - x0) + sum(abs(ys[k + 1] - ys[k]) for k in range(steps - 1)), 1)

    css = f""".in {{ animation: in .7s cubic-bezier(.2,.8,.2,1) both; }}
.bar {{ transform-box: fill-box; transform-origin: left center; animation: grow .6s cubic-bezier(.2,.8,.2,1) .5s both; }}
.wave {{ stroke-dasharray: {wave_len} {wave_len}; animation: wave 1.6s ease-out .3s both; }}
.stair {{ stroke-dasharray: {stair_len} {stair_len}; animation: stair 2s cubic-bezier(.6,0,.3,1) 1.1s both; }}
@keyframes in {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
@keyframes wave {{ from {{ stroke-dashoffset: {wave_len}; }} to {{ stroke-dashoffset: 0; }} }}
@keyframes stair {{ from {{ stroke-dashoffset: {stair_len}; }} to {{ stroke-dashoffset: 0; }} }}"""

    grid = "".join(f'<path d="M{x0} {yc + d}H{x1}" stroke="{c["faint"]}" stroke-opacity="{.9 if d == 0 else .45}" '
                   f'stroke-dasharray="{"none" if d == 0 else "2 4"}"/>' for d in (-amp, 0, amp))
    body = f'''<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["bg"]}" stroke="{c["edge"]}"/>
<g class="in"><text x="40" y="96" font-family="{SANS}" font-size="52" font-weight="700" letter-spacing="-1.2" fill="{c["fg"]}">Maadhav</text></g>
<rect class="bar" x="42" y="114" width="48" height="3" rx="1.5" fill="{c["accent"]}"/>
<g class="in" style="animation-delay:.25s"><text x="40" y="148" font-family="{SANS}" font-size="18" fill="{c["fg"]}">{esc(TAGLINE)}</text></g>
<g class="in" style="animation-delay:.4s"><text x="40" y="172" font-family="{MONO}" font-size="12.5" fill="{c["muted"]}">{esc(META)}</text></g>
{grid}
<path class="wave" d="{smooth}" fill="none" stroke="{c["muted"]}" stroke-opacity=".55" stroke-width="1.4"/>
<path class="stair" d="{stair}" fill="none" stroke="{c["accent"]}" stroke-width="2" stroke-linejoin="round"/>
<text x="{x1}" y="{yc - amp - 14}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{c["muted"]}">fp32 <tspan fill="{c["accent"]}">→ int4</tspan></text>'''
    return svg(W, H, f"Maadhav. {TAGLINE} {META}.", body, css)


# ---------------------------------------------------------------------- cards

# (repo, language, badge, two description lines)
WORK = [
    ("semicon-driftsense", "Python", "runner-up · SEMICON India '26",
     ["Finds a 1 µm reference patch in a ~10 µm SEM frame",
      "under unknown zoom, rotation and possible absence."]),
    ("razorpay-agentic-firewall", "Python", None,
     ["Checks that AI shopping agents spend only what",
      "the user authorized. Deterministic, no LLM in the loop."]),
    ("thodar", "Python", "Health-a-thon '26",
     ["Mother–baby follow-up desk for care teams: due",
      "dates, morning worklists, two-way reminders."]),
    ("quantization-lab", "Python", None,
     ["Post-training quantization, worked out by hand",
      "before trusting a library to do it."]),
    ("hiver-email-suggested-response", "Python", None,
     ["Retrieval-grounded email reply drafts, plus an",
      "eval harness that scores them two ways."]),
    ("karpathy-zero-to-hero", "Jupyter", None,
     ["From one neuron up to a GPT, following",
      "Zero to Hero with every step typed out."]),
]


def card(c, repo, lang, badge, lines):
    W, H = 420, 132
    badge_svg = ""
    if badge:
        bw = round(len(badge) * 11 * .6 + 18, 1)
        badge_svg = (f'<rect x="{W - 20 - bw:.1f}" y="18" width="{bw}" height="22" rx="11" fill="{c["gold_bg"]}" '
                     f'stroke="{c["gold"]}" stroke-opacity=".5"/>'
                     f'<text x="{W - 20 - bw / 2:.1f}" y="33" text-anchor="middle" font-family="{MONO}" font-size="11" '
                     f'fill="{c["gold"]}">{esc(badge)}</text>')
    desc = "".join(f'<text x="22" y="{66 + 20 * i}" font-family="{SANS}" font-size="13.5" fill="{c["muted"]}">{esc(l)}</text>'
                   for i, l in enumerate(lines))
    body = f'''<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{c["bg"]}" stroke="{c["edge"]}"/>
<text x="22" y="35" font-family="{SANS}" font-size="15.5" font-weight="600" fill="{c["accent"]}">{esc(repo)}</text>
{badge_svg}
{desc}
<circle cx="27" cy="{H - 22}" r="5" fill="{LANG[lang]}"/>
<text x="38" y="{H - 18}" font-family="{SANS}" font-size="12" fill="{c["muted"]}">{lang}</text>'''
    return svg(W, H, f"{repo}: {' '.join(lines)}", body)


# ---------------------------------------------------------------------- stack

STACK = [
    ("languages", ["Python · C · Java", "TypeScript · Bash"]),
    ("ml", ["PyTorch · NumPy · OpenCV", "Hugging Face · int8 / PTQ"]),
    ("tools", ["Docker · Linux · Git", "Jupyter · GDSII · SEM data"]),
]


def stack(c):
    W, H = 860, 112
    cols = []
    for i, (head, lines) in enumerate(STACK):
        x = 40 + 280 * i
        cols.append(f'<text x="{x}" y="38" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{c["muted"]}">{head.upper()}</text>'
                    + "".join(f'<text x="{x}" y="{66 + 22 * j}" font-family="{SANS}" font-size="14.5" fill="{c["fg"]}">{esc(l)}</text>'
                              for j, l in enumerate(lines)))
    seps = "".join(f'<path d="M{20 + 280 * i} 26V{H - 26}" stroke="{c["edge"]}"/>' for i in (1, 2))
    body = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["bg"]}" stroke="{c["edge"]}"/>\n'
            + seps + "\n" + "\n".join(cols))
    alt = "Stack. " + ". ".join(f"{h}: {' · '.join(l)}" for h, l in STACK)
    return svg(W, H, alt, body)


# --------------------------------------------------------------------- readme

def write(stem, make):
    out = {}
    for theme, c in THEMES.items():
        s = make(c)
        name = f"{stem}-{theme}.{hashlib.sha1(s.encode()).hexdigest()[:8]}.svg"
        (ASSETS / name).write_text(s, encoding="utf-8")
        out[theme] = f"assets/{name}"
    return out


def picture(src, alt, width):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{src["dark"]}">'
            f'<img src="{src["light"]}" width="{width}" alt="{esc(alt)}"></picture>')


def main():
    ASSETS.mkdir(exist_ok=True)
    for old in ASSETS.glob("*.svg"):
        old.unlink()

    head = write("header", header)
    cards = []
    for repo, lang, badge, lines in WORK:
        src = write(f"card-{repo}", lambda c: card(c, repo, lang, badge, lines))
        cards.append(f'<a href="https://github.com/{USER}/{repo}">{picture(src, f"{repo}: {" ".join(lines)}", "49%")}</a>')
    grid = "\n".join(" ".join(cards[i:i + 2]) for i in range(0, len(cards), 2))
    tools = write("stack", stack)

    readme = f'''{picture(head, f"Maadhav. {TAGLINE}", "100%")}

ECE student who kept ending up in the inference code. Right now I'm building **neka-rt**, a local-first inference runtime (private for now), and calibrating int8 models in [quantization-lab](https://github.com/{USER}/quantization-lab).

### Selected work

<p>
{grid}
</p>

### Stack

{picture(tools, "Stack: " + "; ".join(f"{h}: {', '.join(l)}" for h, l in STACK), "100%")}

<sub><a href="mailto:sid.maadhav@gmail.com">email</a> &nbsp;·&nbsp; <a href="https://www.linkedin.com/in/{USER}">linkedin</a> &nbsp;·&nbsp; <a href="https://x.com/maadh3v">x</a> &nbsp;·&nbsp; <a href="https://orcid.org/0009-0002-9269-7337">orcid</a></sub>
'''
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
