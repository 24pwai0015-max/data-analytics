"""DAY 7 - VERIFY FINDINGS (read-only).
Recomputes the numbers behind each of the 8 findings, straight from the data.
Run it, put the output next to FINDINGS.md, and fix every line that disagrees.
"""
import pandas as pd
from pathlib import Path

here = Path(__file__).resolve().parent
df = pd.read_csv(here / "zomato_features.csv")
long = pd.read_csv(here / "zomato_cuisines_long.csv")

order = ["Budget (<=200)", "Affordable (201-500)",
         "Mid-Range (501-1000)", "Fine Dining (>1000)"]
df["price_band"] = pd.Categorical(df["price_band"], categories=order, ordered=True)

print("=" * 70)
print("DAY 7: VERIFICATION AUDIT — RECOMPUTING ALL 8 FINDINGS")
print("=" * 70)
print("TOTAL ROWS:", len(df))

print("\nF1  Top 5 areas by restaurant count:")
print(df["area"].value_counts().head(5))

print("\nF2  Areas with >= 50 restaurants: best delivery ratings")
print("    (look at n and std: is the gap between #1 and #2 bigger than the noise?)")
g = df.groupby("area")["delivery_ratings"].agg(mean="mean", std="std", n="count")
print(g[g["n"] >= 50].sort_values("mean", ascending=False).head(5).round(3))

print("\nF3  Price band share (%)")
print((df["price_band"].value_counts(normalize=True, sort=False) * 100).round(1))

print("\nF4  Cost by indoor seating")
c = df.groupby("is_indoor_seating")["average_cost"].agg(["mean", "median", "count"]).round(1)
print(c)
print("    mean ratio (seating / no seating):", round(c.loc[1, "mean"] / c.loc[0, "mean"], 2))

print("\nF5  Top 6 cuisines (exploded: outlets offering the cuisine)")
print(long["cuisine"].value_counts().head(6))

print("\nF6  Veg-only share (%) and home-delivery share (%)")
print("    veg-only:", round(df["is_veg_only"].mean() * 100, 1),
      "| home delivery:", round(df["is_home_delivery"].mean() * 100, 1))

print("\nF7  Is price decoupled from rating? Compare BASE RATES, not raw counts")
rated = df.dropna(subset=["delivery_ratings"])
share_42 = rated.groupby("price_band", observed=True)["delivery_ratings"].apply(
    lambda s: (s >= 4.2).mean() * 100)
print("    % of rated restaurants with rating >= 4.2, by price band:")
print(share_42.round(1))
print("    count cost<=250 and rating>=4.2:",
      ((rated["average_cost"] <= 250) & (rated["delivery_ratings"] >= 4.2)).sum())
print("    count cost<=300 and rating>=4.2:",
      ((rated["average_cost"] <= 300) & (rated["delivery_ratings"] >= 4.2)).sum())
print("    Spearman correlation, cost vs rating:",
      round(rated["average_cost"].corr(rated["delivery_ratings"], method="spearman"), 3))

print("\nF8  Mean vs median of total_reviews by price band")
r = df.groupby("price_band", observed=True)["total_reviews"].agg(["mean", "median"])
r["mean_over_median"] = (r["mean"] / r["median"]).round(1)
print(r.round(1))
print("=" * 70)
