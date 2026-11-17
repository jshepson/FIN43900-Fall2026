"""Reproduce the Project 2 historical-window comparison.

Run from the repository root:
    python3 assignments/project-2-meridian/analysis.py

The finance engine and sourced classroom price file remain in the earlier
portfolio lab folder so the result is traceable to its original evidence.
"""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PORTFOLIO_DIR = ROOT / "assignments" / "week-09-portfolio-baselines"
sys.path.insert(0, str(PORTFOLIO_DIR))

from portfolio import estimate_from_prices, find_lowest_risk_mix  # noqa: E402


OBJECTIVE = 0.065
GRID_STEP = 0.05
PRICES = PORTFOLIO_DIR / "prices.csv"


def run_window(last_36: bool) -> dict:
    """Estimate inputs and return the least-risk feasible 5%-grid mix."""
    sleeves, correlations = estimate_from_prices(str(PRICES), last_36=last_36)
    result = find_lowest_risk_mix(
        sleeves, correlations, OBJECTIVE, set(), reserve_minimum=0.0, step=GRID_STEP
    )
    if result is None:
        raise RuntimeError("The stated 6.5% objective unexpectedly has no feasible mix.")
    return {
        "observations": 36 if last_36 else 59,
        "annualized_arithmetic_returns_percent": {
            name: round(values["return"] * 100, 2) for name, values in sleeves.items()
        },
        "least_risk_feasible_mix_percent": {
            name: round(weight * 100, 2) for name, weight in result["weights"].items()
        },
        "expected_return_percent": round(result["expected_return"] * 100, 2),
        "volatility_percent": round(result["volatility"] * 100, 2),
    }


def main() -> None:
    output = {
        "decision": "Reject as an adoptable allocation; retain only as a pilot calculation.",
        "as_of": "2026-10-01 (last monthly adjusted-close observation)",
        "objective": "6.5% annualized arithmetic return estimate; gross and pre-cost",
        "constraints": "long-only 5% grid; 0% reserve floor because supplied universe has no reserve sleeve",
        "all_59_monthly_returns": run_window(False),
        "last_36_monthly_returns": run_window(True),
        "material_stability_result": "SPY rises 25 percentage points and VOO falls 25 percentage points when the all-history window is replaced by the latest 36 monthly returns. The selection changes from a 75/25 SPY/VOO overlap to 100% SPY.",
        "reversal_condition": "Reconsider only after a complete mandate, a genuine reserve sleeve, net-of-costs objective, overlap treatment, and stability checks.",
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
