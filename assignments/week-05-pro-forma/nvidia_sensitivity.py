"""Lab 11 one-at-a-time sensitivity analysis for the NVIDIA pro-forma.

All dollar amounts are USD millions except value per share.  This module keeps
the base input set separate and creates a new copy for every model run.
"""

from copy import deepcopy

from nvidia_proforma import (
    YEARS, opening, rd_to_revenue, sga_to_gross_profit, inventory_days,
    receivable_days, payable_days, prepaids_to_revenue,
    accrued_to_revenue, depreciation_to_opening_ppe, capex, tax_rate,
    interest_rate, shareholder_return_rate, minimum_cash, revolver_limit,
    revolver_rate, cost_of_equity, terminal_growth, shares_outstanding,
    assert_balanced,
)


# Independent base assumptions.  Each scenario starts from a deepcopy of this
# dictionary so a previous run cannot leak into the next one.
BASE_INPUTS = {
    "revenue_growth": [0.70, 0.40, 0.25, 0.15, 0.08],
    "gross_margin": [0.740, 0.740, 0.735, 0.730, 0.725],
}

SENSITIVITIES = {
    "Revenue-growth path (percentage points)": {
        "input_key": "revenue_growth",
        "lower": [x - 0.05 for x in BASE_INPUTS["revenue_growth"]],
        "higher": [x + 0.05 for x in BASE_INPUTS["revenue_growth"]],
        "units": "% of prior-year revenue",
    },
    "Gross-margin path (percentage points)": {
        "input_key": "gross_margin",
        "lower": [x - 0.01 for x in BASE_INPUTS["gross_margin"]],
        "higher": [x + 0.01 for x in BASE_INPUTS["gross_margin"]],
        "units": "% of revenue",
    },
}


def run_model(inputs):
    """Run the linked income statement, balance sheet, cash flow, and FCFE value."""
    prior, model = opening.copy(), []
    for i, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1 + inputs["revenue_growth"][i])
        gross_profit = revenue * inputs["gross_margin"][i]
        cost_of_revenue = revenue - gross_profit
        rd = revenue * rd_to_revenue[i]
        sga = gross_profit * sga_to_gross_profit[i]
        depreciation = prior["ppe"] * depreciation_to_opening_ppe
        operating_income = gross_profit - rd - sga - depreciation
        interest = prior["debt"] * interest_rate + prior["revolver"] * revolver_rate
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * tax_rate
        net_income = pretax_income - tax

        receivables = revenue * receivable_days / 365
        inventory = cost_of_revenue * inventory_days / 365
        prepaids = revenue * prepaids_to_revenue
        accounts_payable = cost_of_revenue * payable_days / 365
        accrued_liabilities = revenue * accrued_to_revenue
        ppe = prior["ppe"] + capex[i] - depreciation
        shareholder_returns = net_income * shareholder_return_rate
        operating_nwc_change = ((receivables - prior["receivables"]) +
                                (inventory - prior["inventory"]) +
                                (prepaids - prior["prepaids"]) -
                                (accounts_payable - prior["accounts_payable"]) -
                                (accrued_liabilities - prior["accrued_liabilities"]))
        fcfe = net_income + depreciation - capex[i] - operating_nwc_change
        cash_before_revolver = prior["cash"] + fcfe - shareholder_returns
        revolver = prior["revolver"]
        if cash_before_revolver < minimum_cash:
            draw = min(minimum_cash - cash_before_revolver, revolver_limit - revolver)
            revolver += draw
            cash = cash_before_revolver + draw
        else:
            repayment = min(revolver, cash_before_revolver - minimum_cash)
            revolver -= repayment
            cash = cash_before_revolver - repayment

        equity = prior["equity"] + net_income - shareholder_returns
        current = {
            "revenue": revenue, "gross_profit": gross_profit, "cost_of_revenue": cost_of_revenue,
            "rd": rd, "sga": sga, "depreciation": depreciation, "operating_income": operating_income,
            "interest": interest, "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "receivables": receivables, "inventory": inventory, "prepaids": prepaids, "ppe": ppe,
            "cash": cash, "accounts_payable": accounts_payable, "accrued_liabilities": accrued_liabilities,
            "debt": prior["debt"], "revolver": revolver, "equity": equity,
            "other_non_cash_assets": prior["other_non_cash_assets"],
            "marketable_securities": prior["marketable_securities"],
            "other_liabilities": prior["other_liabilities"], "fcfe": fcfe,
            "shareholder_returns": shareholder_returns, "operating_nwc_change": operating_nwc_change,
        }
        current["assets"] = sum(current[k] for k in (
            "cash", "marketable_securities", "receivables", "inventory", "prepaids", "ppe", "other_non_cash_assets"))
        current["liabilities"] = sum(current[k] for k in (
            "accounts_payable", "accrued_liabilities", "debt", "revolver", "other_liabilities"))
        current["balance_gap"] = current["assets"] - current["liabilities"] - equity
        assert_balanced(year, current["balance_gap"], cash)
        model.append(current)
        prior = current

    equity_value = sum(m["fcfe"] / (1 + cost_of_equity) ** (i + 1) for i, m in enumerate(model))
    terminal_value = model[-1]["fcfe"] * (1 + terminal_growth) / (cost_of_equity - terminal_growth)
    equity_value += terminal_value / (1 + cost_of_equity) ** len(YEARS)
    return {"inputs": deepcopy(inputs), "model": model, "equity_value": equity_value,
            "value_per_share": equity_value / shares_outstanding}


def summary(result):
    final = result["model"][-1]
    return {"operating_income": final["operating_income"], "fcfe": final["fcfe"],
            "value_per_share": result["value_per_share"],
            "max_balance_gap": max(abs(m["balance_gap"]) for m in result["model"]),
            "minimum_cash_headroom": min(m["cash"] - minimum_cash for m in result["model"])}


def format_path(values):
    return ", ".join(f"{value:.1%}" for value in values)


def print_driver(driver_name, specification, base_result):
    results = {}
    for case, path in (("Lower", specification["lower"]), ("Base", BASE_INPUTS[specification["input_key"]]),
                       ("Higher", specification["higher"])):
        inputs = deepcopy(BASE_INPUTS)
        inputs[specification["input_key"]] = path[:]
        results[case] = run_model(inputs)

    base = summary(base_result)
    print(f"\n{driver_name}")
    print(f"Units: {specification['units']}; FY2027E-FY2031E")
    print("Case     Input path                         Op. income   FCFE (FCFE)   Value/share   Check")
    for case in ("Lower", "Base", "Higher"):
        item = summary(results[case])
        print(f"{case:<9}{format_path(results[case]['inputs'][specification['input_key']]):<35}"
              f"${item['operating_income']:>10,.1f} ${item['fcfe']:>10,.1f}   ${item['value_per_share']:>9.2f}  "
              f"pass (gap ${item['max_balance_gap']:.1f}m)")
        if case != "Base":
            print(f"          Change from base:                  ${item['operating_income'] - base['operating_income']:>+10,.1f} ${item['fcfe'] - base['fcfe']:>+10,.1f}   ${item['value_per_share'] - base['value_per_share']:>+9.2f}")
    values = [summary(results[case]) for case in ("Lower", "Base", "Higher")]
    print("Span (max - min):                           "
          f"${max(x['operating_income'] for x in values) - min(x['operating_income'] for x in values):>10,.1f} "
          f"${max(x['fcfe'] for x in values) - min(x['fcfe'] for x in values):>10,.1f}   "
          f"${max(x['value_per_share'] for x in values) - min(x['value_per_share'] for x in values):>9.2f}")
    return results


def main():
    base_before = run_model(deepcopy(BASE_INPUTS))
    print("NVIDIA Lab 11 — One-at-a-Time Sensitivity (USD millions except per-share data)")
    print("Base before: FY2031E operating income ${:,.1f}; FCFE ${:,.1f}; value/share ${:.2f}".format(
        summary(base_before)["operating_income"], summary(base_before)["fcfe"], summary(base_before)["value_per_share"]))
    for name, specification in SENSITIVITIES.items():
        print_driver(name, specification, base_before)
    base_after = run_model(deepcopy(BASE_INPUTS))
    before, after = summary(base_before), summary(base_after)
    same = all(abs(before[key] - after[key]) < 0.005 for key in before)
    print("\nRestored-base check: {}. Base inputs and output metrics match within $0.005m / $0.005 per share.".format(
        "PASS" if same else "FAIL"))
    print("Selected trace — revenue-growth higher case FY2031E: linked revenue, operating income, FCFE")
    traced = run_model({**deepcopy(BASE_INPUTS), "revenue_growth": SENSITIVITIES["Revenue-growth path (percentage points)"]["higher"]})
    final = traced["model"][-1]
    print("Revenue ${:,.1f}; operating income ${:,.1f}; FCFE ${:,.1f}; balance gap ${:,.1f}m".format(
        final["revenue"], final["operating_income"], final["fcfe"], final["balance_gap"]))


if __name__ == "__main__":
    main()
