"""Deterministic Burry checks for the Lab 19 shared EDGAR panel."""

from __future__ import annotations


def check_results(rows: list[dict]) -> dict[str, str]:
    cash_vs_income = [(row.get("operating_cash_flow"), row.get("net_income")) for row in rows]
    latest = rows[-1] if rows else {}
    liabilities, equity = latest.get("liabilities"), latest.get("equity")
    cash_check = "not known" if any(cash is None or income is None for cash, income in cash_vs_income) else ("pass" if all(cash >= income for cash, income in cash_vs_income) else "fail")
    leverage_check = "not known" if liabilities is None or equity is None or equity <= 0 else ("pass" if liabilities <= 2 * equity else "fail")
    return {
        "Operating cash flow at least net income every year": cash_check,
        "Liabilities no more than twice equity, latest year": leverage_check,
    }
