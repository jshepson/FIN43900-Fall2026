"""NVIDIA five-year three-statement pro-forma (USD millions except per-share data)."""

YEARS = [2027, 2028, 2029, 2030, 2031]

# FY2026 opening balance sheet (year ended January 25, 2026).
opening = {
    "revenue": 215_938.0, "cash": 10_605.0, "marketable_securities": 51_951.0,
    "receivables": 38_466.0, "inventory": 21_403.0, "prepaids": 3_180.0,
    "ppe": 10_383.0, "other_non_cash_assets": 70_815.0,
    "accounts_payable": 9_812.0, "accrued_liabilities": 21_352.0,
    "debt": 8_468.0, "other_liabilities": 9_878.0, "revolver": 0.0,
    "equity": 157_293.0,
}

# Assumptions: the Data Center ramp is NVIDIA's company-specific driver.
revenue_growth = [0.70, 0.40, 0.25, 0.15, 0.08]
gross_margin = [0.740, 0.740, 0.735, 0.730, 0.725]
rd_to_revenue = [0.075, 0.074, 0.073, 0.072, 0.071]
sga_to_gross_profit = [0.030, 0.030, 0.031, 0.031, 0.032]
inventory_days = 125.0
receivable_days = 65.0
payable_days = 57.0
prepaids_to_revenue = 3_180.0 / 215_938.0
accrued_to_revenue = 21_352.0 / 215_938.0
depreciation_to_opening_ppe = 2_843.0 / 10_383.0
capex = [9_000.0, 11_000.0, 12_000.0, 13_000.0, 14_000.0]
tax_rate = 0.18
interest_rate = 259.0 / 8_468.0
shareholder_return_rate = 0.25
minimum_cash = 10_000.0
revolver_limit = 10_000.0
revolver_rate = 0.06
cost_of_equity = 0.10
terminal_growth = 0.03
shares_outstanding = 24_304.0


def assert_balanced(year, balance_gap, cash):
    """Refuse to print a broken statement set or a cash-floor breach."""
    if abs(balance_gap) > 0.05:
        raise AssertionError(f"FY{year}E does not balance: gap {balance_gap:.1f}")
    if cash < minimum_cash - 0.05:
        raise AssertionError(f"FY{year}E cash below minimum: {cash:.1f}")


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'USD millions':<34}" + "".join(f"FY{year}E{'':>8}" for year in YEARS))
    for label, values in rows:
        print(f"{label:<34}" + "".join(f"{value:>12,.1f}" for value in values))


def main():
    prior, model = opening.copy(), []
    for i, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1 + revenue_growth[i])
        gross_profit = revenue * gross_margin[i]
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

    values = lambda key: [year[key] for year in model]
    print_table("Income Statement", [
        ("Revenue", values("revenue")), ("Cost of revenue", values("cost_of_revenue")),
        ("Gross profit", values("gross_profit")), ("R&D", values("rd")), ("SG&A", values("sga")),
        ("Depreciation & amortization", values("depreciation")), ("Operating income", values("operating_income")),
        ("Interest expense", values("interest")), ("Pretax income", values("pretax_income")),
        ("Tax", values("tax")), ("Net income", values("net_income")),
    ])
    print_table("Balance Sheet", [
        ("Cash", values("cash")), ("Marketable securities", values("marketable_securities")),
        ("Accounts receivable", values("receivables")), ("Inventory", values("inventory")),
        ("Prepaids", values("prepaids")), ("PP&E", values("ppe")),
        ("Other non-cash assets", values("other_non_cash_assets")), ("Total assets", values("assets")),
        ("Accounts payable", values("accounts_payable")), ("Accrued liabilities", values("accrued_liabilities")),
        ("Debt", values("debt")), ("Revolver", values("revolver")), ("Other liabilities", values("other_liabilities")),
        ("Total liabilities", values("liabilities")), ("Shareholders' equity", values("equity")),
        ("Total liabilities + equity", [m["liabilities"] + m["equity"] for m in model]),
    ])
    print_table("Cash Flow and Checks", [
        ("Net income", values("net_income")), ("Depreciation & amortization", values("depreciation")),
        ("Capital spending", [-x for x in capex]), ("Change in operating NWC", [-x for x in values("operating_nwc_change")]),
        ("Free cash flow to equity", values("fcfe")), ("Shareholder returns", [-x for x in values("shareholder_returns")]),
        ("Assets - liabilities - equity", values("balance_gap")),
        ("Cash at or above minimum", [m["cash"] - minimum_cash for m in model]),
    ])
    pv_fcfe = sum(m["fcfe"] / (1 + cost_of_equity) ** (i + 1) for i, m in enumerate(model))
    terminal_value = model[-1]["fcfe"] * (1 + terminal_growth) / (cost_of_equity - terminal_growth)
    equity_value = pv_fcfe + terminal_value / (1 + cost_of_equity) ** len(YEARS)
    print(f"\nEquity value: ${equity_value:,.2f} million")
    print(f"Value per share: ${equity_value / shares_outstanding:,.2f}")


if __name__ == "__main__":
    main()
