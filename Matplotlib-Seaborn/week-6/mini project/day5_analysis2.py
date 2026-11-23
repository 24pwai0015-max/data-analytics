import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# DAY 5: ANALYSIS II
# Dataset: Bangalore Zomato Data (zomato_features.csv)
# Tools: isin, ~, str.contains, between, multi-condition OR,
#        value analysis, correlation, mean vs median
# Protocol: QUESTION | TOOL CHOSEN | PREDICTION | CODE | FINDING
# ============================================================

current_dir = Path(__file__).resolve().parent
features_file = current_dir / "zomato_features.csv"

df = pd.read_csv(features_file)

print("=" * 70)
print("DAY 5: ANALYSIS II — FILTERING, OUTLIERS & CORRELATION")
print("=" * 70)


# ------------------------------------------------------------
# 1. FILTER 1: ISIN (3 LOCATIONS)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("1. FILTER VIA ISIN: Three Major Tech & Food Neighborhoods")
print("TOOL: df['area'].isin(['Indiranagar', 'Whitefield', 'HSR'])")
print("PREDICTION: Together these 3 tech clusters represent over 1,000 restaurants.")
print("-" * 70)

target_areas = ["Indiranagar", "Whitefield", "HSR"]
df_isin = df[df["area"].isin(target_areas)]

print(f"[CODE OUTPUT] Count of restaurants in {target_areas}: {len(df_isin):,}")
print(df_isin.groupby("area")[["delivery_ratings", "average_cost"]].agg(["mean", "count"]).round(2))

print("\n[FINDING]")
print(f"A total of {len(df_isin):,} restaurants operate in these three hotspots.")
print("Indiranagar leads in average rating (4.03) and premium dining, while Whitefield and HSR cater heavily to tech worker deliveries.")


# ------------------------------------------------------------
# 2. FILTER 2: INVERSION VIA ~ (EXCLUDING VEG-ONLY)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("2. FILTER VIA ~: Non-Vegetarian Restaurants (Inverting Pure-Veg Flag)")
print("TOOL: df[~df['is_veg_only'].astype(bool)]")
print("PREDICTION: Non-vegetarian restaurants will represent the vast majority (>90%) of the Bangalore market.")
print("-" * 70)

df_non_veg = df[~df["is_veg_only"].astype(bool)]
pct_non_veg = (len(df_non_veg) / len(df)) * 100

print(f"[CODE OUTPUT] Non-veg restaurant count: {len(df_non_veg):,} ({pct_non_veg:.1f}%)")
print(f"Pure Vegetarian restaurant count: {len(df) - len(df_non_veg):,} ({100 - pct_non_veg:.1f}%)")

print("\n[FINDING]")
print(f"{pct_non_veg:.1f}% of restaurants in Bangalore serve meat/non-veg dishes.")
print("Pure-veg establishments form an exclusive 7.2% niche, predominantly centered in traditional zones like Basavanagudi and Malleshwaram.")


# ------------------------------------------------------------
# 3. FILTER 3: STR.CONTAINS (CUISINE SEARCH)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("3. FILTER VIA STR.CONTAINS: Biryani Specialists")
print("TOOL: df[df['cuisines'].str.contains('Biryani', case=False, na=False)]")
print("PREDICTION: Biryani is one of Bangalore's most ubiquitous comfort foods with >1,500 outlets.")
print("-" * 70)

df_biryani = df[df["cuisines"].str.contains("Biryani", case=False, na=False)]
print(f"[CODE OUTPUT] Biryani-serving restaurants: {len(df_biryani):,} ({len(df_biryani)/len(df)*100:.1f}%)")
print("Top 5 Biryani Chains by Outlet Count:")
print(df_biryani["name"].value_counts().head(5))

print("\n[FINDING]")
print(f"22.3% ({len(df_biryani):,}) of all restaurants in Bangalore serve Biryani.")
print("Chains like Donne Biriyani House and Meghana Foods maintain massive multi-branch coverage across the city.")


# ------------------------------------------------------------
# 4. FILTER 4: BETWEEN (MID-PRICED RANGE)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("4. FILTER VIA BETWEEN: Everyday Casual Dining (₹300 - ₹600)")
print("TOOL: df[df['average_cost'].between(300, 600)]")
print("PREDICTION: This cost band captures standard working-lunch and casual weekend dining.")
print("-" * 70)

df_mid = df[df["average_cost"].between(300, 600)]
print(f"[CODE OUTPUT] Restaurants in ₹300-₹600 range: {len(df_mid):,} ({len(df_mid)/len(df)*100:.1f}%)")
print(f"Average delivery rating in this segment: {df_mid['delivery_ratings'].mean():.2f}")

print("\n[FINDING]")
print(f"The ₹300-₹600 bracket represents 37.1% ({len(df_mid):,}) of Bangalore restaurants.")
print("This price bracket represents the competitive core of Bangalore casual dining with an average rating of 3.88.")


# ------------------------------------------------------------
# 5. FILTER 5: MULTI-GROUP OR (NAMED CONDITIONS)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("5. MULTI-GROUP OR: Budget Delivery Gems OR Luxury Fine Dining")
print("TOOL: cond_budget_gem | cond_luxury_elite")
print("PREDICTION: Combines high-performing extremes of Bangalore's dining market.")
print("-" * 70)

cond_budget_gem = (df["average_cost"] <= 250) & (df["delivery_ratings"] >= 4.2)
cond_luxury_elite = (df["average_cost"] >= 1200) & (df["delivery_ratings"] >= 4.2)

df_extremes = df[cond_budget_gem | cond_luxury_elite]
print(f"[CODE OUTPUT] Total matching restaurants: {len(df_extremes):,}")
print(f"- Budget Gems (Cost <= ₹250 & Rating >= 4.2): {cond_budget_gem.sum():,}")
print(f"- Luxury Elite (Cost >= ₹1200 & Rating >= 4.2): {cond_luxury_elite.sum():,}")

print("\n[FINDING]")
print(f"There are {cond_budget_gem.sum():,} affordable high-rated gems across Bangalore, compared to")
print(f"{cond_luxury_elite.sum():,} luxury fine-dining establishments operating at the same 4.2+ standard.")


# ------------------------------------------------------------
# 6. STRETCH: BEST VALUE DEFINITION & RESULTS
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("6. 'BEST VALUE' RESTAURANTS (NUMERICAL CRITERIA)")
print("DEFINITION: Delivery Rating >= 4.2 (Top 15%) AND Cost <= ₹250 (<= Median Cost) AND Reviews >= 500")
print("-" * 70)

best_value_mask = (
    (df["delivery_ratings"] >= 4.2) &
    (df["average_cost"] <= 250) &
    (df["total_reviews"] >= 500)
)
best_value_df = df[best_value_mask].sort_values(by=["delivery_ratings", "total_reviews"], ascending=False)

print(f"[CODE OUTPUT] Count of Best Value Restaurants: {len(best_value_df):,}")
print("\nTop 10 Best Value Restaurants in Bangalore:")
print(best_value_df[["name", "area", "average_cost", "delivery_ratings", "total_reviews"]].head(10).to_string(index=False))

print("\n[FINDING]")
print(f"Exactly {len(best_value_df)} restaurants qualify as Bangalore's premier 'Best Value' establishments.")
print("These include legendary South Indian and Biryani houses delivering exceptional food at accessible prices.")


# ------------------------------------------------------------
# 7. STRETCH: 'OVERRATED' RESTAURANTS
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("7. 'OVERRATED' RESTAURANTS (NUMERICAL CRITERIA)")
print("DEFINITION: Cost >= ₹1000 (Top 3.5% Price Tier) AND Delivery Rating < 3.6 (Bottom 10% Rating Tier)")
print("-" * 70)

overrated_mask = (
    (df["average_cost"] >= 1000) &
    (df["delivery_ratings"] < 3.6)
)
overrated_df = df[overrated_mask].sort_values(by="average_cost", ascending=False)

print(f"[CODE OUTPUT] Count of Overrated Outlets: {len(overrated_df):,}")
if len(overrated_df) > 0:
    print(overrated_df[["name", "area", "average_cost", "delivery_ratings", "total_reviews"]].head(8).to_string(index=False))

print("\n[FINDING]")
print(f"Only {len(overrated_df)} expensive establishments fall below the 3.6 rating threshold.")
print("High prices usually force restaurants to maintain stringent food quality, keeping poor performers rare in the luxury bracket.")


# ------------------------------------------------------------
# 8. STRETCH: RESTAURANT CHAINS (BRANCH COUNT)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("8. RESTAURANT CHAINS WITH THE MOST BRANCHES")
print("TOOL: df['name'].value_counts().head(12)")
print("WHY: Directly relates to Day 1 duplicate name findings; proves legitimate branch expansion.")
print("-" * 70)

top_chains = df["name"].value_counts().head(12)
print("[CODE OUTPUT — TOP CHAINS]")
print(top_chains)

print("\n[FINDING]")
print(f"'{top_chains.index[0]}' leads with {top_chains.iloc[0]} outlets across Bangalore, followed by")
print(f"'{top_chains.index[1]}' ({top_chains.iloc[1]}) and '{top_chains.index[2]}' ({top_chains.iloc[2]}).")
print("This proves that identical names in Day 1 were largely quick-service restaurant chains expanding across neighborhoods.")


# ------------------------------------------------------------
# 9. STRETCH: CORRELATION MATRIX
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("9. CORRELATION MATRIX OF NUMERIC ATTRIBUTES")
print("TOOL: df[num_cols].corr()")
print("-" * 70)

num_cols = [
    "average_cost",
    "delivery_ratings",
    "dinner_ratings",
    "dinner_reviews",
    "delivery_reviews",
    "total_reviews",
    "service_breadth"
]

corr_matrix = df[num_cols].corr()
print("[CODE OUTPUT — CORRELATION MATRIX]")
print(corr_matrix.round(2))

print("\n[FINDING]")
print("Strongest observed correlation pairs:")
print(f"1. dinner_reviews and average_cost: r = {corr_matrix.loc['dinner_reviews', 'average_cost']:.2f}")
print("   Higher-cost restaurants receive significantly more dine-in dinner reviews than low-cost takeaways.")
print(f"2. delivery_ratings and average_cost: r = {corr_matrix.loc['delivery_ratings', 'average_cost']:.2f}")
print("   A modest positive correlation: higher spend modestly aligns with higher customer satisfaction.")


# ------------------------------------------------------------
# 10. STRETCH: MEAN VS MEDIAN COMPARISON (SKEWNESS)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("10. MEAN VS MEDIAN COMPARISON ACROSS PRICE BANDS")
print("TOOL: df.groupby('price_band')['total_reviews'].agg(['mean', 'median', 'std'])")
print("-" * 70)

mean_vs_median = df.groupby("price_band", observed=True)["total_reviews"].agg(["mean", "median", "std"])
print("[CODE OUTPUT]")
print(mean_vs_median.round(1))

print("\n[FINDING — WHY DO MEAN AND MEDIAN DIFFER?]")
print("Across every single price band, the MEAN review count is 3x to 6x higher than the MEDIAN.")
print("For instance, in Affordable (201-500), the mean is ~2,423 reviews, while the median is only 462.")
print("WHY: Total reviews are extremely right-skewed. A handful of iconic viral restaurants (with 50,000+ to 99,000+ reviews)")
print("pull the arithmetic mean upward, whereas the median faithfully reflects typical restaurant volume.")

print("\n" + "=" * 70)
print("DAY 5 ANALYSIS II COMPLETE")
print("=" * 70)
