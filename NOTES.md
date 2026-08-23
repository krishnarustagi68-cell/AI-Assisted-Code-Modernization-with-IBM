# What I checked, and what the agent got wrong

## What the agent got wrong

The agent initially suggested that `km_to_miles` multiplied by 1.609, which is the number of
kilometres in a mile — not miles per kilometre. Using 1.609 makes 100 km show as 160.9 miles,
which is obviously wrong (100 km ≈ 62.1 miles). The constant name `MILES_PER_KM` was misleading:
the value stored was actually `KM_PER_MILE`. I caught this by running `verify.py` and seeing
the mileage conversion check fail, then checking the arithmetic by hand.

The agent also needed careful direction on how to handle a car with no `last_service_km`. Its
first instinct was to treat a missing reading as zero (the original default), but that falsely
flags the car as worn. A missing reading means "we don't know", not "it was serviced at 0 km",
so the correct action is to skip the car.

## What I checked before I accepted its work

1. I ran `pytest` and confirmed all 4 tests pass (2 in test_km_wachter, 2 in test_fleet_report).
2. I ran `python verify.py` and confirmed all 11 checks pass.
3. I manually checked that `SERVICE_INTERVAL_KM` is still 15000, `WARN_AT_PERCENT` is still 80,
   and `settings.cfg` has not been modified.
4. I verified the wear calculation by hand: 14900/15000 = 0.9933, × 100 = 99.33%, which is ≥ 80%
   so the car is correctly flagged.
5. I confirmed that `km_to_miles(100)` now returns ≈ 62.14, which is correct.

## What the data actually said

The obvious-looking predictors — total mileage (`odometer_km`) and car age (`age_years`) — turn
out to have almost zero difference between cars that broke down and those that did not. Their
means are nearly identical (53,448 vs 53,302 for mileage; 5.88 vs 5.89 for age).

The factors that actually predict breakdowns are:
- **km_since_service** (mean 11,678 for broke-down vs 7,261 for survived — 61% higher)
- **avg_daily_km** (mean 160 vs 131 — 22% higher)
- **load_factor** (mean 0.60 vs 0.51 — 19% higher)

In short: it is not old or high-mileage cars that break down, it is cars that are driven hard
(high daily km), loaded heavily, and overdue for service. The risk score combines these three
factors and clearly separates the two groups.
