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
For the ALFRED exercise, I selected **CPIAUCSL**: the seasonally adjusted,
monthly U.S. Consumer Price Index (1982–1984 = 100). It is an inflation/objective
context input, not a security return or a replacement for the Project 2 price
data. The series is published in ALFRED's Consumer Price Index release and
sourced from the U.S. Bureau of Labor Statistics.

Before Thursday:

1. Read the assigned ALFRED Help headings: *What is ALFRED?*, *What is a Release
   and what are Release Dates?*, *How are Release Dates determined?*, and *How
   does ALFRED verify vintage data?*
2. `alfred_series_table.csv` contains 52 monthly CPIAUCSL observations for the
   Lab 15 price-window period, retrieved from the ALFRED snapshot fixed at
   **31 March 2026**. The source URL is preserved on every row.
3. This is an as-of snapshot, so it proves what was in ALFRED by the cutoff but
   does **not** invent an original publication day for each observation. The
   source snapshot has a blank October 2025 value; row 48 is explicitly
   quarantined rather than filled or deleted.
4. For a row-level *publication-date* filter, download ALFRED's “Observations by
   Real-Time Period” export and retain its real-time-start and real-time-end
   fields. Do not substitute the snapshot date for an original release date.
5. Bring this table, its source URL, the Lab 16 filter, and the Lab 15 universe
   to class.

ALFRED states that a vintage date retrieves values actually available at that
historical date. Its release-date documentation also explains that a release date
is when the source first makes the data available; those are distinct concepts.

## Brightspace checkout draft

Use your own attendance/session details and partner contribution. The evidence to
report is: the 31 March 2026 cutoff; funnel rows 11, 7, 3/8/10, and 2; the retained
panel; the as-of versus naive signal gap; the rule that revisions replace older
available vintages; and the limitation that the training table is fictional.

Growth note: I can now separate the month an observation describes from the day
it became usable, preserve excluded rows in a funnel, and reproduce a decision
set as of a cutoff. I still need practice obtaining and documenting real vintage
release metadata before using a public series in a historical portfolio test.
