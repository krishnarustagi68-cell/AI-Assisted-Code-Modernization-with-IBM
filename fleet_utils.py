# fleet_utils.py
# Helper utilities for the Vossberg Mobility fleet service.

MILES_PER_KM: float = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a number to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a value as a whole-number percentage string."""
    return f"{value:.0f}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list of numbers, or 0 if empty."""
    if not values:
        return 0
    return sum(values) / len(values)
