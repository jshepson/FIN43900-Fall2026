#!/usr/bin/env python3
"""Compute a fixed Buffett-style 10-K fact table from SEC EDGAR company facts."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
FIELDS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "equity": ["StockholdersEquity"],
    "liabilities": ["Liabilities"],
    "assets_current": ["AssetsCurrent"],
    "liabilities_current": ["LiabilitiesCurrent"],
}
DISPLAY = {"revenue": "Revenue", "net_income": "Net income", "operating_cash_flow": "Operating cash flow", "capital_spending": "Capital spending", "equity": "Equity", "liabilities": "Liabilities", "assets_current": "AssetsCurrent", "liabilities_current": "LiabilitiesCurrent"}
BALANCE_SHEET_FIELDS = {"equity", "liabilities", "assets_current", "liabilities_current"}


def download_json(url: str, user_agent: str) -> dict:
    request = Request(url, headers={"User-Agent": user_agent})
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"SEC returned HTTP {error.code} for {url}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach SEC EDGAR: {error.reason}") from error


def cik_for_ticker(ticker: str, user_agent: str) -> int:
    records = download_json(TICKERS_URL, user_agent)
    for record in records.values():
        if record["ticker"].upper() == ticker.upper():
            return int(record["cik_str"])
    raise ValueError(f"Ticker {ticker!r} was not found in SEC's company_tickers.json")


def is_one_year_flow(fact: dict) -> bool:
    start, end = fact.get("start"), fact.get("end")
    if not start or not end:
        return False
    return 300 <= (date.fromisoformat(end) - date.fromisoformat(start)).days <= 400


def filing_timestamp(fact: dict) -> tuple[str, str]:
    return (fact.get("filed", ""), fact.get("accn", ""))


def annual_candidates(company_facts: dict, tag: str, flow: bool) -> dict[str, dict]:
    units = company_facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {})
    candidates: dict[str, dict] = {}
    for facts in units.values():
        for fact in facts:
            if fact.get("form") != "10-K" or not fact.get("fy") or fact.get("fp") != "FY":
                continue
            if flow and not is_one_year_flow(fact):
                continue
            end = fact.get("end")
            if end and (end not in candidates or filing_timestamp(fact) > filing_timestamp(candidates[end])):
                candidates[end] = fact
    return candidates


def select_fact(company_facts: dict, tags: list[str], end: str, flow: bool) -> tuple[dict | None, str | None]:
    for tag in tags:
        fact = annual_candidates(company_facts, tag, flow).get(end)
        if fact is not None:
            return fact, tag
    return None, None


def value_in_millions(fact: dict | None) -> float | None:
    return None if fact is None else float(fact["val"]) / 1_000_000


def format_value(value: float | None) -> str:
    return "not found" if value is None else f"{value:,.0f}"


def format_percent(value: float | None) -> str:
    return "not known" if value is None else f"{value * 100:.1f}%"


def format_ratio(value: float | None) -> str:
    return "not known" if value is None else f"{value:.2f}"


def five_fiscal_year_ends(company_facts: dict) -> list[str]:
    return sorted(annual_candidates(company_facts, "NetIncomeLoss", flow=True))[-5:]


def build_rows(company_facts: dict) -> list[dict]:
    rows = []
    for end in five_fiscal_year_ends(company_facts):
        row: dict = {"fiscal_year_end": end, "tags": {}}
        for field, tags in FIELDS.items():
            fact, tag = select_fact(company_facts, tags, end, flow=field not in BALANCE_SHEET_FIELDS)
            row[field] = value_in_millions(fact)
            row["tags"][field] = tag or "not found"
        equity, net_income = row["equity"], row["net_income"]
        row["roe"] = net_income / equity if net_income is not None and equity is not None and equity > 0 else None
        ocf, capex = row["operating_cash_flow"], row["capital_spending"]
        row["owner_earnings"] = ocf - capex if ocf is not None and capex is not None else None
        assets_current, liabilities_current = row["assets_current"], row["liabilities_current"]
        row["current_ratio"] = assets_current / liabilities_current if assets_current is not None and liabilities_current is not None and liabilities_current > 0 else None
        liabilities = row["liabilities"]
        row["liabilities_to_equity"] = liabilities / equity if liabilities is not None and equity is not None and equity > 0 else None
        rows.append(row)
    return rows


def check_results(rows: list[dict]) -> dict[str, str]:
    roe = [row["roe"] for row in rows]
    owner_earnings = [row["owner_earnings"] for row in rows]
    return {
        "ROE of 15% or more every year": "not known" if any(value is None for value in roe) else ("pass" if all(value >= 0.15 for value in roe) else "fail"),
        "Owner earnings positive every year": "not known" if any(value is None for value in owner_earnings) else ("pass" if all(value > 0 for value in owner_earnings) else "fail"),
        "Owner earnings grew, first year to last": "not known" if len(owner_earnings) < 2 or owner_earnings[0] is None or owner_earnings[-1] is None else ("pass" if owner_earnings[-1] > owner_earnings[0] else "fail"),
    }


def print_report(ticker: str, cik: int, rows: list[dict], checks: dict[str, str]) -> None:
    print(f"{ticker.upper()} — SEC EDGAR 10-K facts (USD millions); CIK {cik:010d}")
    print("Latest 10-K filing wins when the same fiscal-year period appears more than once.\n")
    print("FY end | Revenue | Net income | Operating cash flow | Capital spending | Equity | Liabilities | Assets current | Liabilities current | ROE | Current ratio | Liabilities / equity | Owner earnings")
    print("--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---")
    for row in rows:
        print(" | ".join([row["fiscal_year_end"], format_value(row["revenue"]), format_value(row["net_income"]), format_value(row["operating_cash_flow"]), format_value(row["capital_spending"]), format_value(row["equity"]), format_value(row["liabilities"]), format_value(row["assets_current"]), format_value(row["liabilities_current"]), format_percent(row["roe"]), format_ratio(row["current_ratio"]), format_ratio(row["liabilities_to_equity"]), format_value(row["owner_earnings"])]))
        print("  tags: " + "; ".join(f"{DISPLAY[field]}={row['tags'][field]}" for field in FIELDS))
    print("\nBuffett checks")
    for name, result in checks.items():
        print(f"- {name}: {result}")


def report(ticker: str, user_agent: str) -> dict:
    cik = cik_for_ticker(ticker, user_agent)
    rows = build_rows(download_json(FACTS_URL.format(cik=cik), user_agent))
    if len(rows) < 5:
        raise RuntimeError(f"Only found {len(rows)} annual 10-K net-income periods; need five.")
    return {"ticker": ticker.upper(), "cik": cik, "rows": rows, "checks": check_results(rows), "retrieved_at": datetime.now().isoformat(timespec="seconds")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker", help="SEC-listed ticker, e.g. COST")
    parser.add_argument("--user-agent", required=True, help="Your name and contact email for SEC EDGAR")
    parser.add_argument("--json-output", type=Path, help="Optional path for the exact computed report")
    args = parser.parse_args()
    try:
        result = report(args.ticker, args.user_agent)
    except (RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print_report(result["ticker"], result["cik"], result["rows"], result["checks"])
    if args.json_output:
        args.json_output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"\nSaved exact computed report to {args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
