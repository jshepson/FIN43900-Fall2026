"""Check the Meridian Foundation Reserve mandate's computable rules.

Run: python mandate.py
All weights and limits below are percentages of the portfolio unless noted.
"""

# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": "none", "redeem_days": 0, "reserve_eligible": True},
    "Treasury bills": {
        "issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True
    },
    "Global equity index fund": {
        "issuer": "diversified fund", "redeem_days": 2, "reserve_eligible": False
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund", "redeem_days": 3, "reserve_eligible": False
    },
    "Private real estate fund": {
        "issuer": "diversified fund", "redeem_days": 90, "reserve_eligible": False
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp", "redeem_days": 4, "reserve_eligible": False
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp", "redeem_days": 1, "reserve_eligible": False
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # Attack portfolio: it passes the checkable rules but may not meet S2's return objective.
    "D": {
        "Cash": 100, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 0, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90
ISSUER_LIMIT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def status(value: float, passes: bool) -> str:
    return f"{value:.1f} {'pass' if passes else 'FAIL'}"


def weight_if(weights: dict[str, float], condition) -> float:
    return sum(weight for holding, weight in weights.items() if condition(HOLDINGS[holding]))


def largest_company_weight(weights: dict[str, float]) -> float:
    issuer_weights: dict[str, float] = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            issuer_weights[issuer] = issuer_weights.get(issuer, 0) + weight
    return max(issuer_weights.values(), default=0.0)


def check_candidate(name: str, weights: dict[str, float], reserve_minimum: float) -> None:
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = weight_if(weights, lambda holding: holding["reserve_eligible"])
    liquid_weight = weight_if(
        weights, lambda holding: holding["redeem_days"] <= LIQUIDITY_WINDOW_DAYS
    )
    largest_company = largest_company_weight(weights)

    checks = [
        ("Weights sum to 100", total_weight, abs(total_weight - 100) < 1e-9),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0),
        (f"Reserve >= {reserve_minimum:.1f}%", reserve_weight, reserve_weight >= reserve_minimum),
        (
            f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days >= {MINIMUM_LIQUID_SHARE:.1f}%",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUID_SHARE,
        ),
        (f"Largest single company <= {ISSUER_LIMIT:.1f}%", largest_company, largest_company <= ISSUER_LIMIT),
    ]
    failures = 0

    print(f"\nCandidate {name}")
    for label, value, passes in checks:
        print(f"{label}: {status(value, passes)}")
        failures += not passes
    print("Calendar-year loss: requires CIO clarification")
    if failures == 0:
        print("Verdict: passes every checkable rule")
    else:
        print(f"Verdict: fails {failures} rule(s)")


def main() -> None:
    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {reserve_minimum:.1f}% of the portfolio")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
