"""Streamlit view for the fixed Buffett EDGAR analysis."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

SKILL_SCRIPT = Path(__file__).parents[2] / ".codex/skills/buffett-edgar/scripts/analyze_company.py"
sys.path.insert(0, str(SKILL_SCRIPT.parent))
from analyze_company import report  # noqa: E402


def displayed_numbers(result: dict) -> set[str]:
    numbers: set[str] = set()
    for row in result["rows"]:
        for field in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "owner_earnings"):
            if row[field] is not None:
                numbers.add(f"{row[field]:,.0f}")
        if row["roe"] is not None:
            numbers.add(f"{row['roe'] * 100:.1f}")
    return numbers


def memo_number_audit(memo: str, result: dict) -> list[str]:
    allowed = displayed_numbers(result)
    candidates = re.findall(r"(?<![\w.])(?!\d+-K)\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?%?", memo)
    flagged = []
    for candidate in candidates:
        normalized = candidate.lstrip("$").rstrip("%")
        if normalized not in allowed and normalized not in flagged:
            flagged.append(normalized)
    return flagged


@st.cache_data(show_spinner=False)
def analyze(ticker: str, user_agent: str) -> dict:
    return report(ticker, user_agent)


st.set_page_config(page_title="Buffett EDGAR review", layout="wide")
st.title("Buffett-style business review")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
with st.sidebar:
    ticker = st.text_input("Ticker", "COST").strip().upper()
    user_agent = st.text_input("SEC User-Agent (your name and email)", type="password", placeholder="Full Name email@example.edu")
    run = st.button("Load 10-K facts", type="primary")
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
    st.subheader(f"{result['ticker']} — owner earnings and net income ($ millions)")
    st.line_chart(frame.set_index("fiscal_year_end")[["owner_earnings", "net_income"]])
    st.subheader("10-K fact table ($ millions)")
    table = frame[["fiscal_year_end", "revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "roe", "owner_earnings"]].copy()
    table["roe"] = table["roe"].map(lambda value: "not known" if pd.isna(value) else f"{value * 100:.1f}%")
    st.dataframe(table, width="stretch", hide_index=True)
    with st.expander("XBRL tags used"):
        st.json([{ "fiscal_year_end": row["fiscal_year_end"], **row["tags"] } for row in result["rows"]])
    st.subheader("Buffett checks")
    st.table(pd.DataFrame(result["checks"].items(), columns=["Check", "Result"]))
    memo_path = Path(__file__).with_name(f"{result['ticker']}_buffett_memo.md")
    default_memo = memo_path.read_text(encoding="utf-8") if memo_path.exists() else "# Buffett memo\n\nWrite a short, price-free memo using only this table."
    st.subheader("Buffett memo")
    memo = st.text_area("Memo markdown", default_memo, height=220)
    st.markdown(memo)
    flagged = memo_number_audit(memo, result)
    if flagged:
        st.warning("Numbers in the memo that were not printed by the script: " + ", ".join(flagged))
    else:
        st.success("Every number in this memo appears in the script's computed table.")
else:
    st.info("Enter a ticker and SEC User-Agent, then load its 10-K facts.")
