"""FIN 43900 — Discounted Cash Flow (DCF) Model.

Inputs, cash flow projections, Gordon-growth terminal value, and enterprise-to-equity bridge.
Uses only Python's standard library.
"""

import sys

# ==============================================================================
# INPUT BLOCK (Edit assumptions here)
# ==============================================================================
STARTING_FCFF: float = 96895.8470  # USD millions (FY2026 FCFF; see NVIDIA_DCF.md)
GROWTH_RATES: list[float] = [0.70, 0.40, 0.25, 0.15, 0.08]  # Years 1 to 5
WACC: float = 0.10  # Weighted Average Cost of Capital (10%)
TERMINAL_GROWTH: float = 0.03  # Long-term perpetual growth rate (3%)
NON_OPERATING_CASH: float = 62556.0  # USD millions, Jan. 25, 2026
DEBT: float = 8468.0  # USD millions, Jan. 25, 2026 carrying amount
DILUTED_SHARES: float = 24514.0  # Millions of diluted weighted-average shares

# Sensitivity and reverse-DCF settings (edit these, not the calculation code)
SENSITIVITY_WACCS: list[float] = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTHS: list[float] = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE: float = 223.67  # USD; Sep. 9, 2026 closing price
REVERSE_SHIFT_LOWER: float = -0.05  # percentage points expressed as decimals
REVERSE_SHIFT_UPPER: float = 0.10
# ==============================================================================


def calculate_dcf() -> None:
    # 1. Boundary & Validity Checks
    if TERMINAL_GROWTH >= WACC:
        sys.exit(
            f"Error: Terminal growth rate ({TERMINAL_GROWTH:.4f}) must be strictly less than "
            f"WACC ({WACC:.4f}). When terminal growth >= WACC, the Gordon Growth Model denominator "
            f"(WACC - g) is non-positive, implying infinite or undefined value."
        )

    if DILUTED_SHARES <= 0:
        sys.exit(f"Error: Diluted shares must be positive. Provided: {DILUTED_SHARES}")

    if len(GROWTH_RATES) != 5:
        sys.exit(f"Error: Exactly 5 growth rates are required. Provided: {len(GROWTH_RATES)}")

    # 2. Project Explicit FCFF for Years 1 to 5
    fcff_projections: list[float] = []
    current_fcff = STARTING_FCFF
    for g in GROWTH_RATES:
        current_fcff *= (1.0 + g)
        fcff_projections.append(current_fcff)

    # 3. Discount Explicit FCFF to Present Value
    pv_explicit_list: list[float] = []
    for t, fcff in enumerate(fcff_projections, start=1):
        pv = fcff / ((1.0 + WACC) ** t)
        pv_explicit_list.append(pv)

    pv_explicit_fcff = sum(pv_explicit_list)

    # 4. Gordon Growth Terminal Value at End of Year 5
    # Year 6 FCFF = Year 5 FCFF * (1 + g_terminal)
    fcff_year_5 = fcff_projections[-1]
    terminal_value_year_5 = (fcff_year_5 * (1.0 + TERMINAL_GROWTH)) / (WACC - TERMINAL_GROWTH)

    # 5. Discount Terminal Value 5 Years to Present
    pv_terminal_value = terminal_value_year_5 / ((1.0 + WACC) ** 5)

    # 6. Enterprise Value and Enterprise-to-Equity Bridge
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_diluted_share = equity_value / DILUTED_SHARES

    # 7. Terminal Value Share of Enterprise Value
    terminal_value_share = pv_terminal_value / enterprise_value

    # 8. Print Twelve Labelled Lines to 4 Decimals
    for t, fcff in enumerate(fcff_projections, start=1):
        print(f"FCFF Year {t}: {fcff:.4f}")
    print(f"PV of explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal value, Year 5: {terminal_value_year_5:.4f}")
    print(f"PV of terminal value: {pv_terminal_value:.4f}")
    print(f"Enterprise value: {enterprise_value:.4f}")
    print(f"Equity value: {equity_value:.4f}")
    print(f"Value per share: {value_per_diluted_share:.4f}")
    print(f"PV of TV ÷ enterprise value: {terminal_value_share:.4f} ({terminal_value_share * 100:.2f}%)")


def value_per_share(
    starting_fcff: float, growth_rates: list[float], wacc: float,
    terminal_growth: float, cash: float, debt: float, diluted_shares: float,
) -> float:
    """Return DCF value per diluted share without printing it."""
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be strictly less than WACC.")
    fcff = starting_fcff
    projected_fcff: list[float] = []
    for growth_rate in growth_rates:
        fcff *= 1.0 + growth_rate
        projected_fcff.append(fcff)
    pv_explicit = sum(
        cash_flow / ((1.0 + wacc) ** year)
        for year, cash_flow in enumerate(projected_fcff, start=1)
    )
    terminal_value = projected_fcff[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    enterprise_value = pv_explicit + terminal_value / ((1.0 + wacc) ** len(projected_fcff))
    return (enterprise_value + cash - debt) / diluted_shares


def print_sensitivity_grid() -> None:
    """Print per-share values across the editable WACC and terminal-growth lists."""
    header = "WACC \\ terminal growth".ljust(24) + "".join(
        f"{growth:>10.1%}" for growth in SENSITIVITY_TERMINAL_GROWTHS
    )
    print("\nSensitivity grid: value per diluted share ($)")
    print(header)
    for wacc in SENSITIVITY_WACCS:
        row = f"{wacc:.1%}".ljust(24)
        for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
            cell = "invalid" if terminal_growth >= wacc else (
                f"{value_per_share(STARTING_FCFF, GROWTH_RATES, wacc, terminal_growth, NON_OPERATING_CASH, DEBT, DILUTED_SHARES):.2f}"
            )
            row += f"{cell:>10}"
        print(row)


def print_reverse_dcf() -> None:
    """Solve a uniform shift to all five explicit growth rates by bisection."""
    print("\nReverse DCF: uniform shift to all five explicit growth rates")
    print(f"Target price: ${TARGET_SHARE_PRICE:.2f}")
    print("Held fixed: starting FCFF, WACC, terminal growth, cash, debt, diluted shares; only the five explicit growth rates shift together.")
    if REVERSE_SHIFT_LOWER >= REVERSE_SHIFT_UPPER:
        print("No solution: lower bound must be less than upper bound.")
        return
    if min(growth + REVERSE_SHIFT_LOWER for growth in GROWTH_RATES) <= -1.0 or min(growth + REVERSE_SHIFT_UPPER for growth in GROWTH_RATES) <= -1.0:
        print("No solution: this bracket pushes an annual growth rate to -100% or below.")
        return

    def price_for_shift(shift: float) -> float:
        return value_per_share(STARTING_FCFF, [growth + shift for growth in GROWTH_RATES], WACC, TERMINAL_GROWTH, NON_OPERATING_CASH, DEBT, DILUTED_SHARES)

    lower, upper = REVERSE_SHIFT_LOWER, REVERSE_SHIFT_UPPER
    lower_difference = price_for_shift(lower) - TARGET_SHARE_PRICE
    upper_difference = price_for_shift(upper) - TARGET_SHARE_PRICE
    if lower_difference == 0:
        solved_shift = lower
    elif upper_difference == 0:
        solved_shift = upper
    elif lower_difference * upper_difference > 0:
        print(f"No solution in bracket [{lower:+.2%}, {upper:+.2%}]: prices span ${price_for_shift(lower):.2f} to ${price_for_shift(upper):.2f}.")
        return
    else:
        for _ in range(100):
            midpoint = (lower + upper) / 2.0
            midpoint_difference = price_for_shift(midpoint) - TARGET_SHARE_PRICE
            if abs(midpoint_difference) < 0.000001:
                break
            if lower_difference * midpoint_difference <= 0:
                upper = midpoint
            else:
                lower = midpoint
                lower_difference = midpoint_difference
        solved_shift = midpoint
    print(f"Solved uniform growth-rate shift: {solved_shift:+.4%}")
    print(f"Shifted explicit growth rates: {[f'{growth + solved_shift:.2%}' for growth in GROWTH_RATES]}")


if __name__ == "__main__":
    calculate_dcf()
    print_sensitivity_grid()
    print_reverse_dcf()
