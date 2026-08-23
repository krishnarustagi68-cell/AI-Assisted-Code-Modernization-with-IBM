# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.

SERVICE_INTERVAL_KM: int = 15000
WARN_AT_PERCENT: int = 80


def wear_percent(km_since_service: int, interval: int) -> float:
    """Return the wear percentage (0–100+) for a given distance since last service."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True if the car is due for service based on wear percentage."""
    if "last_service_km" not in car:
        return False  # unknown service history — cannot determine wear
    km_since = car["odometer"] - car["last_service_km"]
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Check every car in the fleet and return a list of IDs that are due for service."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
