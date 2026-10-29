# Lab 17 — Point-in-Time Audit

## App and known-answer check

Run from this folder:

```sh
../../.venv/bin/streamlit run asof_app.py
```

`asof_app.py` makes one cached FRED download and one cached ALFRED vintage
download per selected series. It treats `.` as missing, keeps an invalid typed
series from stopping the remaining series, and compares only overlapping dates
when counting revisions.

With **As known on = 5 October 2026**, the app reproduced:

| Series | Last date known | Value |
| --- | --- | ---: |
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | 2 October 2026 | 5.28 |
| MORTGAGE30US | 1 October 2026 | 7.28 |

With **PAYEMS** and **As known on = 15 January 2025**, the app reports December
2024 at **159,536**. Its current FRED value is lower and the same-date revised
count is above zero; this confirms the app uses ALFRED for the historical view,
not today's file twice.

## CPIAUCSL data card

| Field | Evidence |
| --- | --- |
| Source and link | Federal Reserve Bank of St. Louis, [FRED CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL); historical vintages from [ALFRED](https://alfred.stlouisfed.org/series?seid=CPIAUCSL). |
| What it measures | Consumer Price Index for All Urban Consumers: All Items in U.S. City Average; monthly, seasonally adjusted. |
| Units | Index, 1982–1984 = 100. |
| Publication lag | Monthly value is released after the month it measures; the app's “as known on” cutoff excludes values not yet present in ALFRED. |
| Revisions | Yes. ALFRED preserves vintage values, and the app counts differences between the selected vintage and today's FRED values on identical dates. |
| Download date | 29 October 2026. |
| Three source checks | Read from the FRED page/download on 29 October 2026: July 2026 = 332.813; August 2026 = 334.131; September 2026 = 336.298. |

## Fresh-eyes attack and call

**Attack — publication date:** A monthly observation date is not its release
date. Evidence: setting the app's cutoff earlier can make the newest measured
month disappear, even though that month is present in FRED today.

**Response:** The series must be selected from the ALFRED vintage at each
decision date, not from today's FRED CSV with a guessed lag. The app makes that
cutoff explicit and reports the newest value actually available.

**Call — quarantine for direct Project 2 return estimation.** CPIAUCSL is a
macroeconomic index rather than a tradable adjusted-close series, is released
after its observation month, and can be revised. It may be used only as a
clearly labelled contextual inflation input from an ALFRED as-of vintage; admit
it to a historical model only after the decision timestamp and vintage rule are
specified in advance.

## Brightspace checkout

| Checkout field | Entry |
| --- | --- |
| Lab date | 29 October 2026 |
| My contribution | I ran the app, checked the four required historical values and the PAYEMS revision probe, and explained how the ALFRED vintage-date download prevents look-ahead bias. I reviewed the CPIAUCSL data card and supported the decision to quarantine it for direct return estimation. |
| Frozen leakage prediction | A series observed in a month may still be unavailable on a decision date because its release occurs later; a current FRED download can also contain later revisions. |
| As-of and revision rule | Use ALFRED with the decision date as `vintage_date`; compare only overlapping, non-missing observation dates; do not use today's revised FRED values for a historical decision. |
| Known-answer / changed-time evidence | On 5 October 2026: BAA 6.47, FEDFUNDS 3.75, DGS10 5.28, MORTGAGE30US 7.28. PAYEMS on 15 January 2025: December 2024 = 159,536; today's value is lower and revisions are nonzero. |
| Data-card decision | Quarantine CPIAUCSL for direct Project 2 return estimation; it may be contextual only when selected from an ALFRED as-of vintage. |
| Condition that reverses the call | A research use may proceed only with a decision timestamp and ALFRED vintage rule set before results are inspected. |
| Artifact links | `asof_app.py` and this file in the Lab 17 GitHub folder. |
