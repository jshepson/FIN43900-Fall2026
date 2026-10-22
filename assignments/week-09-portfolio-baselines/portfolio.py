"""Price simple Meridian portfolio baselines from editable classroom inputs.

Run: python portfolio.py
All returns, volatilities, and weights are decimal values (0.035 means 3.5%).
"""

import csv
from itertools import product
from math import sqrt
from statistics import correlation, mean, stdev


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


def find_lowest_risk_mix(
    sleeves: dict,
    correlations: dict,
    objective_return: float,
    reserve_eligible: set,
    reserve_minimum: float = 0.03,
    step: float = 0.05,
) -> dict | None:
    """Return the lowest-volatility feasible long-only mix on a fixed grid.

    The returned dictionary contains weights, expected_return, volatility, and
    reserve_weight.  ``None`` means no grid portfolio satisfies both rules.
    """
    validate_correlations(sleeves, correlations)
    if not sleeves:
        raise ValueError("At least one sleeve is required.")
    if not 0 < step <= 1 or round(1 / step) * step != 1:
        raise ValueError("Step must divide 100% exactly (for example, 0.05).")
    if not reserve_eligible <= set(sleeves):
        raise ValueError("Reserve-eligible sleeves must be in the sleeve universe.")

    units = round(1 / step)
    names = list(sleeves)
    covariances = covariance_matrix(sleeves, correlations)
    best = None
    # A grid point is an integer number of step-sized units.  The last sleeve
    # receives the remainder, which guarantees every candidate sums to 100%.
    for partial in product(range(units + 1), repeat=len(names) - 1):
        remainder = units - sum(partial)
        if remainder < 0:
            continue
        weights = {
            name: unit * step
            for name, unit in zip(names, (*partial, remainder))
        }
        expected_return = portfolio_return(weights, sleeves)
        reserve_weight = reserve_eligible_weight(weights, reserve_eligible)
        if expected_return + 1e-12 < objective_return or reserve_weight + 1e-12 < reserve_minimum:
            continue
        volatility = portfolio_volatility(weights, covariances)
        candidate = {
            "weights": weights,
            "expected_return": expected_return,
            "volatility": volatility,
            "reserve_weight": reserve_weight,
        }
        if best is None or volatility < best["volatility"] - 1e-12:
            best = candidate
    return best


def estimate_from_prices(source, last_36: bool = False) -> tuple[dict, dict]:
    """Estimate annualized sleeve inputs from a date-first monthly-price CSV.

    Returns are simple monthly returns.  Means are annualized by multiplying by
    12, sample standard deviations by multiplying by sqrt(12), and correlations
    are calculated from the same monthly-return observations.  Set ``last_36``
    to use only the latest 36 return observations.
    """
    close_after_read = False
    if isinstance(source, (str, bytes)):
        source = open(source, newline="", encoding="utf-8")
        close_after_read = True
    try:
        rows = list(csv.reader(source))
    finally:
        if close_after_read:
            source.close()
    if len(rows) < 3 or len(rows[0]) < 2:
        raise ValueError("CSV needs a date column, one or more ticker columns, and at least three rows.")

    names = [name.strip() for name in rows[0][1:]]
    if not all(names) or len(set(names)) != len(names):
        raise ValueError("Ticker column names must be present and unique.")
    prices = {name: [] for name in names}
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(names) + 1:
            raise ValueError(f"Row {row_number} does not have the same number of columns as the header.")
        try:
            values = [float(value) for value in row[1:]]
        except ValueError as error:
            raise ValueError(f"Row {row_number} contains a non-numeric price.") from error
        if any(value <= 0 for value in values):
            raise ValueError(f"Row {row_number} contains a price that is not positive.")
        for name, value in zip(names, values):
            prices[name].append(value)

    returns = {
        name: [(current / previous) - 1 for previous, current in zip(values, values[1:])]
        for name, values in prices.items()
    }
    if last_36:
        returns = {name: values[-36:] for name, values in returns.items()}
    observations = len(next(iter(returns.values())))
    if observations < 2:
        raise ValueError("At least three monthly prices (two monthly returns) are required.")

    sleeves = {
        name: {"return": mean(values) * 12, "volatility": stdev(values) * sqrt(12)}
        for name, values in returns.items()
    }
    correlations = {
        left: {
            right: 1.0 if left == right else correlation(returns[left], returns[right])
            for right in names
        }
        for left in names
    }
    validate_correlations(sleeves, correlations)
    return sleeves, correlations


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
