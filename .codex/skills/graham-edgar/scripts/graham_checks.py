"""Deterministic Graham checks for the Lab 19 shared EDGAR panel."""

from __future__ import annotations


def current_ratio_check(rows: list[dict], threshold: float = 2.0) -> str:
    ratio = rows[-1].get("current_ratio") if rows else None
    if ratio is None:
        return "not known"
    return "pass" if ratio >= threshold else "fail"


def check_results(rows: list[dict], current_ratio_threshold: float = 2.0) -> dict[str, str]:
    income = [row.get("net_income") for row in rows]
    return {
        f"Current ratio of {current_ratio_threshold:.1f} or more, latest year": current_ratio_check(rows, current_ratio_threshold),
        "Net income positive every year": "not known" if any(value is None for value in income) else ("pass" if all(value > 0 for value in income) else "fail"),
        "Net income grew, first year to last": "not known" if len(income) < 2 or income[0] is None or income[-1] is None else ("pass" if income[-1] > income[0] else "fail"),
    }
