"""FIN 43900 Lab 07: P/E comparable-company valuation.

Edit only the INPUTS section.  This exercise uses equity values per share, so it
does not add cash or subtract debt.
"""

from statistics import median


# =============================================================================
# INPUTS (edit these values for a different case)
# =============================================================================
TARGET = {
    "ticker": "ABG",
    "name": "Asbury Automotive",
    "price": 243.03,
    "diluted_eps": 21.50,
}

PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "diluted_eps": 16.92},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "diluted_eps": 36.81},
]
# =============================================================================


def number_is_positive(value: object) -> bool:
    """Return True only for a supplied positive numeric value."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def label(company: dict[str, object]) -> str:
    return f"{company.get('ticker', 'Unknown')} ({company.get('name', 'Unnamed company')})"


def valid_multiple(company: dict[str, object]) -> tuple[bool, float | None, str | None]:
    """Validate one peer and return its P/E or an explanation."""
    price = company.get("price")
    eps = company.get("diluted_eps")
    if not number_is_positive(price):
        return False, None, "price is missing or nonpositive; P/E is not meaningful"
    if not number_is_positive(eps):
        return False, None, "diluted EPS is missing or nonpositive; P/E is not meaningful"
    return True, float(price) / float(eps), None


def implied_price(pe_multiple: float, target_eps: object) -> float | None:
    """Apply a peer P/E to target EPS only when target EPS is usable."""
    if not number_is_positive(target_eps):
        return None
    return pe_multiple * float(target_eps)


def print_estimate(title: str, pe_multiple: float, target_eps: object) -> float | None:
    estimate = implied_price(pe_multiple, target_eps)
    if estimate is None:
        print(f"{title}: not meaningful (target diluted EPS is missing or nonpositive)")
    else:
        print(f"{title}: ${estimate:.2f}")
    return estimate


def usable_peers(target: dict[str, object], candidates: list[dict[str, object]]) -> list[tuple[dict[str, object], float]]:
    """Deduplicate by ticker, exclude target, and retain peers with meaningful P/E."""
    target_ticker = str(target.get("ticker", "")).upper()
    seen: set[str] = set()
    usable: list[tuple[dict[str, object], float]] = []

    print("Peer screening")
    for candidate in candidates:
        ticker = str(candidate.get("ticker", "")).upper()
        identity = ticker or label(candidate)
        if ticker == target_ticker:
            print(f"- {label(candidate)}: excluded (the target cannot be its own peer)")
            continue
        if identity in seen:
            print(f"- {label(candidate)}: excluded (duplicate peer)")
            continue
        seen.add(identity)
        is_valid, pe_multiple, problem = valid_multiple(candidate)
        if not is_valid:
            print(f"- {label(candidate)}: {problem}")
            continue
        print(f"- {label(candidate)} P/E: {pe_multiple:.6f}x")
        usable.append((candidate, pe_multiple))
    return usable


def print_leave_one_out(peers: list[tuple[dict[str, object], float]], full_median: float, target_eps: object) -> None:
    """Show the median implied price after removing each valid peer."""
    print("\nLeave-one-out check")
    full_estimate = implied_price(full_median, target_eps)
    for removed_company, _ in peers:
        remaining = [multiple for company, multiple in peers if company is not removed_company]
        if not remaining:
            print(f"Remove {removed_company.get('ticker', 'peer')}: no estimate (no usable peers remain)")
            continue
        remaining_estimate = implied_price(median(remaining), target_eps)
        if remaining_estimate is None or full_estimate is None:
            print(f"Remove {removed_company.get('ticker', 'peer')}: not meaningful (target diluted EPS is missing or nonpositive)")
            continue
        change = remaining_estimate - full_estimate
        print(
            f"Remove {removed_company.get('ticker', 'peer')}: remaining median-implied price "
            f"${remaining_estimate:.2f}; change from full-peer estimate ${change:+.2f}"
        )


def main() -> None:
    print(f"Target: {label(TARGET)}")
    if not number_is_positive(TARGET.get("price")):
        print("Target observed price: not meaningful (price is missing or nonpositive)")
    else:
        print(f"Target observed price: ${float(TARGET['price']):.2f}")

    peers = usable_peers(TARGET, PEERS)
    if not peers:
        print("\nValuation: no usable peers.")
        return

    multiples = [multiple for _, multiple in peers]
    minimum, midpoint, maximum = min(multiples), median(multiples), max(multiples)
    print(f"\nUsable peers: {len(peers)}")
    print(f"Peer minimum P/E: {minimum:.6f}x")
    print(f"Peer median P/E: {midpoint:.6f}x")
    print(f"Peer maximum P/E: {maximum:.6f}x")

    if len(peers) == 1:
        print("One valid peer: this is a reference estimate, not a range.")
        print_estimate("Reference implied price", midpoint, TARGET.get("diluted_eps"))
    else:
        low = print_estimate("Minimum-P/E implied price", minimum, TARGET.get("diluted_eps"))
        middle = print_estimate("Median-P/E implied price", midpoint, TARGET.get("diluted_eps"))
        high = print_estimate("Maximum-P/E implied price", maximum, TARGET.get("diluted_eps"))
        if low is not None and high is not None:
            print(f"Peer-implied range: ${low:.2f}-${high:.2f}")
        if middle is None:
            print("Peer-implied range: not meaningful (target diluted EPS is missing or nonpositive)")

    print_leave_one_out(peers, midpoint, TARGET.get("diluted_eps"))


if __name__ == "__main__":
    main()
