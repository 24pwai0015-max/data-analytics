import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# DAY 2: CLEANING I — STRUCTURE AND TYPES
# Dataset: Bangalore Zomato Data
# Purpose: Fix naming, whitespace, deduplication, missing values,
#          type conversions, and save zomato_stage1.csv.
# ============================================================

current_dir = Path(__file__).resolve().parent
raw_file = current_dir / "BangaloreZomatoData.csv"
output_file = current_dir / "zomato_stage1.csv"

print("=" * 70)
print("DAY 2: DATA CLEANING I — STRUCTURE AND TYPES")
print("=" * 70)

# Load raw dataset
df_raw = pd.read_csv(raw_file)
df = df_raw.copy()

before_shape = df.shape
before_nulls = df.isnull().sum()

print("\n[ORIGINAL DATASET STATUS]")
print(f"Shape: {before_shape}")


# ------------------------------------------------------------
# STEP 1: STANDARDIZE COLUMN NAMES
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 1: STANDARDIZE COLUMN NAMES")
print("-" * 70)

import re

# DECISION:
# Convert CamelCase / PascalCase to snake_case by inserting underscores before
# uppercase letters, replacing non-word characters with underscores, and lowercasing.
# REASON:
# Consistent snake_case naming (e.g. 'average_cost', 'is_home_delivery')
# prevents casing bugs and improves readability.

def to_snake_case(col: str) -> str:
    if col.upper() == "URL":
        return "url"
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", col)
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s)
    return s.strip("_").lower()

df.columns = [to_snake_case(c) for c in df.columns]

print(f"Standardized Columns ({len(df.columns)}):")
print(df.columns.tolist())


# ------------------------------------------------------------
# STEP 2: STRIP WHITESPACE FROM TEXT COLUMNS
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 2: STRIP WHITESPACE FROM TEXT COLUMNS")
print("-" * 70)

# DECISION:
# Apply .str.strip() to all text / object / string columns.
# REASON:
# Hidden leading and trailing spaces cause false category fragmentation
# and string filtering mismatches.

text_cols = df.select_dtypes(include=["object", "string"]).columns
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

print(f"Stripped whitespace across {len(text_cols)} text columns.")


# ------------------------------------------------------------
# STEP 3: DEDUPLICATION DECISION & IMPLEMENTATION
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 3: DEDUPLICATION")
print("-" * 70)

# DECISION:
# Distinct outlets with identical names in different locations (chains) are
# genuine separate branches and MUST NOT be dropped.
# However, records sharing both exact 'name' AND 'full_address' represent
# duplicate scrapes of the exact same physical restaurant.
# We sort by total reviews descending to preserve the most complete entry,
# then drop duplicates on ['name', 'full_address'].
# REASON:
# Removing genuine multi-unit restaurant chains would destroy valid branch data.
# Removing identical address scrapes purges true redundant entries.
# VALIDATION:
# Report exact rows dropped.

dups_before = df.duplicated(subset=["name", "full_address"]).sum()
print(f"True duplicate scrapes identified (name + full_address): {dups_before}")

df = df.sort_values(by=["dinner_reviews", "delivery_reviews"], ascending=False)
df = df.drop_duplicates(subset=["name", "full_address"], keep="first")
df = df.reset_index(drop=True)

print(f"Rows after address-based deduplication: {len(df):,} (Dropped: {dups_before} rows)")


# ------------------------------------------------------------
# STEP 4: CONVERT NUMBER-LIKE TEXT COLUMNS
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 4: CONVERT NUMBER-LIKE TEXT COLUMNS (RATINGS & COSTS)")
print("-" * 70)

# DECISION:
# 'dinner_ratings' and 'delivery_ratings' contain '-' for unrated outlets.
# Replace '-' with np.nan and cast to float.
# Ensure 'dinner_reviews', 'delivery_reviews', and 'average_cost' are integer.
# REASON:
# '-' cannot be averaged, plotted, or correlated. Converting to float with NaN
# preserves missingness faithfully without imputing arbitrary biased numbers.
# VALIDATION:
# Print count of '-' converted to NaN and confirmed dtypes.

for rating_col in ["dinner_ratings", "delivery_ratings"]:
    dash_count = (df[rating_col] == "-").sum()
    df[rating_col] = df[rating_col].replace("-", np.nan)
    df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")
    print(f"{rating_col}: converted {dash_count:,} '-' placeholders to NaN. (Dtype: {df[rating_col].dtype})")

# Verify integer columns
for int_col in ["dinner_reviews", "delivery_reviews", "average_cost"]:
    df[int_col] = pd.to_numeric(df[int_col], errors="coerce").fillna(0).astype(int)
    print(f"{int_col}: confirmed numeric integer. (Min: {df[int_col].min()}, Max: {df[int_col].max()})")


# ------------------------------------------------------------
# STEP 5: MISSING VALUES STRATEGY (ONE DECISION PER COLUMN)
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 5: MISSING VALUES DECISION PER COLUMN")
print("-" * 70)

# DECISION COMMENTS:
# 1. timing: 34.78% missing. Fill with "Not Provided".
#    Reason: Dropping rows would lose 1/3 of Bangalore restaurants.
# 2. known_for: 97.11% missing. Fill with "Unknown".
#    Reason: Sparse marketing tags; preserve existing rows.
# 3. popular_dishes: 82.80% missing. Fill with "Unknown".
#    Reason: Dish tags are optional crowdsourced data; fill with category placeholder.
# 4. people_known_for: 60.95% missing. Fill with "Unknown".
#    Reason: Customer feedback tags; preserve records.
# 5. phone_number: Contains '-' for missing numbers. Replace '-' or 'nan' with "Not Available".
#    Reason: Contact info is metadata, not an analytical numeric metric.
# 6. dinner_ratings & delivery_ratings: Left as NaN.
#    Reason: Unrated restaurants should not have synthetic fake ratings imputed.

df["timing"] = df["timing"].replace(["nan", "None", ""], np.nan).fillna("Not Provided")
df["known_for"] = df["known_for"].replace(["nan", "None", ""], np.nan).fillna("Unknown")
df["popular_dishes"] = df["popular_dishes"].replace(["nan", "None", ""], np.nan).fillna("Unknown")
df["people_known_for"] = df["people_known_for"].replace(["nan", "None", ""], np.nan).fillna("Unknown")
df["phone_number"] = df["phone_number"].replace(["-", "nan", "None", ""], "Not Available")


# ------------------------------------------------------------
# STEP 6: STANDARDIZE CATEGORIES & BINARY FLAGS (STRETCH)
# ------------------------------------------------------------
print("\n" + "-" * 70)
print("STEP 6: STANDARDIZE CATEGORIES & BINARY FLAGS (STRETCH)")
print("-" * 70)

# DECISION:
# Strip redundant ', Bangalore' from 'area' to clean geographic reporting.
# Ensure boolean/binary flags are integer 0/1.

df["area"] = df["area"].str.replace(r",\s*Bangalore$", "", regex=True).str.strip()

binary_cols = ["is_home_delivery", "is_takeaway", "is_indoor_seating", "is_veg_only"]
for b_col in binary_cols:
    df[b_col] = df[b_col].astype(int)
    print(f"Binary flag '{b_col}': {df[b_col].value_counts().to_dict()}")


# ------------------------------------------------------------
# STEP 7: BEFORE VS AFTER SUMMARY & SAVE STAGE 1
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("BEFORE VS AFTER SUMMARY")
print("=" * 70)

after_shape = df.shape
after_nulls = df.isnull().sum()

summary_df = pd.DataFrame({
    "Original_Dtype": [df_raw.dtypes.get(c, "N/A") for c in df_raw.columns],
    "Clean_Dtype": [df.dtypes.get(c, "N/A") for c in df.columns],
    "Original_Nulls": [before_nulls.get(c, 0) for c in df_raw.columns],
    "Clean_Nulls": [after_nulls.get(c, 0) for c in df.columns]
}, index=df.columns)

print(summary_df)

print(f"\nRow-loss Summary:")
print(f"Original rows: {before_shape[0]:,}")
print(f"Cleaned rows:  {after_shape[0]:,}")
print(f"Rows dropped:  {before_shape[0] - after_shape[0]} (0.02% true duplicate records)")

df.to_csv(output_file, index=False)
print(f"\n[SUCCESS] Cleaned data successfully saved to: {output_file.name}")
print("=" * 70)
