import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# DAY 3: CLEANING II AND FEATURE ENGINEERING
# Dataset: Bangalore Zomato Data (zomato_stage1.csv)
# Purpose: Engineer multi-value columns, price/rating/popularity
#          bands, long cuisine table, and IQR outlier detection.
# ============================================================

current_dir = Path(__file__).resolve().parent
input_file = current_dir / "zomato_stage1.csv"
features_output = current_dir / "zomato_features.csv"
cuisines_long_output = current_dir / "zomato_cuisines_long.csv"

print("=" * 70)
print("DAY 3: FEATURE ENGINEERING")
print("=" * 70)

# Load Stage 1 cleaned data
df = pd.read_csv(input_file)
print(f"Loaded {len(df):,} rows from {input_file.name}")


# ------------------------------------------------------------
# STEP 1: MULTI-VALUE CUISINE FEATURE ENGINEERING
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 1: MULTI-VALUE CUISINE FEATURES")
print("-" * 70)

# DECISION:
# Split the comma-separated 'cuisines' string:
# 1. 'n_cuisines': integer count of cuisines offered.
# 2. 'primary_cuisine': the first listed cuisine (primary specialty).

df["cuisines_list"] = df["cuisines"].astype(str).str.split(r",\s*")
df["n_cuisines"] = df["cuisines_list"].apply(len)
df["primary_cuisine"] = df["cuisines_list"].apply(lambda x: x[0] if len(x) > 0 else "Unknown")

print("n_cuisines distribution:")
print(df["n_cuisines"].value_counts().sort_index())
print("\nTop 10 Primary Cuisines:")
print(df["primary_cuisine"].value_counts().head(10))


# ------------------------------------------------------------
# STEP 2: PRICE BANDS (PD.CUT)
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 2: PRICE BANDS")
print("-" * 70)

# DECISION & REASONING FOR BIN EDGES:
# Cost distribution quartiles:
# Min: 50 | 25%: 150 | Median: 250 | 75%: 400 | Max: 4200
# We define 4 logical consumer dining tiers:
# - Budget (<= 200 INR): Street food, tea stalls, quick daily meals.
# - Affordable (201 - 500 INR): Casual dining, small family eateries.
# - Mid-Range (501 - 1000 INR): Upscale casual dining, trendy cafes, bistros.
# - Fine Dining (> 1000 INR): Luxury dining, 5-star hotels, gourmet bars.

cost_bins = [0, 200, 500, 1000, 10000]
cost_labels = [
    "Budget (<=200)",
    "Affordable (201-500)",
    "Mid-Range (501-1000)",
    "Fine Dining (>1000)"
]

df["price_band"] = pd.cut(df["average_cost"], bins=cost_bins, labels=cost_labels)
print("Price Band Distribution:")
print(df["price_band"].value_counts(sort=False))


# ------------------------------------------------------------
# STEP 3: RATING BANDS
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 3: RATING BANDS")
print("-" * 70)

# DECISION:
# Delivery ratings represent the broadest available customer feedback (87% coverage).
# We categorize into 4 performance bands + 'Unrated' for missing ratings:
# - Low (< 3.5): Poor customer experience or operational issues.
# - Average (3.5 - 3.9): Standard satisfactory performance.
# - Good (4.0 - 4.4): High quality, popular choices.
# - Excellent (4.5 - 5.0): Top tier, elite culinary spots.

rating_bins = [0.0, 3.49, 3.99, 4.49, 5.0]
rating_labels = [
    "Low (<3.5)",
    "Average (3.5-3.9)",
    "Good (4.0-4.4)",
    "Excellent (4.5-5.0)"
]

df["rating_band"] = pd.cut(df["delivery_ratings"], bins=rating_bins, labels=rating_labels)
df["rating_band"] = df["rating_band"].astype(str).replace("nan", "Unrated")

print("Delivery Rating Band Distribution:")
print(df["rating_band"].value_counts())


# ------------------------------------------------------------
# STEP 4: POPULARITY BANDS FROM TOTAL REVIEWS
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 4: POPULARITY BANDS (TOTAL REVIEWS)")
print("-" * 70)

# Combine dinner and delivery reviews
df["total_reviews"] = df["dinner_reviews"] + df["delivery_reviews"]

# Popularity tiers based on review volume:
pop_bins = [-1, 50, 300, 1500, 1000000]
pop_labels = [
    "Low Activity (<=50)",
    "Moderate Activity (51-300)",
    "High Activity (301-1500)",
    "Viral / Iconic (>1500)"
]

df["popularity_band"] = pd.cut(df["total_reviews"], bins=pop_bins, labels=pop_labels)
print("Popularity Band Distribution:")
print(df["popularity_band"].value_counts(sort=False))


# ------------------------------------------------------------
# STEP 5: LONG CUISINE TABLE (STRETCH)
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 5: LONG CUISINE TABLE (EXPLODE)")
print("-" * 70)

# COMMENT: Why counting cuisines without explode gives wrong answers:
# If a restaurant offers "North Indian, Chinese, Continental", a simple value_counts()
# treats that composite string as an independent unique category. This fragments
# true cuisine demand and artificially hides the actual frequency of popular food styles.
# By exploding each cuisine to its own row, every individual cuisine receives accurate count.

cuisines_long = df[[
    "name", "area", "average_cost", "delivery_ratings",
    "is_veg_only", "is_home_delivery", "price_band", "cuisines_list"
]].copy()

cuisines_long = cuisines_long.explode("cuisines_list").rename(columns={"cuisines_list": "cuisine"})
cuisines_long["cuisine"] = cuisines_long["cuisine"].str.strip()

# Filter out empty or unknown cuisines
cuisines_long = cuisines_long[cuisines_long["cuisine"] != ""]

print(f"Exploded long cuisine table rows: {len(cuisines_long):,}")
print("Top 10 Cuisines in Bangalore (True Individual Counts):")
top_cuisines = cuisines_long["cuisine"].value_counts().head(10)
print(top_cuisines)

cuisines_long.to_csv(cuisines_long_output, index=False)
print(f"Saved long cuisine dataset to: {cuisines_long_output.name}")


# ------------------------------------------------------------
# STEP 6: OUTLIER DETECTION VIA IQR (COST & REVIEWS)
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 6: IQR OUTLIER DETECTION (COST & REVIEWS)")
print("-" * 70)

# IQR calculation for AverageCost:
q1_cost = df["average_cost"].quantile(0.25)
q3_cost = df["average_cost"].quantile(0.75)
iqr_cost = q3_cost - q1_cost
upper_cost_bound = q3_cost + 1.5 * iqr_cost
df["is_cost_outlier"] = df["average_cost"] > upper_cost_bound

# IQR calculation for Total Reviews:
q1_rev = df["total_reviews"].quantile(0.25)
q3_rev = df["total_reviews"].quantile(0.75)
iqr_rev = q3_rev - q1_rev
upper_rev_bound = q3_rev + 1.5 * iqr_rev
df["is_review_outlier"] = df["total_reviews"] > upper_rev_bound

# DECISION:
# KEEP the outliers! Do not drop or arbitrarily cap them.
# REASON:
# Cost outliers (> 775 INR) are genuine fine-dining establishments and luxury hotels.
# Review outliers (> 3,700 reviews) are real iconic Bangalore institutions (e.g. Meghana Foods).
# Dropping them would distort market reality and exclude Bangalore's most famous dining spots.

print(f"AverageCost IQR Bounds: Q1={q1_cost}, Q3={q3_cost}, Upper Threshold={upper_cost_bound}")
print(f"Cost Outliers Count: {df['is_cost_outlier'].sum():,} ({df['is_cost_outlier'].mean()*100:.1f}%)")

print(f"\nTotal Reviews IQR Bounds: Q1={q1_rev}, Q3={q3_rev}, Upper Threshold={upper_rev_bound}")
print(f"Review Outliers Count: {df['is_review_outlier'].sum():,} ({df['is_review_outlier'].mean()*100:.1f}%)")


# ------------------------------------------------------------
# STEP 7: CUSTOM FEATURE OF OWN INVENTION
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 7: CUSTOM FEATURE — SERVICE BREADTH SCORE")
print("-" * 70)

# FEATURE: 'service_breadth'
# Sum of available service channels: is_home_delivery + is_takeaway + is_indoor_seating (range: 1 to 3).
# ONE-LINE REASON:
# Measures the operational flexibility of the restaurant (1 = single-channel dark kitchen; 3 = full-service restaurant).

df["service_breadth"] = df["is_home_delivery"] + df["is_takeaway"] + df["is_indoor_seating"]
print("Service Breadth distribution:")
print(df["service_breadth"].value_counts().sort_index())

# Drop the temporary list column before saving
df = df.drop(columns=["cuisines_list"])

# Save engineered dataset
df.to_csv(features_output, index=False)
print("\n" + "=" * 70)
print(f"[SUCCESS] Feature-engineered dataset saved to: {features_output.name}")
print(f"Columns ({len(df.columns)}): {df.columns.tolist()}")
print("=" * 70)
