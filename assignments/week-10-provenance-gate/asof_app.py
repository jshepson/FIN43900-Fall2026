"""Lab 17 FRED/ALFRED point-in-time rate viewer.

Run from this folder with:
    ../../.venv/bin/streamlit run asof_app.py
"""

from __future__ import annotations

from datetime import date
from io import StringIO
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import pandas as pd
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Effective federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year fixed mortgage rate",
}
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_CSV = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}&vintage_date={vintage_date}"


def read_series(url: str, series_id: str) -> pd.DataFrame:
    """Download and normalize a two-column FRED/ALFRED CSV."""
    try:
        with urlopen(url, timeout=20) as response:
            text = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as error:
        raise ValueError(f"Could not download {series_id}: {error}") from error

    frame = pd.read_csv(StringIO(text))
    if frame.shape[1] != 2:
        raise ValueError(f"{series_id} did not return a two-column data file.")
    frame.columns = ["date", "value"]
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    # FRED/ALFRED use "." for an observation that is not available.
    frame["value"] = pd.to_numeric(frame["value"].replace(".", pd.NA), errors="coerce")
    return frame.dropna(subset=["date"]).sort_values("date")


@st.cache_data(show_spinner=False)
def download_today(series_id: str) -> pd.DataFrame:
    """Get the series exactly as FRED displays it today."""
    return read_series(FRED_CSV.format(series_id=series_id), series_id)


@st.cache_data(show_spinner=False)
def download_as_known_on(series_id: str, vintage_date: str) -> pd.DataFrame:
    """Get the series as ALFRED recorded it on the selected historical date."""
    url = ALFRED_CSV.format(series_id=series_id, vintage_date=vintage_date)
    return read_series(url, series_id)


def nonmissing(frame: pd.DataFrame, start_date: date) -> pd.DataFrame:
    return frame[(frame["date"].dt.date >= start_date) & frame["value"].notna()].copy()


def summary_row(series_id: str, today: pd.DataFrame, asof: pd.DataFrame, start_date: date) -> dict[str, object]:
    """Compare today with the point-in-time view without using future values."""
    current = nonmissing(today, start_date)
    known = nonmissing(asof, start_date)
    if known.empty:
        raise ValueError(f"No non-missing {series_id} values were known after {start_date}.")

    latest_known = known.iloc[-1]
    latest_today = current.iloc[-1] if not current.empty else pd.Series({"date": pd.NaT, "value": pd.NA})
    current_after_known = current[current["date"] > latest_known["date"]]
    matched = known.merge(current, on="date", how="inner", suffixes=("_known", "_today"))
    revised = matched[matched["value_known"].round(10) != matched["value_today"].round(10)]
    return {
        "Series ID": series_id,
        "FRED page": f"https://fred.stlouisfed.org/series/{series_id}",
        "Last known date": latest_known["date"].date().isoformat(),
        "Value known then": float(latest_known["value"]),
        "Last date today": latest_today["date"].date().isoformat() if pd.notna(latest_today["date"]) else "—",
        "Value today": float(latest_today["value"]) if pd.notna(latest_today["value"]) else pd.NA,
        "Today values after known date": len(current_after_known),
        "Revised same-date values": len(revised),
    }


st.set_page_config(page_title="Point-in-Time Rates", layout="wide")
st.title("Point-in-Time Rates")
st.caption(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
    "built with AI help, a learning demonstration, not investment advice."
)

with st.sidebar:
    st.header("Series and dates")
    selected = st.multiselect(
        "Rate series",
        options=list(SERIES),
        default=list(SERIES),
        format_func=lambda series_id: f"{series_id} — {SERIES[series_id]}",
    )
    typed_ids = st.text_input("Add FRED series ID(s), comma separated", value="").upper()
    additions = [item.strip() for item in typed_ids.split(",") if item.strip()]
    selected_ids = list(dict.fromkeys(selected + additions))
    start_date = st.date_input("Start date", value=date(2020, 1, 1))
    vintage_date = st.date_input("As known on", value=date.today(), max_value=date.today())

if not selected_ids:
    st.info("Select a series or enter a FRED series ID.")
    st.stop()

rows = []
for series_id in selected_ids:
    try:
        today = download_today(series_id)
        asof = download_as_known_on(series_id, vintage_date.isoformat())
        chart = nonmissing(today, start_date).set_index("date")[["value"]].rename(columns={"value": series_id})
        st.subheader(f"{series_id} — {SERIES.get(series_id, 'Added FRED series')}")
        st.line_chart(chart, use_container_width=True)
        known = nonmissing(asof, start_date)
        if known.empty:
            st.warning(f"No {series_id} value was available after the selected start date as of {vintage_date}.")
        else:
            last_known = known.iloc[-1]
            st.caption(
                f"Last value known on {vintage_date:%d %B %Y}: "
                f"{last_known['date']:%d %B %Y} — {last_known['value']:,.3f}"
            )
        rows.append(summary_row(series_id, today, asof, start_date))
    except (ValueError, pd.errors.ParserError) as error:
        st.error(f"{series_id}: {error}")

st.subheader("As-known-on versus today")
if rows:
    table = pd.DataFrame(rows)
    st.dataframe(
        table,
        hide_index=True,
        use_container_width=True,
        column_config={
            "FRED page": st.column_config.LinkColumn("FRED page", display_text="Open FRED page"),
            "Value known then": st.column_config.NumberColumn(format="%.3f"),
            "Value today": st.column_config.NumberColumn(format="%.3f"),
        },
    )
else:
    st.warning("No selected series returned usable data.")
