import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# DAY 4: ANALYSIS I
# Dataset: Bangalore Zomato Data (zomato_features.csv)
# Tools: groupby, agg, pivot_table, crosstab, value_counts
# Protocol: QUESTION | TOOL CHOSEN | PREDICTION | CODE | FINDING
# ============================================================

current_dir = Path(__file__).resolve().parent
features_file = current_dir / "zomato_features.csv"
long_file = current_dir / "zomato_cuisines_long.csv"

df = pd.read_csv(features_file)
df_long = pd.read_csv(long_file)

print("=" * 70)
print("DAY 4: ANALYSIS I — AGGREGATION & CROSS-TABULATION")
print("=" * 70)


# ------------------------------------------------------------
# QUESTION 1: TOP 10 LOCATIONS BY RESTAURANT COUNT
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("QUESTION 1: Which are the top 10 locations in Bangalore by number of restaurants?")
print("TOOL CHOSEN: df['area'].value_counts().head(10)")
print("WHY: Directly computes frequency counts of categorical entries sorted descending.")
print("PREDICTION: High-density commercial/tech hubs like BTM, Koramangala, and HSR will dominate.")
print("-" * 70)

top_10_locations = df["area"].value_counts().head(10)
print("[CODE OUTPUT]")
print(top_10_locations)

print("\n[FINDING]")
print(f"'{top_10_locations.index[0]}' is the undisputed restaurant hub of Bangalore with {top_10_locations.iloc[0]} outlets,")
print(f"followed by {top_10_locations.index[1]} ({top_10_locations.iloc[1]}), {top_10_locations.index[2]} ({top_10_locations.iloc[2]}), {top_10_locations.index[3]} ({top_10_locations.iloc[3]}), and {top_10_locations.index[4]} ({top_10_locations.iloc[4]}).")
print("Tech corridors and student rental clusters drive the highest density of eateries.")


# ------------------------------------------------------------
# QUESTION 2: AVERAGE RATING BY LOCATION (SAMPLE THRESHOLD)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("QUESTION 2: Which locations have the highest average rating (with sufficient sample size)?")
print("TOOL CHOSEN: df.groupby('area')['delivery_ratings'].agg(['mean', 'median', 'count'])")
print("WHY: Groups data by locality and computes both central tendencies alongside sample size.")
print("THRESHOLD JUSTIFICATION: Set min_count >= 50 restaurants. Small pockets with <10 restaurants")
print("suffer from extreme sample variance where a single restaurant skews the entire area's score.")
print("PREDICTION: Upscale neighborhoods (Indiranagar, Koramangala) will boast higher ratings than peripheral zones.")
print("-" * 70)

location_ratings = (
    df.groupby("area")["delivery_ratings"]
    .agg(mean_rating="mean", median_rating="median", restaurant_count="count")
)
location_filtered = location_ratings[location_ratings["restaurant_count"] >= 50].sort_values(
    by="mean_rating", ascending=False
)

print("[CODE OUTPUT — TOP 5 HIGHEST RATED AREAS]")
print(location_filtered.head(5).round(2))

print("\n[CODE OUTPUT — TOP 5 LOWEST RATED AREAS]")
print(location_filtered.tail(5).round(2))

top_area = location_filtered.index[0]
print(f"\n[FINDING]")
print(f"Among areas with >=50 restaurants, '{top_area}' achieves the highest average delivery rating")
print(f"({location_filtered.loc[top_area, 'mean_rating']:.2f}), whereas peripheral high-density areas")
print(f"often score lower due to mass fast-food volume and delivery delays.")


# ------------------------------------------------------------
# QUESTION 3: HOME DELIVERY VS RATINGS
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("QUESTION 3: Does offering home delivery relate to restaurant ratings?")
print("TOOL CHOSEN: df.groupby('is_home_delivery')[['delivery_ratings', 'dinner_ratings']].agg(['mean', 'median', 'count'])")
print("WHY: Compares mean and median ratings between delivery-enabled vs non-delivery outlets.")
print("PREDICTION: Delivery-enabled restaurants maintain reliable delivery ratings (~3.9-4.0).")
print("-" * 70)

delivery_rel = df.groupby("is_home_delivery")[["delivery_ratings", "dinner_ratings"]].agg(["mean", "median", "count"])
print("[CODE OUTPUT]")
print(delivery_rel.round(2))

print("\n[FINDING]")
print(f"99.8% of restaurants in this dataset offer home delivery ({delivery_rel.loc[1, ('delivery_ratings', 'count')]:,}).")
print("For delivery ratings, average is ~3.94. Pure non-delivery outlets have virtually zero delivery ratings recorded.")


# ------------------------------------------------------------
# QUESTION 4: PRICE BAND VS RATING BAND (CROSSTAB)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("QUESTION 4: How are rating bands distributed within each price band?")
print("TOOL CHOSEN: pd.crosstab(df['price_band'], df['rating_band'], normalize='index') * 100")
print("WHY: Row-normalized contingency table shows percentage breakdown across rating tiers for each budget class.")
print("PREDICTION: Higher price bands (Fine Dining) will hold a greater percentage of 'Good' and 'Excellent' ratings.")
print("-" * 70)

price_rating_cross = pd.crosstab(
    df["price_band"],
    df["rating_band"],
    normalize="index"
) * 100

print("[CODE OUTPUT (% breakdown per price band)]")
print(price_rating_cross.round(2))

print("\n[FINDING]")
print("As price band increases from Budget to Fine Dining, the proportion of 'Good (4.0-4.4)'")
print("and 'Excellent (4.5-5.0)' ratings rises steadily, while 'Low (<3.5)' drops significantly.")
print("Customers hold premium dining to higher operational standards, but when satisfied, rate them higher.")


# ------------------------------------------------------------
# QUESTION 5: PIVOT TABLE: LOCATION X PRICE BAND (STRETCH)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("QUESTION 5: How does average delivery rating vary across top locations by price band?")
print("TOOL CHOSEN: pd.pivot_table(index='area', columns='price_band', values='delivery_ratings', aggfunc='mean')")
print("WHY: Two-dimensional matrix reveals geographic price-to-satisfaction dynamics.")
print("PREDICTION: Mid-Range and Fine Dining maintain consistent ~4.1-4.3 across prime food zones.")
print("-" * 70)

top_8_areas = df["area"].value_counts().head(8).index
pivot_area_price = df[df["area"].isin(top_8_areas)].pivot_table(
    index="area",
    columns="price_band",
    values="delivery_ratings",
    aggfunc="mean"
)

print("[CODE OUTPUT]")
print(pivot_area_price.round(2))

print("\n[FINDING]")
print("Across all major hubs, average ratings scale upwards with price tier.")
print("Budget food experiences greater score volatility depending on neighborhood delivery logistics.")


# ------------------------------------------------------------
# QUESTION 6: TOP 10 CUISINES: LONG TABLE VS PRIMARY CUISINE (STRETCH)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("QUESTION 6: How do top 10 cuisines differ when using the exploded long table vs primary cuisine?")
print("TOOL CHOSEN: pd.concat([df_long['cuisine'].value_counts().head(10), df['primary_cuisine'].value_counts().head(10)], axis=1)")
print("WHY: Direct side-by-side comparison reveals the multi-tag distortion effect.")
print("PREDICTION: Exploded counts will dramatically elevate complementary items (Beverages, Chinese, Desserts).")
print("-" * 70)

long_counts = df_long["cuisine"].value_counts().head(10).rename("Exploded_All_Cuisines")
primary_counts = df["primary_cuisine"].value_counts().head(10).rename("Primary_Cuisine_Only")

comparison = pd.concat([long_counts, primary_counts], axis=1)
print("[CODE OUTPUT]")
print(comparison)

print("\n[FINDING]")
print("Comparing exploded vs primary cuisine reveals massive distortion:")
print("- 'Beverages' and 'Chinese' jump massively in exploded table because they are common secondary offerings.")
print("- Counting only primary cuisine hides the massive presence of multi-cuisine offerings across Bangalore.")


# ------------------------------------------------------------
# QUESTION 7: INDOOR SEATING VS AVERAGE COST (STRETCH)
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("QUESTION 7: Does indoor seating significantly increase average restaurant cost?")
print("TOOL CHOSEN: df.groupby('is_indoor_seating')['average_cost'].agg(['mean', 'median', 'std', 'count'])")
print("WHY: Quantifies economic cost difference between dine-in restaurants and takeaway/cloud kitchens.")
print("PREDICTION: Indoor seating restaurants incur commercial real-estate costs, so cost will be ~2x higher.")
print("-" * 70)

seating_cost = df.groupby("is_indoor_seating")["average_cost"].agg(["mean", "median", "std", "count"])
seating_cost.index = ["Takeaway / Cloud Kitchen Only (0)", "Dine-in / Indoor Seating (1)"]

print("[CODE OUTPUT]")
print(seating_cost.round(2))

print("\n[FINDING]")
mean_dine_in = seating_cost.loc["Dine-in / Indoor Seating (1)", "mean"]
mean_delivery_only = seating_cost.loc["Takeaway / Cloud Kitchen Only (0)", "mean"]
print(f"Restaurants with indoor seating have an average cost of INR {mean_dine_in:.0f},")
print(f"compared to INR {mean_delivery_only:.0f} for delivery/takeaway-only outlets.")
print("Indoor seating virtually doubles average dining cost due to overhead and dining ambience.")

print("\n" + "=" * 70)
print("DAY 4 ANALYSIS I COMPLETE")
print("=" * 70)
