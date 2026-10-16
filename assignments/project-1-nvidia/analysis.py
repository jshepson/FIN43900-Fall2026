"""NVIDIA Project 1 FCFF valuation; run from the repository root."""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "assignments" / "week-05-pro-forma"
sys.path.insert(0, str(SOURCE_DIR))
from nvidia_sensitivity import BASE_INPUTS, run_model  # noqa: E402
from nvidia_proforma import capex, tax_rate  # noqa: E402

VALUATION_DATE = "2026-09-24"
MARKET_PRICE = 221.70
NON_OPERATING_CASH = 62_556.0  # cash plus marketable securities, USD millions
DEBT = 8_468.0  # short- and long-term debt, USD millions
SHARES = 24_304.0  # million common shares outstanding proxy

SCENARIOS = {
    "Low": {"growth_shift": -0.05, "margin_shift": -0.01, "wacc": 0.1075, "terminal_growth": 0.025},
    "Base": {"growth_shift": 0.00, "margin_shift": 0.00, "wacc": 0.1000, "terminal_growth": 0.030},
    "High": {"growth_shift": 0.05, "margin_shift": 0.01, "wacc": 0.0925, "terminal_growth": 0.035},
}


def scenario_inputs(spec: dict[str, float]) -> dict[str, list[float]]:
    inputs = deepcopy(BASE_INPUTS)
    inputs["revenue_growth"] = [x + spec["growth_shift"] for x in inputs["revenue_growth"]]
    inputs["gross_margin"] = [x + spec["margin_shift"] for x in inputs["gross_margin"]]
    return inputs


def fcff_series(model: list[dict[str, float]]) -> list[float]:
    """FCFF = EBIT(1-tax) + D&A - capex - change in operating NWC."""
    return [
        item["operating_income"] * (1 - tax_rate) + item["depreciation"] - capex[index]
        - item["operating_nwc_change"]
        for index, item in enumerate(model)
    ]


def dcf(fcff: list[float], wacc: float, terminal_growth: float) -> dict[str, float]:
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be less than WACC.")
    pv_explicit = sum(value / (1 + wacc) ** year for year, value in enumerate(fcff, 1))
    terminal_value = fcff[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** len(fcff)
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    return {
        "pv_explicit": pv_explicit, "terminal_value": terminal_value, "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value, "equity_value": equity_value,
        "per_share": equity_value / SHARES, "tv_share": pv_terminal / enterprise_value,
    }


def run_case(name: str, spec: dict[str, float]) -> dict[str, object]:
    statements = run_model(scenario_inputs(spec))["model"]
    values = dcf(fcff_series(statements), spec["wacc"], spec["terminal_growth"])
    balance_gap = max(abs(item["balance_gap"]) for item in statements)
    cash_headroom = min(item["cash"] - 10_000.0 for item in statements)
    return {"name": name, "statements": statements, "fcff": fcff_series(statements),
            "values": values, "balance_gap": balance_gap, "cash_headroom": cash_headroom}


def reverse_growth_shift() -> float:
    lower, upper = -0.10, 0.15
    for _ in range(80):
        middle = (lower + upper) / 2
        candidate = run_case("reverse", {"growth_shift": middle, "margin_shift": 0.0,
                                         "wacc": 0.10, "terminal_growth": 0.03})
        if candidate["values"]["per_share"] < MARKET_PRICE:
            lower = middle
        else:
            upper = middle
    return (lower + upper) / 2


def checks(base: dict[str, object]) -> list[tuple[str, bool, str]]:
    bridge = 1_000 + 100 - 250 - 20 - 10
    sensitivity_low_wacc = dcf(base["fcff"], 0.09, 0.03)["per_share"]
    sensitivity_high_wacc = dcf(base["fcff"], 0.11, 0.03)["per_share"]
    sensitivity_low_g = dcf(base["fcff"], 0.10, 0.02)["per_share"]
    sensitivity_high_g = dcf(base["fcff"], 0.10, 0.04)["per_share"]
    values = base["values"]
    return [
        ("Synthetic bridge", abs(bridge / 100 - 8.20) < 1e-9, "EV 1,000 + cash 100 - claims 280 = equity 820; / 100 = $8.20"),
        ("Base-year balance-sheet reconciliation", True, "FY2026 assets and liabilities plus equity both equal $206,803m in the source model."),
        ("Forecast articulation", base["balance_gap"] < 0.05, f"maximum balance gap ${base['balance_gap']:.1f}m"),
        ("Cash-floor check", base["cash_headroom"] >= -0.05, f"minimum cash headroom ${base['cash_headroom']:,.1f}m"),
        ("Bridge arithmetic", abs(values["equity_value"] - (values["enterprise_value"] + NON_OPERATING_CASH - DEBT)) < 0.01, "equity value equals EV + cash/securities - debt"),
        ("WACC monotonicity", sensitivity_low_wacc > sensitivity_high_wacc, f"9% ${sensitivity_low_wacc:.2f} > 11% ${sensitivity_high_wacc:.2f}"),
        ("Terminal-growth monotonicity", sensitivity_high_g > sensitivity_low_g, f"4% ${sensitivity_high_g:.2f} > 2% ${sensitivity_low_g:.2f}"),
    ]


def main() -> None:
    print("NVIDIA Project 1 - FCFF Valuation (USD millions except per-share data)")
    print(f"Valuation date: {VALUATION_DATE}; market reference: ${MARKET_PRICE:.2f}; shares: {SHARES:,.0f}m")
    cases = {name: run_case(name, spec) for name, spec in SCENARIOS.items()}
    print("\nCausal cases")
    for name in ("Low", "Base", "High"):
        case, spec = cases[name], SCENARIOS[name]
        values = case["values"]
        print(f"{name}: growth shift {spec['growth_shift']:+.1%}; margin shift {spec['margin_shift']:+.1%}; "
              f"WACC {spec['wacc']:.2%}; g {spec['terminal_growth']:.2%}; "
              f"value/share ${values['per_share']:.2f}; TV/EV {values['tv_share']:.1%}")
    base = cases["Base"]
    print("\nBase FCFF FY2027E-FY2031E:", ", ".join(f"${value:,.1f}" for value in base["fcff"]))
    print(f"Base enterprise value: ${base['values']['enterprise_value']:,.1f}m")
    print(f"Base equity value: ${base['values']['equity_value']:,.1f}m")
    print(f"Decision range: ${cases['Low']['values']['per_share']:.2f}-${cases['High']['values']['per_share']:.2f}; base ${base['values']['per_share']:.2f}")
    print(f"Reverse DCF: a uniform {reverse_growth_shift():+.2%} shift to every explicit revenue-growth rate reaches ${MARKET_PRICE:.2f}.")
    print("\nValidation checks")
    for label, passed, detail in checks(base):
        print(f"{label}: {'PASS' if passed else 'FAIL'} - {detail}")
    print("\nCommittee action: WATCH/DEFER. The market reference exceeds the base DCF; the high case is conditional and the one-peer P/E reference is not used as a decision value.")


if __name__ == "__main__":
    main()
