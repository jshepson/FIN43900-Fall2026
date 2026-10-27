"""Lab 16: point-in-time filter for the fictional card-spend index.

Run with: python asof.py
Only TABLE and DECISION_DATE are intended to be edited for a new exercise.
"""

from __future__ import annotations

import csv
from datetime import date
from io import StringIO


DECISION_DATE = date.fromisoformat("2026-03-31")

TABLE = """row_number,ticker,month_measured,published_on,index
1,AAA,2026-01,2026-02-10,101.0
2,AAA,2026-02,2026-03-10,104.0
3,AAA,2026-03,2026-04-10,109.0
4,AAA,2026-02,2026-03-25,103.0
5,BBB,2026-01,2026-02-10,98.0
6,BBB,2026-02,2026-03-10,97.0
7,BBB,2026-02,2026-03-10,97.0
8,BBB,2026-03,2026-04-10,92.0
9,CCC,2026-01,2026-02-10,110.0
10,CCC,2026-02,2026-04-05,112.0
11,,2026-02,2026-03-10,99.0
12,CCC,2026-02,2026-03-10,111.0
"""


def read_table(table: str) -> list[dict[str, object]]:
    """Parse the editable CSV input into consistently typed rows."""
    rows = []
    for raw in csv.DictReader(StringIO(table.strip())):
        rows.append(
            {
                "row_number": int(raw["row_number"]),
                "ticker": raw["ticker"].strip(),
                "month_measured": raw["month_measured"],
                "published_on": date.fromisoformat(raw["published_on"]),
                "index": float(raw["index"]),
            }
        )
    return rows


def row_numbers(rows: list[dict[str, object]]) -> str:
    return ", ".join(str(row["row_number"]) for row in rows) or "none"


def remove_exact_duplicates(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Keep the first occurrence; report later rows identical in all data fields."""
    seen = set()
    kept, removed = [], []
    for row in rows:
        signature = (row["ticker"], row["month_measured"], row["published_on"], row["index"])
        if signature in seen:
            removed.append(row)
        else:
            seen.add(signature)
            kept.append(row)
    return kept, removed


def keep_latest_publication(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """For each ticker/month, retain its latest publication and preserve the old vintage."""
    latest_by_month: dict[tuple[object, object], dict[str, object]] = {}
    for row in rows:
        key = (row["ticker"], row["month_measured"])
        current = latest_by_month.get(key)
        if current is None or (row["published_on"], row["row_number"]) > (
            current["published_on"], current["row_number"]
        ):
            latest_by_month[key] = row
    kept = [row for row in rows if latest_by_month[(row["ticker"], row["month_measured"])] is row]
    removed = [row for row in rows if row not in kept]
    return kept, removed


def point_in_time_panel(rows: list[dict[str, object]], cutoff: date) -> tuple[list[dict[str, object]], list[tuple[str, list[dict[str, object]]]]]:
    """Apply the Lab 16 rules in their required order and retain each removal record."""
    no_ticker = [row for row in rows if not row["ticker"]]
    remaining = [row for row in rows if row["ticker"]]

    remaining, duplicates = remove_exact_duplicates(remaining)

    late = [row for row in remaining if row["published_on"] > cutoff]
    remaining = [row for row in remaining if row["published_on"] <= cutoff]

    remaining, older_vintages = keep_latest_publication(remaining)
    panel = sorted(remaining, key=lambda row: (row["ticker"], row["month_measured"], row["row_number"]))
    funnel = [
        ("Quarantined: no ticker", no_ticker),
        ("Exact duplicate", duplicates),
        (f"Published after {cutoff:%d %B}", late),
        ("Older vintage replaced by a revision", older_vintages),
    ]
    return panel, funnel


def naive_panel(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Use all publication dates, while still applying identity and duplicate rules."""
    identified = [row for row in rows if row["ticker"]]
    deduplicated, _ = remove_exact_duplicates(identified)
    panel, _ = keep_latest_publication(deduplicated)
    return sorted(panel, key=lambda row: (row["ticker"], row["month_measured"], row["row_number"]))


def signals(panel: list[dict[str, object]]) -> list[tuple[str, str, float]]:
    """Return each ticker's change from its prior available month to its latest month."""
    by_ticker: dict[str, list[dict[str, object]]] = {}
    for row in panel:
        by_ticker.setdefault(str(row["ticker"]), []).append(row)

    results = []
    for ticker, ticker_rows in sorted(by_ticker.items()):
        ticker_rows.sort(key=lambda row: str(row["month_measured"]))
        if len(ticker_rows) < 2:
            continue
        previous, latest = ticker_rows[-2:]
        change = (float(latest["index"]) / float(previous["index"]) - 1) * 100
        results.append((ticker, str(latest["month_measured"]), change))
    return results


def print_panel(title: str, panel: list[dict[str, object]]) -> None:
    print(f"\n{title}")
    print("row  ticker  month measured  published on  index")
    for row in panel:
        print(
            f"{row['row_number']:>3}  {row['ticker']:<6}  {row['month_measured']:<14}  "
            f"{row['published_on'].isoformat()}    {row['index']:>5.1f}"
        )


def print_signals(title: str, panel: list[dict[str, object]]) -> None:
    print(f"\n{title}")
    for ticker, month, change in signals(panel):
        month_name = date.fromisoformat(f"{month}-01").strftime("%B %Y")
        print(f"{ticker}: {change:+.2f}% ({month_name})")


def main() -> None:
    rows = read_table(TABLE)
    asof_panel, funnel = point_in_time_panel(rows, DECISION_DATE)

    print(f"Decision date: {DECISION_DATE.isoformat()}")
    print("\nRow funnel")
    for step, removed in funnel:
        print(f"{step}: {len(removed)} removed (rows {row_numbers(removed)})")
    print(f"As-of panel: {len(asof_panel)} rows (rows {row_numbers(asof_panel)})")

    print_panel("As-of panel", asof_panel)
    print_signals("As-of signals", asof_panel)
    print_signals("Naive signals (all publication dates)", naive_panel(rows))


if __name__ == "__main__":
    main()
