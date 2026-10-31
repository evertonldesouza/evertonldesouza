#!/usr/bin/env python3
"""Update the UPPER tenure displayed in the profile's terminal SVG."""
import argparse
from datetime import date, datetime
from pathlib import Path
import re
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "terminal_everton.svg"
# Month and year from the LinkedIn experience supplied by Everton.
START_YEAR, START_MONTH = 2021, 8
PATTERN = re.compile(r"(\[ UPPER / BIPPER \]  )[^\n<]+")


def tenure(today: date) -> str:
    months = (today.year - START_YEAR) * 12 + today.month - START_MONTH
    if months < 0:
        raise ValueError("The current date precedes the start month")
    years, remaining = divmod(months, 12)
    parts = []
    if years:
        parts.append(f"{years} {'ano' if years == 1 else 'anos'}")
    if remaining or not parts:
        parts.append(f"{remaining} {'mês' if remaining == 1 else 'meses'}")
    return " ".join(parts)


def update(content: str, today: date) -> str:
    result, count = PATTERN.subn(lambda match: match.group(1) + tenure(today), content)
    if count != 1:
        raise ValueError(f"Expected exactly one UPPER tenure line, found {count}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=date.fromisoformat, help="Reference date (YYYY-MM-DD)")
    args = parser.parse_args()
    today = args.date or datetime.now(ZoneInfo("America/Sao_Paulo")).date()
    original = SVG.read_text(encoding="utf-8")
    updated = update(original, today)
    if original != updated:
        SVG.write_text(updated, encoding="utf-8")
        print(f"Updated tenure: {tenure(today)}")
    else:
        print(f"Already up to date: {tenure(today)}")


if __name__ == "__main__":
    main()
