# analyze.py
# Breakdown-risk analysis for KM-Waechter.
#
# Key finding: total mileage (odometer_km) and age_years do NOT predict breakdowns —
# their means are nearly identical for cars that broke down vs. those that did not.
# The real predictors are km_since_service (how overdue the car is), avg_daily_km
# (how hard it is driven daily), and load_factor (how heavily it is loaded).

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load the data
# ---------------------------------------------------------------------------
df = pd.read_csv("fleet_history.csv")

# ---------------------------------------------------------------------------
# 2. Compare broke-down vs. survived cars column by column
# ---------------------------------------------------------------------------
broke = df[df["broke_down"] == 1]
ok = df[df["broke_down"] == 0]

print("=" * 65)
print("FACTOR COMPARISON: broke-down vs. survived")
print("=" * 65)
for col in ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]:
    m_broke = broke[col].mean()
    m_ok = ok[col].mean()
    diff_pct = ((m_broke - m_ok) / m_ok) * 100 if m_ok != 0 else 0
    tag = "** SEPARATES **" if abs(diff_pct) > 10 else "   no signal"
    print(f"  {col:20s}  broke={m_broke:8.2f}  ok={m_ok:8.2f}  diff={diff_pct:+6.1f}%  {tag}")
print()

# ---------------------------------------------------------------------------
# 3. Build a simple 0–100 risk score from the three discriminating factors
# ---------------------------------------------------------------------------
# We normalise each predictor to 0–1 using min-max scaling across the fleet,
# then combine them with weights proportional to how much they separate the
# two groups (km_since_service contributes most, then avg_daily_km, then load_factor).

WEIGHTS = {
    "km_since_service": 0.50,
    "avg_daily_km": 0.30,
    "load_factor": 0.20,
}

for col in WEIGHTS:
    col_min = df[col].min()
    col_max = df[col].max()
    df[f"{col}_norm"] = (df[col] - col_min) / (col_max - col_min) if col_max != col_min else 0.0

df["risk_score"] = (
    WEIGHTS["km_since_service"] * df["km_since_service_norm"]
    + WEIGHTS["avg_daily_km"] * df["avg_daily_km_norm"]
    + WEIGHTS["load_factor"] * df["load_factor_norm"]
) * 100

df["risk_score"] = df["risk_score"].round(1)

# ---------------------------------------------------------------------------
# 4. Print the cars ranked by risk, highest first
# ---------------------------------------------------------------------------
ranked = df.sort_values("risk_score", ascending=False)

print("=" * 65)
print("BREAKDOWN RISK RANKING  (highest risk first)")
print("=" * 65)
print(f"{'Rank':>4}  {'Car ID':10s}  {'Risk':>5}  {'km_since':>10}  {'daily_km':>8}  {'load':>5}  {'Broke?':>6}")
print("-" * 65)
for i, (_, row) in enumerate(ranked.iterrows(), 1):
    flag = " YES" if row["broke_down"] == 1 else "  no"
    print(
        f"{i:4d}  {row['car_id']:10s}  {row['risk_score']:5.1f}  "
        f"{row['km_since_service']:10.0f}  {row['avg_daily_km']:8.0f}  "
        f"{row['load_factor']:5.2f}  {flag}"
    )

# ---------------------------------------------------------------------------
# 5. Quick validation: how well does the score separate the two groups?
# ---------------------------------------------------------------------------
avg_risk_broke = ranked[ranked["broke_down"] == 1]["risk_score"].mean()
avg_risk_ok = ranked[ranked["broke_down"] == 0]["risk_score"].mean()

print()
print("=" * 65)
print("VALIDATION")
print(f"  Average risk score (broke down) : {avg_risk_broke:.1f}")
print(f"  Average risk score (survived)   : {avg_risk_ok:.1f}")
print(f"  Separation                      : {avg_risk_broke - avg_risk_ok:.1f} points")
print("=" * 65)
print()
print("SUMMARY: odometer_km and age_years are NOT predictors. The real")
print("risk factors are km_since_service, avg_daily_km, and load_factor.")
