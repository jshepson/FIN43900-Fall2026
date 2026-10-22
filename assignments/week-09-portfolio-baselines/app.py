"""Streamlit interface for the Lab 15 portfolio-stability exercise.

Run from this directory: streamlit run app.py
"""

from copy import deepcopy
from io import StringIO

import streamlit as st

from portfolio import (
    CORRELATIONS,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    estimate_from_prices,
    find_lowest_risk_mix,
)


st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")


def loaded_inputs(uploaded_file):
    """Return current inputs and the all-history comparison inputs."""
    if uploaded_file is None:
        return deepcopy(SLEEVES), deepcopy(CORRELATIONS), "Meridian training inputs"
    csv_text = uploaded_file.getvalue().decode("utf-8-sig")
    all_history = estimate_from_prices(StringIO(csv_text), last_36=False)
    current = estimate_from_prices(StringIO(csv_text), last_36=st.session_state.last_36)
    return *current, "Uploaded CSV (all monthly returns)"


def render_result(result):
    if result is None:
        st.warning("No mix meets the objective.")
        return
    st.dataframe(
        {
            "Asset": list(result["weights"]),
            "Weight": [f"{weight:.0%}" for weight in result["weights"].values()],
        },
        hide_index=True,
        use_container_width=True,
    )
    st.metric("Expected return", f"{result['expected_return']:.2%}")
    st.metric("Volatility", f"{result['volatility']:.2%}")
    st.metric("Reserve-eligible weight", f"{result['reserve_weight']:.2%}")


st.title("Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Mandate controls")
    objective = st.number_input("Objective expected return (%)", value=OBJECTIVE_RETURN * 100, step=0.1) / 100
    reserve_minimum = st.number_input("Minimum reserve-eligible weight (%)", value=3.0, min_value=0.0, max_value=100.0, step=1.0) / 100
    uploaded_file = st.file_uploader("Upload monthly prices.csv", type="csv")
    st.toggle("Use last 36 monthly returns", key="last_36")

try:
    source_sleeves, source_correlations, comparison_label = loaded_inputs(uploaded_file)
    if uploaded_file is None:
        comparison_sleeves, comparison_correlations = deepcopy(SLEEVES), deepcopy(CORRELATIONS)
    else:
        csv_text = uploaded_file.getvalue().decode("utf-8-sig")
        comparison_sleeves, comparison_correlations = estimate_from_prices(StringIO(csv_text))
except (UnicodeDecodeError, ValueError) as error:
    st.error(f"Could not use this CSV: {error}")
    st.stop()

st.subheader("Expected-return estimates")
edited_sleeves = deepcopy(source_sleeves)
columns = st.columns(len(source_sleeves))
for column, name in zip(columns, source_sleeves):
    with column:
        edited_sleeves[name]["return"] = st.number_input(
            name,
            value=float(source_sleeves[name]["return"] * 100),
            step=0.1,
            key=f"return_{name}",
        ) / 100

st.subheader("Reserve eligibility")
eligibility_columns = st.columns(len(source_sleeves))
reserve_eligible = {
    name
    for column, name in zip(eligibility_columns, source_sleeves)
    if column.checkbox(name, value=name in RESERVE_ELIGIBLE, key=f"reserve_{name}")
}

current_result = find_lowest_risk_mix(
    edited_sleeves, source_correlations, objective, reserve_eligible, reserve_minimum
)
loaded_result = find_lowest_risk_mix(
    comparison_sleeves, comparison_correlations, objective, reserve_eligible, reserve_minimum
)

current_column, loaded_column = st.columns(2)
with current_column:
    st.subheader("Lowest-risk mix for current controls")
    render_result(current_result)
with loaded_column:
    st.subheader(f"Answer as loaded: {comparison_label}")
    render_result(loaded_result)
    if current_result is not None and loaded_result is not None:
        largest_change = max(
            abs(current_result["weights"][name] - loaded_result["weights"][name])
            for name in current_result["weights"]
        )
        st.metric("Largest weight change", f"{largest_change:.0%}")
