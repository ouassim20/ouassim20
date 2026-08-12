"""Fetch public GitHub contribution data without a token or dependency."""

from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import urllib.request


USERNAME = "ouassim20"


class ContributionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.days: dict[str, dict[str, object]] = {}
        self.tooltip_for: str | None = None
        self.tooltip_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = (values.get("class") or "").split()
        if tag == "td" and "ContributionCalendar-day" in classes and values.get("data-date"):
            element_id = values.get("id") or values["data-date"]
            self.days[element_id] = {
                "date": values["data-date"],
                "level": int(values.get("data-level") or 0),
                "count": 0,
            }
        elif tag == "tool-tip" and values.get("for"):
            self.tooltip_for = values["for"]
            self.tooltip_text = []

    def handle_data(self, data: str) -> None:
        if self.tooltip_for:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tool-tip" and self.tooltip_for:
            text = " ".join(self.tooltip_text)
            match = re.search(r"([\d,]+) contribution", text)
            if self.tooltip_for in self.days:
                self.days[self.tooltip_for]["count"] = int(match.group(1).replace(",", "")) if match else 0
            self.tooltip_for = None
            self.tooltip_text = []


def streaks(days: list[dict[str, object]]) -> tuple[int, int]:
    active = {date.fromisoformat(str(day["date"])) for day in days if int(day["count"]) > 0}
    longest = 0
    run = 0
    previous = None
    for current in sorted(active):
        run = run + 1 if previous and current == previous + timedelta(days=1) else 1
        longest = max(longest, run)
        previous = current

    current = 0
    cursor = date.today()
    if cursor not in active:
        cursor -= timedelta(days=1)
    while cursor in active:
        current += 1
        cursor -= timedelta(days=1)
    return current, longest


def main() -> None:
    if len(sys.argv) > 1:
        html = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        url = f"https://github.com/users/{USERNAME}/contributions"
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/html",
            },
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8")

    parser = ContributionParser()
    parser.feed(html)
    today = date.today()
    days = sorted((day for day in parser.days.values() if date.fromisoformat(str(day["date"])) <= today), key=lambda day: str(day["date"]))
    if not days:
        raise RuntimeError("GitHub returned no contribution days")

    current, longest = streaks(days)
    best = max(days, key=lambda day: int(day["count"]))
    monthly: dict[str, int] = defaultdict(int)
    for day in days:
        monthly[str(day["date"])[:7]] += int(day["count"])

    payload = {
        "username": USERNAME,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "days": days,
        "stats": {
            "total": sum(int(day["count"]) for day in days),
            "current_streak": current,
            "longest_streak": longest,
            "best_day": best,
            "monthly_totals": dict(sorted(monthly.items())),
        },
    }
    output = Path("data/contributions.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output} with {len(days)} days")


if __name__ == "__main__":
    main()
