"""ABG five-year three-statement pro-forma (USD millions, except per-share data)."""

YEARS = [2026, 2027, 2028, 2029, 2030]

# Opening FY2025 balance sheet and operating base.
opening = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "debt": 3_572.0,
    "revolver": 0.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
}

growth = 0.018
gross_margin = 0.1705
sga_to_gross_profit = [0.665, 0.655, 0.645, 0.645, 0.645]
depreciation_to_opening_ppe = 82.4 / 3_070.4
impairment = 120.0
capex = 250.0
tax_rate = 0.255
inventory_days = 2_135.8 / (17_999.0 - 3_071.7) * 365
floor_plan_to_inventory = 2_027.0 / 2_135.8
other_working_capital_rate = 0.008
minimum_cash = 25.0
revolver_limit = 850.0
revolver_rate = 0.06
debt_repayment = 150.0
share_buyback = 150.0
floor_plan_rate = 0.0467
term_debt_rate = 0.0544
cost_of_equity = 0.10
terminal_growth = 0.025
shares_outstanding = 17.951349


def assert_balanced(year, balance_gap, cash):
    """Refuse a statement set that does not balance or breaches minimum cash."""
    if abs(balance_gap) > 0.05:
        raise AssertionError(f"FY{year}E does not balance: gap {balance_gap:.1f}")
    if cash < minimum_cash - 0.05:
        raise AssertionError(f"FY{year}E cash below minimum: {cash:.1f}")


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'USD millions':<31}" + "".join(f"FY{year}E{'':>8}" for year in YEARS))
    for label, values in rows:
        print(f"{label:<31}" + "".join(f"{value:>12,.1f}" for value in values))


def main():
    prior = opening.copy()
    model = []

    for index, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1 + growth)
        gross_profit = revenue * gross_margin
        sga = gross_profit * sga_to_gross_profit[index]
        depreciation = prior["ppe"] * depreciation_to_opening_ppe
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (prior["floor_plan"] * floor_plan_rate
                    + prior["debt"] * term_debt_rate
                    + prior["revolver"] * revolver_rate)
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * tax_rate
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * inventory_days / 365
        floor_plan = inventory * floor_plan_to_inventory
        ppe = prior["ppe"] + capex - depreciation
        other_working_capital = other_working_capital_rate * (revenue - prior["revenue"])
        other_assets = prior["other_assets"] + other_working_capital - impairment
        debt = prior["debt"] - debt_repayment
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income - share_buyback

        fcfe = (net_income + depreciation + impairment - capex
                - (inventory - prior["inventory"]) - other_working_capital
                + (floor_plan - prior["floor_plan"]) - debt_repayment)
        cash_before_revolver = prior["cash"] + fcfe - share_buyback
        revolver = prior["revolver"]
        if cash_before_revolver < minimum_cash:
            draw = min(minimum_cash - cash_before_revolver, revolver_limit - revolver)
            revolver += draw
            cash = cash_before_revolver + draw
        else:
            repayment = min(revolver, cash_before_revolver - minimum_cash)
            revolver -= repayment
            cash = cash_before_revolver - repayment

        current = {
            "revenue": revenue, "gross_profit": gross_profit, "sga": sga,
            "depreciation": depreciation, "impairment": impairment,
            "operating_income": operating_income, "interest": interest,
            "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
            "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
            "cash": cash, "floor_plan": floor_plan, "debt": debt,
            "revolver": revolver, "other_liabilities": other_liabilities,
            "equity": equity, "other_working_capital": other_working_capital,
            "fcfe": fcfe,
        }
        current["assets"] = inventory + ppe + other_assets + cash
        current["liabilities"] = floor_plan + debt + revolver + other_liabilities
        current["balance_gap"] = current["assets"] - current["liabilities"] - equity
        assert_balanced(year, current["balance_gap"], cash)
        model.append(current)
        prior = current

    values = lambda key: [year[key] for year in model]
    print_table("Income Statement", [
        ("Revenue", values("revenue")), ("Gross profit", values("gross_profit")),
        ("SG&A", values("sga")), ("Depreciation", values("depreciation")),
        ("Impairment", values("impairment")), ("Operating income", values("operating_income")),
        ("Interest expense", values("interest")), ("Pretax income", values("pretax_income")),
        ("Tax", values("tax")), ("Net income", values("net_income")),
    ])
    print_table("Balance Sheet", [
        ("Inventory", values("inventory")), ("PP&E", values("ppe")),
        ("Other assets", values("other_assets")), ("Cash", values("cash")),
        ("Total assets", values("assets")), ("Floor plan", values("floor_plan")),
        ("Term debt", values("debt")), ("Revolver", values("revolver")),
        ("Other liabilities", values("other_liabilities")), ("Equity", values("equity")),
    ])
    print_table("Cash Flow", [
        ("Net income", values("net_income")), ("Depreciation", values("depreciation")),
        ("Impairment", values("impairment")), ("Capital spending", [-capex] * 5),
        ("Change in inventory", [-(m["inventory"] - (opening if i == 0 else model[i - 1])["inventory"]) for i, m in enumerate(model)]),
        ("Change in other working capital", [-m["other_working_capital"] for m in model]),
        ("Change in floor plan", [m["floor_plan"] - (opening if i == 0 else model[i - 1])["floor_plan"] for i, m in enumerate(model)]),
        ("Debt repayment", [-debt_repayment] * 5), ("Free cash flow to equity", values("fcfe")),
        ("Share buyback", [-share_buyback] * 5), ("Change in cash", [m["cash"] - (opening if i == 0 else model[i - 1])["cash"] for i, m in enumerate(model)]),
    ])
    print_table("Checks", [
        ("Assets - liabilities - equity", values("balance_gap")),
        ("Cash at or above minimum", [m["cash"] - minimum_cash for m in model]),
    ])

    pv_fcfe = sum(m["fcfe"] / (1 + cost_of_equity) ** (i + 1) for i, m in enumerate(model))
    terminal_value = ((model[-1]["fcfe"] + debt_repayment) * (1 + terminal_growth)
                      / (cost_of_equity - terminal_growth))
    pv_terminal_value = terminal_value / (1 + cost_of_equity) ** 5
    equity_value = pv_fcfe + pv_terminal_value
    print(f"\nEquity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {pv_terminal_value / equity_value:.1%}")
    print(f"Value per share: ${equity_value / shares_outstanding:,.2f}")


if __name__ == "__main__":
    main()
