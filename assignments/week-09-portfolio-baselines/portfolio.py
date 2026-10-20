"""Price simple Meridian portfolio baselines from editable classroom inputs.

Run: python portfolio.py
All returns, volatilities, and weights are decimal values (0.035 means 3.5%).
"""

from math import sqrt


# Editable inputs
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00, "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05, "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10, "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80, "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05, "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00, "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00, "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25, "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def validate_correlations(sleeves: dict, correlations: dict) -> None:
    """Raise ValueError if the correlation table has missing, invalid, or asymmetric entries."""
    names = set(sleeves)
    if set(correlations) != names:
        raise ValueError("Correlation table rows must match the sleeve names.")
    for left in sleeves:
        if set(correlations[left]) != names:
            raise ValueError(f"Correlation row for {left} must contain every sleeve.")
        for right in sleeves:
            value = correlations[left][right]
            if not -1 <= value <= 1:
                raise ValueError(
                    f"Invalid correlation for {left} / {right}: {value}. "
                    "Correlations must be between -1 and 1."
                )
            if value != correlations[right][left]:
                raise ValueError(
                    f"Correlation table is not symmetric: {left} / {right} differs "
                    f"from {right} / {left}."
                )


def covariance_matrix(sleeves: dict, correlations: dict) -> dict:
    """Return covariance[i][j] = correlation[i][j] * volatility[i] * volatility[j]."""
    return {
        left: {
            right: correlations[left][right]
            * sleeves[left]["volatility"]
            * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def equal_weight_portfolio(sleeves: dict) -> dict:
    """Return weights that allocate equally across all sleeves."""
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_portfolio(sleeves: dict) -> dict:
    """Return weights proportional to 1 / volatility, normalized to sum to one."""
    inverse_volatilities = {name: 1 / data["volatility"] for name, data in sleeves.items()}
    total_inverse_volatility = sum(inverse_volatilities.values())
    return {name: value / total_inverse_volatility for name, value in inverse_volatilities.items()}


def portfolio_return(weights: dict, sleeves: dict) -> float:
    """Calculate the weighted expected return."""
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_variance(weights: dict, covariances: dict) -> float:
    """Calculate w-transpose times covariance times w, including every covariance term."""
    return sum(
        weights[left] * covariances[left][right] * weights[right]
        for left in weights
        for right in weights
    )


def portfolio_volatility(weights: dict, covariances: dict) -> float:
    """Calculate portfolio volatility as the square root of portfolio variance."""
    return sqrt(portfolio_variance(weights, covariances))


def reserve_eligible_weight(weights: dict, reserve_eligible: set) -> float:
    """Calculate the combined weight of reserve-eligible sleeves."""
    return sum(weights[name] for name in reserve_eligible)


def print_portfolio(name: str, weights: dict, sleeves: dict, covariances: dict) -> None:
    """Print the requested baseline results from calculated values."""
    ordered_weights = " / ".join(f"{weights[sleeve] * 100:.1f}" for sleeve in sleeves)
    expected_return = portfolio_return(weights, sleeves)
    volatility = portfolio_volatility(weights, covariances)
    reserve_weight = reserve_eligible_weight(weights, RESERVE_ELIGIBLE)
    meets_objective = "yes" if expected_return >= OBJECTIVE_RETURN else "no"

    print(name)
    print(f"  Weights (bills / 10-year / IG / equity): {ordered_weights}%")
    print(f"  Expected return: {expected_return * 100:.2f}%")
    print(f"  Volatility: {volatility * 100:.2f}%")
    print(f"  Reserve-eligible: {reserve_weight * 100:.1f}%")
    print(f"  Meets {OBJECTIVE_RETURN * 100:.1f}% objective: {meets_objective}")


def main() -> None:
    validate_correlations(SLEEVES, CORRELATIONS)
    covariances = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": {
            "Treasury bills": 0.0, "Treasury 10-year note": 0.0,
            "Investment-grade bond fund": 0.4, "Global equity index fund": 0.6,
        },
        "Equal weight": equal_weight_portfolio(SLEEVES),
        "Inverse volatility": inverse_volatility_portfolio(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariances)


if __name__ == "__main__":
    main()
