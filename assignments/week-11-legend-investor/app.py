"""Streamlit view for the Lab 19 Buffett, Graham, and Burry EDGAR panel."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

SKILLS = Path(__file__).parents[2] / ".codex/skills"
sys.path.extend([str(SKILLS / "buffett-edgar/scripts"), str(SKILLS / "graham-edgar/scripts"), str(SKILLS / "burry-edgar/scripts")])
from analyze_company import report  # noqa: E402
from burry_checks import check_results as burry_checks  # noqa: E402
from graham_checks import check_results as graham_checks  # noqa: E402


def panel_checks(result: dict) -> dict[str, dict[str, str]]:
    return {"Buffett": result["checks"], "Graham": graham_checks(result["rows"]), "Burry": burry_checks(result["rows"])}


def verdict(checks: dict[str, str]) -> str:
    values = list(checks.values())
    if values and all(value == "pass" for value in values):
        return "own the business"
    if values.count("fail") >= 2:
        return "pass"
    return "watch it"


def displayed_numbers(result: dict, checks: dict[str, dict[str, str]]) -> set[str]:
    numbers: set[str] = {"1.0", "2.0"}
    for row in result["rows"]:
        for field in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities", "assets_current", "liabilities_current", "owner_earnings"):
            if row.get(field) is not None:
                numbers.add(f"{row[field]:,.0f}")
        if row.get("roe") is not None:
            numbers.add(f"{row['roe'] * 100:.1f}")
        for field in ("current_ratio", "liabilities_to_equity"):
            if row.get(field) is not None:
                numbers.add(f"{row[field]:.2f}")
    return numbers


def memo_number_audit(memo: str, result: dict, checks: dict[str, dict[str, str]]) -> list[str]:
    allowed = displayed_numbers(result, checks)
    candidates = re.findall(r"(?<![\w.])(?!\d+-K)\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?%?", memo)
    flagged = []
    for candidate in candidates:
        normalized = candidate.lstrip("$").rstrip("%")
        if normalized not in allowed and normalized not in flagged:
            flagged.append(normalized)
    return flagged


def memo_for(ticker: str, investor: str) -> str:
    path = Path(__file__).with_name(f"{ticker}_{investor.lower()}_memo.md")
    return path.read_text(encoding="utf-8") if path.exists() else f"# {investor} memo\n\nWrite a short, price-free memo using only the panel table."


@st.cache_data(show_spinner=False)
def analyze(ticker: str, user_agent: str) -> dict:
    return report(ticker, user_agent)


st.set_page_config(page_title="Legend investor panel", layout="wide")
st.title("Legend investor panel")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
with st.sidebar:
    ticker = st.text_input("Ticker", "COST").strip().upper()
    user_agent = st.text_input("SEC User-Agent (your name and email)", type="password", placeholder="Full Name email@example.edu")
    run = st.button("Load 10-K panel", type="primary")
if run:
    if not user_agent.strip():
        st.error("Enter a truthful User-Agent with your name and contact email before contacting SEC EDGAR.")
    else:
        try:
            st.session_state["result"] = analyze(ticker, user_agent.strip())
        except Exception as error:
            st.error(f"EDGAR query failed: {error}")
result = st.session_state.get("result")
if result:
    frame = pd.DataFrame(result["rows"])
    checks = panel_checks(result)
    st.subheader(f"{result['ticker']} — owner earnings and net income ($ millions)")
    st.line_chart(frame.set_index("fiscal_year_end")[["owner_earnings", "net_income"]])
    st.subheader("10-K fact table ($ millions except ratios)")
    columns = ["fiscal_year_end", "revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities", "assets_current", "liabilities_current", "roe", "current_ratio", "liabilities_to_equity", "owner_earnings"]
    table = frame[columns].copy()
    table["roe"] = table["roe"].map(lambda value: "not known" if pd.isna(value) else f"{value * 100:.1f}%")
    for field in ("current_ratio", "liabilities_to_equity"):
        table[field] = table[field].map(lambda value: "not known" if pd.isna(value) else f"{value:.2f}")
    st.dataframe(table, width="stretch", hide_index=True)
    with st.expander("XBRL tags used"):
        st.json([{ "fiscal_year_end": row["fiscal_year_end"], **row["tags"] } for row in result["rows"]])
    panel_rows = [{"Investor": investor, "Check": check, "Result": outcome} for investor, investor_checks in checks.items() for check, outcome in investor_checks.items()]
    st.subheader("Panel checks")
    st.table(pd.DataFrame(panel_rows))
    probe = graham_checks(result["rows"], current_ratio_threshold=1.0)
    st.caption(f"Graham threshold probe (1.0): {next(iter(probe.values()))}. Retained threshold: 2.0.")
    st.subheader("Panel verdicts")
    st.table(pd.DataFrame([{"Investor": investor, "Verdict": verdict(investor_checks)} for investor, investor_checks in checks.items()]))
    st.subheader("Investor memos")
    audits = []
    for column, investor in zip(st.columns(3), ("Buffett", "Graham", "Burry"), strict=True):
        with column:
            st.markdown(f"### {investor}")
            memo = st.text_area(f"{investor} memo markdown", memo_for(result["ticker"], investor), height=260)
            st.markdown(memo)
            audits.extend((investor, number) for number in memo_number_audit(memo, result, checks))
    if audits:
        st.warning("Numbers in the memos that were not printed by the scripts: " + ", ".join(f"{investor}: {number}" for investor, number in audits))
    else:
        st.success("Every number in all three memos appears in the scripts' computed panel.")
else:
    st.info("Enter a ticker and SEC User-Agent, then load its 10-K panel.")
