# Lab 16 — Provenance Gate

## Decision rule

The decision date is **31 March 2026**. An observation is eligible only when its
publication date is on or before that date. The month measured is the period the
index describes; it is not evidence that the value was available in that month.

`asof.py` applies the supplied rules in this order:

1. Quarantine rows without a ticker.
2. Remove exact duplicates.
3. Remove rows published after the decision date.
4. For each ticker/month, retain the latest publication that was available by the
   decision date; the earlier value remains visible in the funnel as a revision.

Run it from this folder:

```sh
python asof.py
```

## Verified known answer

| Funnel step | Removed rows |
| --- | --- |
| Quarantined: no ticker | 11 |
| Exact duplicate | 7 |
| Published after 31 March | 3, 8, 10 |
| Older vintage replaced by a revision | 2 |
| As-of panel | 1, 4, 5, 6, 9, 12 |

| Ticker | As-of signal | Naive signal |
| --- | ---: | ---: |
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

The AAA as-of result uses row 4 (103.0), not row 2 (104.0), because row 4 is the
latest February publication available on 31 March. The naive result uses March
109.0, but that number was not published until 10 April.

## Point-in-time reflection

Look-ahead bias occurs when a historical test includes information that was not
available at the historical decision time. Here, event time is the month measured,
publication time is when the market could have seen the value, and a revision is a
newer publication for an already measured month. AAA's naive +5.83% signal looks
better because it includes March's 109.0 even though it was published after the
31 March decision. A backtest based on the naive column would overstate what a
trader could have known and could choose a strategy on unavailable information.

The most consequential rule is the publication-date cutoff: it excludes AAA's
unavailable March value. The revision rule also matters because retaining row 2
instead of row 4 would incorrectly report AAA's as-of change as +2.97%.

## Thursday prework — ALFRED series table

Lab 15's current Project 2 universe is QQQ, SPY, NVDA, and VOO. The provided
price file is sourced from Yahoo Finance and does not contain vintage/release
dates, so it cannot itself establish what was known on an earlier decision date.
For the ALFRED exercise, select a monthly series that has a documented connection
to the portfolio decision (for example, CPI as an inflation/objective context
input). Do not represent it as a security return or as a replacement for the
Project 2 price data.

Before Thursday:

1. Read the assigned ALFRED Help headings: *What is ALFRED?*, *What is a Release
   and what are Release Dates?*, *How are Release Dates determined?*, and *How
   does ALFRED verify vintage data?*
2. Choose and record one monthly ALFRED series ID, its release/source, units, and
   why it is relevant to the decision.
3. Export/download the series vintage observations from ALFRED and enter them in
   `alfred_series_table.csv`. Preserve the raw download separately if course
   instructions permit it; do not overwrite its dates with today’s date.
4. Complete the table's `published_on` field from the release/vintage metadata.
   If the date is unavailable, write `UNKNOWN` and quarantine that row rather
   than guessing.
5. State an intended historical decision date before filtering, then bring this
   file, the raw source link/download, this Lab 16 filter, and the Lab 15
   universe to class.

The table intentionally starts empty: entering real ALFRED observations requires
the specific series and vintage evidence you select and download.

## Brightspace checkout draft

Use your own attendance/session details and partner contribution. The evidence to
report is: the 31 March 2026 cutoff; funnel rows 11, 7, 3/8/10, and 2; the retained
panel; the as-of versus naive signal gap; the rule that revisions replace older
available vintages; and the limitation that the training table is fictional.

Growth note: I can now separate the month an observation describes from the day
it became usable, preserve excluded rows in a funnel, and reproduce a decision
set as of a cutoff. I still need practice obtaining and documenting real vintage
release metadata before using a public series in a historical portfolio test.
