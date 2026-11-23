import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# DAY 1: DATA INSPECTION AND EXPLORATORY DATA ANALYSIS
# Dataset: Bangalore Zomato Data
# Purpose: Read-only inspection; understand structure, nulls,
#          duplicates, and data types before touching the data.
# ============================================================

current_dir = Path(__file__).resolve().parent
file_path = current_dir / "BangaloreZomatoData.csv"

# ------------------------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------------------------

print("=" * 70)
print("DAY 1: DATA INSPECTION (READ-ONLY)")
print("=" * 70)

print("\n[PREDICTION]")
print("I expect a dataset containing restaurant information,")
print("including names, cuisines, ratings, reviews, address, and cost.")

df = pd.read_csv(file_path)

print("\n[FINDING]")
print(f"Dataset loaded successfully from: {file_path.name}")
print(f"Rows: {df.shape[0]:,}, Columns: {df.shape[1]}")

print("\n--- Column Names ---")
print(df.columns.tolist())

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- DataFrame Info ---")
df.info()

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Last 5 Rows ---")
print(df.tail())

print("\n--- Random 5 Sample Rows ---")
print(df.sample(5, random_state=42))


# ------------------------------------------------------------
# 2. MISSING VALUES ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MISSING VALUES ANALYSIS")
print("=" * 70)

print("\n[PREDICTION]")
print("I expect text fields and optional tags (such as opening timings,")
print("known-for tags, and popular dishes) to contain significant missing values.")

missing_count = df.isnull().sum()
missing_percentage = (df.isnull().sum() / len(df)) * 100

missing_table = pd.DataFrame({
    "Missing_Count": missing_count,
    "Missing_Percentage": missing_percentage.round(2)
}).sort_values(by="Missing_Percentage", ascending=False)

print("\n[FINDING: Missing Values Table]")
print(missing_table)

print("\nInterpretation:")
print(f"- KnownFor: {missing_table.loc['KnownFor', 'Missing_Count']:,} missing ({missing_table.loc['KnownFor', 'Missing_Percentage']}%)")
print(f"- PopularDishes: {missing_table.loc['PopularDishes', 'Missing_Count']:,} missing ({missing_table.loc['PopularDishes', 'Missing_Percentage']}%)")
print(f"- PeopleKnownFor: {missing_table.loc['PeopleKnownFor', 'Missing_Count']:,} missing ({missing_table.loc['PeopleKnownFor', 'Missing_Percentage']}%)")
print(f"- Timing: {missing_table.loc['Timing', 'Missing_Count']:,} missing ({missing_table.loc['Timing', 'Missing_Percentage']}%)")
print("- The remaining 15 columns contain 0 pandas null values (though placeholders like '-' exist).")


# ------------------------------------------------------------
# 3. DATA DICTIONARY
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATA DICTIONARY")
print("=" * 70)

data_dictionary = {
    "Name": (
        "Restaurant name",
        "Text / Identifier",
        "Different outlets share the same name (chains)"
    ),
    "URL": (
        "Restaurant webpage URL",
        "Identifier / URL",
        "Unique web link for each restaurant page"
    ),
    "Cuisines": (
        "Cuisines offered by the restaurant",
        "Multi-value Text",
        "Comma-separated list; needs splitting and explosion"
    ),
    "Area": (
        "Area or locality of the restaurant",
        "Category",
        "Contains city suffix like ', Bangalore'; needs cleaning"
    ),
    "Timing": (
        "Restaurant opening and closing timings",
        "Text",
        "34.78% missing values; irregular unstructured text"
    ),
    "Full_Address": (
        "Full restaurant address",
        "Text",
        "Detailed physical location; key for deduplication"
    ),
    "PhoneNumber": (
        "Restaurant contact number",
        "Identifier / Text",
        "Contains '-' placeholders; not a mathematical number"
    ),
    "IsHomeDelivery": (
        "Home delivery availability",
        "Binary Flag (0/1)",
        "Boolean-like indicator (1 = Yes, 0 = No)"
    ),
    "isTakeaway": (
        "Takeaway availability",
        "Binary Flag (0/1)",
        "Boolean-like indicator (1 = Yes, 0 = No)"
    ),
    "isIndoorSeating": (
        "Indoor seating availability",
        "Binary Flag (0/1)",
        "Boolean-like indicator (1 = Yes, 0 = No)"
    ),
    "isVegOnly": (
        "Whether the restaurant is vegetarian-only",
        "Binary Flag (0/1)",
        "Boolean-like indicator (1 = Yes, 0 = No)"
    ),
    "Dinner Ratings": (
        "Dinner rating (out of 5.0)",
        "Numeric-like Text",
        "Stored as object; contains 5,325 '-' placeholders"
    ),
    "Dinner Reviews": (
        "Number of dinner reviews",
        "Integer",
        "Heavily right-skewed; many 0s"
    ),
    "Delivery Ratings": (
        "Delivery rating (out of 5.0)",
        "Numeric-like Text",
        "Stored as object; contains 1,131 '-' placeholders"
    ),
    "Delivery Reviews": (
        "Number of delivery reviews",
        "Integer",
        "Heavily right-skewed; primary activity metric"
    ),
    "KnownFor": (
        "Highlights the restaurant is known for",
        "Text",
        "97.11% missing; very sparse"
    ),
    "PopularDishes": (
        "Signature popular dishes",
        "Text / Multi-value",
        "82.80% missing; sparse free-text"
    ),
    "PeopleKnownFor": (
        "Customer impressions and ambience keywords",
        "Text",
        "60.95% missing"
    ),
    "AverageCost": (
        "Average cost for two people in INR",
        "Integer",
        "Numeric; ranges from 50 to 4,200 INR"
    )
}

dict_df = pd.DataFrame(data_dictionary, index=["Meaning", "Category", "Suspected_Problem"]).T
dict_csv_path = current_dir / "data_dictionary.csv"
dict_df.to_csv(dict_csv_path)
print(f"[FINDING] Data dictionary exported to: {dict_csv_path.name}")
print(dict_df)


# ------------------------------------------------------------
# 4. DUPLICATE ANALYSIS (THREE WAYS)
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DUPLICATE ANALYSIS (THREE WAYS)")
print("=" * 70)

# (a) Fully identical rows
print("\n(a) Fully Identical Duplicate Rows:")
print("[PREDICTION] Expect 0 or very few completely identical rows.")
full_dups = df.duplicated().sum()
print(f"[FINDING] Fully identical duplicate count: {full_dups}")

# (b) Same Restaurant Name
print("\n(b) Same Restaurant Name:")
print("[PREDICTION] Restaurant chains have multiple branches across Bangalore.")
repeated_names_count = df["Name"].duplicated().sum()
distinct_repeated_names = df.loc[df["Name"].duplicated(keep=False), "Name"].nunique()
print(f"[FINDING] Repeated Name occurrences: {repeated_names_count:,}")
print(f"[FINDING] Distinct restaurant names appearing more than once: {distinct_repeated_names:,}")
print("\nTop 10 Most Frequent Restaurant Names (Chains):")
print(df["Name"].value_counts().head(10))

# (c) Same Name + Full Address
print("\n(c) Same Name + Full Address (True Duplicates):")
print("[PREDICTION] Should be near 0; identical name + exact address represents duplicate scrapings.")
name_address_dups = df.duplicated(subset=["Name", "Full_Address"]).sum()
print(f"[FINDING] Same Name + Full Address duplicate count: {name_address_dups}")
if name_address_dups > 0:
    print(df[df.duplicated(subset=["Name", "Full_Address"], keep=False)][["Name", "Area", "Full_Address", "AverageCost"]])


# ------------------------------------------------------------
# 5. NUMERIC-LIKE COLUMN INSPECTION
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NUMERIC-LIKE COLUMN INSPECTION")
print("=" * 70)

num_cols_to_inspect = [
    "Dinner Ratings",
    "Delivery Ratings",
    "Dinner Reviews",
    "Delivery Reviews",
    "AverageCost"
]

for col in num_cols_to_inspect:
    print(f"\n--- Column: {col} ---")
    print(f"Dtype: {df[col].dtype} | Non-null count: {df[col].count():,}")
    print("Top 5 value counts:")
    print(df[col].value_counts().head(5))
    
    # Check for placeholder values like '-'
    if df[col].dtype == "object":
        coerced = pd.to_numeric(df[col], errors="coerce")
        bad_mask = coerced.isna() & df[col].notna()
        print(f"Non-numeric placeholder count: {bad_mask.sum():,} ({bad_mask.sum()/len(df)*100:.1f}%)")
        print("Non-numeric unique values:", df.loc[bad_mask, col].unique())


# ------------------------------------------------------------
# 6. SUMMARY STATISTICS & TEXT WHITESPACE CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NUMERIC AND CATEGORICAL SUMMARY (STRETCH)")
print("=" * 70)

print("\nNumeric Summary:")
print(df.describe())

print("\nCategorical Summary:")
print(df.describe(include="object"))

# Check for leading/trailing whitespace
text_cols = df.select_dtypes(include="object").columns
whitespace_issues = {}
for col in text_cols:
    has_spaces = (df[col].astype(str) != df[col].astype(str).str.strip()).sum()
    if has_spaces > 0:
        whitespace_issues[col] = has_spaces

print("\nLeading / Trailing Whitespace Counts in Text Columns:")
print(whitespace_issues if whitespace_issues else "No leading/trailing spaces found.")


# ------------------------------------------------------------
# 7. TOP 8 POTENTIAL DATA-QUALITY PROBLEMS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 8 POTENTIAL DATA-QUALITY PROBLEMS")
print("=" * 70)

problems = """
1. Dinner Ratings is stored as text with 5,325 '-' placeholders (59.68% unrated).
   Impact: Critical. Cannot compute means, correlations, or distributions without cleaning.

2. Delivery Ratings is stored as text with 1,131 '-' placeholders (12.67% unrated).
   Impact: High. Must convert '-' to NaN for accurate mathematical operations.

3. KnownFor has 97.11% missing values (8,665 nulls).
   Impact: Extreme column sparsity; cannot be used for broad statistical modeling.

4. PopularDishes has 82.80% missing values (7,388 nulls).
   Impact: High sparsity; dish analysis must be restricted to populated subsets.

5. PeopleKnownFor has 60.95% missing values (5,439 nulls).
   Impact: Moderate-to-high sparsity; limited usability for customer sentiment.

6. Timing has 34.78% missing values (3,103 nulls) and unstructured format.
   Impact: Moderate; must be handled without dropping entire rows.

7. Cuisines is a comma-separated multi-value string.
   Impact: Counting distinct cuisines directly distorts frequencies without exploding.

8. Two identical restaurant scrapings share the exact Name and Full_Address.
   Impact: Minor duplicate distortion (2 rows); must be deduplicated in Stage 1.
"""

print(problems)

print("\n" + "=" * 70)
print("DAY 1 INSPECTION COMPLETE — NO DATA MODIFIED")
print("=" * 70)
