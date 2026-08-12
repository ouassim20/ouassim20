"""Render contribution JSON as an animated GitHub-style SVG heatmap."""

from datetime import date, timedelta
from html import escape
import json
from pathlib import Path


WIDTH = 860
HEIGHT = 250
CELL = 10
GAP = 3
GRID_X = 70
GRID_Y = 55
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def main() -> None:
    payload = json.loads(Path("data/contributions.json").read_text(encoding="utf-8"))
    days = payload["days"]
    stats = payload["stats"]
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Ouassim&#39;s GitHub contribution heatmap</title>',
        f'<desc id="desc">{stats["total"]:,} contributions in the last year, animated week by week.</desc>',
        '<style>@keyframes reveal{from{opacity:0;transform:translateY(-7px)}to{opacity:1;transform:translateY(0)}}.day{opacity:0;animation:reveal .35s cubic-bezier(.2,.8,.2,1) forwards}</style>',
        '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',
        '<rect x=".5" y=".5" width="859" height="249" rx="11.5" fill="none" stroke="#30363d"/>',
        '<circle cx="18" cy="18" r="4" fill="#ff5f56"/><circle cx="31" cy="18" r="4" fill="#ffbd2e"/><circle cx="44" cy="18" r="4" fill="#27c93f"/>',
        '<text x="430" y="22" text-anchor="middle" fill="#7d8590" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="10">contributions.sh</text>',
        '<g font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="10" fill="#8b949e">',
        f'<text x="{GRID_X - 34}" y="{GRID_Y + 23}">Mon</text><text x="{GRID_X - 34}" y="{GRID_Y + 49}">Wed</text><text x="{GRID_X - 34}" y="{GRID_Y + 75}">Fri</text>',
    ]

    seen_months: set[tuple[int, int]] = set()
    for day in days:
        current = date.fromisoformat(day["date"])
        week = (current - start).days // 7
        weekday = (current.weekday() + 1) % 7
        x = GRID_X + week * (CELL + GAP)
        y = GRID_Y + weekday * (CELL + GAP)
        month_key = (current.year, current.month)
        if current.day <= 7 and month_key not in seen_months:
            seen_months.add(month_key)
            out.append(f'<text x="{x}" y="45">{MONTHS[current.month - 1]}</text>')
        level = max(0, min(4, int(day["level"])))
        delay = .12 + week * .018 + weekday * .022
        label = f'{int(day["count"])} contributions on {day["date"]}'
        out.append(
            f'<rect class="day" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{PALETTE[level]}" style="animation-delay:{delay:.3f}s">'
            f'<title>{escape(label)}</title></rect>'
        )

    footer_y = 181
    out.extend([
        f'<text x="{GRID_X}" y="{footer_y}" fill="#c9d1d9" font-size="12">{stats["total"]:,} contributions</text>',
        f'<text x="{GRID_X + 190}" y="{footer_y}" fill="#c9d1d9" font-size="12">current streak <tspan fill="#39d353">{stats["current_streak"]}d</tspan></text>',
        f'<text x="{GRID_X + 380}" y="{footer_y}" fill="#c9d1d9" font-size="12">longest <tspan fill="#39d353">{stats["longest_streak"]}d</tspan></text>',
        f'<text x="{GRID_X + 540}" y="{footer_y}" fill="#c9d1d9" font-size="12">best day <tspan fill="#39d353">{stats["best_day"]["count"]}</tspan></text>',
        f'<text x="{GRID_X}" y="218" fill="#8b949e">Less</text>',
    ])
    for index, color in enumerate(PALETTE):
        out.append(f'<rect x="{GRID_X + 34 + index * 15}" y="208" width="10" height="10" rx="2" fill="{color}"/>')
    out.append(f'<text x="{GRID_X + 112}" y="218" fill="#8b949e">More</text>')
    out.append(f'<text x="790" y="218" text-anchor="end" fill="#484f58">@{escape(payload["username"])}</text></g></svg>')

    Path("contrib-heatmap.svg").write_text("".join(out), encoding="utf-8")
    print("wrote contrib-heatmap.svg")


if __name__ == "__main__":
    main()

