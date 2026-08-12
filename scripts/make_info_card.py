"""Generate Ouassim's animated neofetch-style information card."""

from pathlib import Path
import os


WIDTH = 490
HEIGHT = 460


def main() -> None:
    static = os.getenv("STATIC") == "1"
    lines = [
        ("name", "Ouassim Tijani", "#58a6ff"),
        ("role", "Graphic Designer + Digital Marketer", "#f778ba"),
        ("focus", "Brand identities / campaign creative", "#d2a8ff"),
        ("craft", "Digital experiences / presentation design", "#ffa657"),
        ("stack", "React / Vite / Tailwind / Three.js", "#7ee787"),
        ("motion", "GSAP / Framer Motion / Lenis", "#79c0ff"),
        ("building", "Portfolio + event experiences", "#e3b341"),
        ("status", "Open to ambitious creative work", "#56d364"),
    ]

    style = "" if static else """
      .line { opacity: 0; transform: translateY(7px); animation: enter .42s cubic-bezier(.2,.8,.2,1) forwards; }
      @keyframes enter { to { opacity: 1; transform: translateY(0); } }
    """
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Ouassim Tijani profile information</title>',
        '<desc id="desc">A terminal-style card describing Ouassim as a graphic designer and digital marketer.</desc>',
        f'<style>{style}</style>',
        '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',
        '<rect x=".5" y=".5" width="489" height="459" rx="11.5" fill="none" stroke="#30363d"/>',
        '<circle cx="18" cy="18" r="4" fill="#ff5f56"/><circle cx="31" cy="18" r="4" fill="#ffbd2e"/><circle cx="44" cy="18" r="4" fill="#27c93f"/>',
        '<text x="245" y="22" text-anchor="middle" fill="#7d8590" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="10">ouassim@github:~</text>',
        '<g font-family="ui-monospace, SFMono-Regular, Consolas, monospace">',
        '<g class="line" style="animation-delay:.15s"><text x="26" y="65" fill="#39d353" font-size="14">$ neofetch --creative</text></g>',
        '<g class="line" style="animation-delay:.28s"><text x="26" y="94" fill="#58a6ff" font-size="18" font-weight="700">ouassim20</text><text x="116" y="94" fill="#8b949e" font-size="18">@github</text></g>',
        '<g class="line" style="animation-delay:.4s"><rect x="26" y="106" width="438" height="1" fill="#30363d"/></g>',
    ]

    for index, (key, value, color) in enumerate(lines):
        y = 140 + index * 35
        delay = .52 + index * .11
        out.append(
            f'<g class="line" style="animation-delay:{delay:.2f}s">'
            f'<text x="26" y="{y}" fill="{color}" font-size="13" font-weight="700">{key:>8}</text>'
            f'<text x="104" y="{y}" fill="#c9d1d9" font-size="13">{value}</text></g>'
        )

    swatches = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#58a6ff", "#d2a8ff", "#f778ba"]
    out.append('<g class="line" style="animation-delay:1.52s">')
    for index, color in enumerate(swatches):
        out.append(f'<rect x="{104 + index * 22}" y="424" width="16" height="16" rx="3" fill="{color}"/>')
    out.append('<text x="26" y="437" fill="#8b949e" font-size="12">palette</text></g></g></svg>')

    Path("info-card.svg").write_text("".join(out), encoding="utf-8")
    print("wrote info-card.svg")


if __name__ == "__main__":
    main()

