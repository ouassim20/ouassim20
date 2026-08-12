"""Convert a prepared portrait into a self-typing monochrome SVG."""

from html import escape
from pathlib import Path
import sys

from PIL import Image, ImageEnhance, ImageOps


RAMP = "@%#*+=-:. "
WIDTH = 370
HEIGHT = 460
COLS = 57
ROWS = 52


def main() -> None:
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png")
    output = Path(sys.argv[2] if len(sys.argv) > 2 else "ouassim-ascii.svg")

    image = Image.open(source).convert("L")
    image = ImageOps.autocontrast(image, cutoff=1)
    image = ImageEnhance.Contrast(image).enhance(1.18)
    image = image.resize((COLS, ROWS), Image.Resampling.LANCZOS)

    rows = []
    for y in range(ROWS):
        line = "".join(RAMP[min(len(RAMP) - 1, image.getpixel((x, y)) * len(RAMP) // 256)] for x in range(COLS))
        rows.append(line.rstrip())

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Animated ASCII portrait of Ouassim Tijani</title>',
        '<desc id="desc">A monochrome portrait types itself from top to bottom.</desc>',
        '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',
        '<rect x=".5" y=".5" width="369" height="459" rx="11.5" fill="none" stroke="#30363d"/>',
        '<circle cx="18" cy="18" r="4" fill="#ff5f56"/><circle cx="31" cy="18" r="4" fill="#ffbd2e"/><circle cx="44" cy="18" r="4" fill="#27c93f"/>',
        '<text x="185" y="22" text-anchor="middle" fill="#7d8590" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="10">portrait.sh</text>',
        '<defs>',
    ]

    for index in range(ROWS):
        parts.append(
            f'<clipPath id="row-{index}"><rect x="12" y="{32 + index * 8.05:.2f}" width="0" height="9">'
            f'<animate attributeName="width" from="0" to="346" dur=".48s" begin="{index * .055:.3f}s" fill="freeze"/>'
            '</rect></clipPath>'
        )
    parts.append('</defs><g fill="#c9d1d9" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="7.2" xml:space="preserve">')

    for index, line in enumerate(rows):
        y = 40 + index * 8.05
        parts.append(f'<text x="13" y="{y:.2f}" clip-path="url(#row-{index})">{escape(line)}</text>')

    parts.append('</g>')
    total = ROWS * .055 + .5
    parts.append(
        f'<rect x="13" y="448" width="6" height="2" fill="#39d353" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;0;1" dur=".6s" begin="{total:.2f}s" repeatCount="indefinite"/>'
        '</rect></svg>'
    )
    output.write_text("".join(parts), encoding="utf-8")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()

