import pandas as pd

# ============================================================
# DAY 1: DATA INSPECTION AND EXPLORATORY DATA ANALYSIS
# Dataset: Bangalore Zomato Data
# ============================================================

# ------------------------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------------------------

file_path = r"D:\4th sem summer\data analytics\Matplotlib-Seaborn\week-6\mini project\BangaloreZomatoData.csv"

df = pd.read_csv(file_path)

print("=" * 60)
print("DAY 1: DATA INSPECTION")
print("=" * 60)

print("\nPrediction:")
print("I expect a dataset containing restaurant information,")
print("including names, cuisines, ratings, reviews, and cost.")

print("\nActual finding:")
print("Dataset loaded successfully.")

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nDataset information:")
df.info()

print("\nFirst 5 rows:")
print(df.head())

print("\nLast 5 rows:")
print(df.tail())

print("\nRandom 5 rows:")
print(df.sample(5, random_state=42))


# ------------------------------------------------------------
# 2. MISSING VALUES ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES ANALYSIS")
print("=" * 60)

print("\nPrediction:")
print("I expect some restaurant information, such as timings")
print("and popular dishes, to be missing.")

# Count missing values
missing_count = df.isnull().sum()

# Calculate missing-value percentages
missing_percentage = (df.isnull().sum() / len(df)) * 100

# Combine results into one table
missing_table = pd.DataFrame({
    "Missing_Count": missing_count,
    "Missing_Percentage": missing_percentage.round(2)
})

# Sort from highest to lowest missing percentage
missing_table = missing_table.sort_values(
    by="Missing_Percentage",
    ascending=False
)

print("\nActual finding:")
print(missing_table)

print("\nInterpretation:")
print("KnownFor has 8,665 missing values (97.11%).")
print("PopularDishes has 7,388 missing values (82.80%).")
print("PeopleKnownFor has 5,439 missing values (60.95%).")
print("Timing has 3,103 missing values (34.78%).")
print("The other 15 columns have no pandas-recognized null values.")


# ------------------------------------------------------------
# 3. DATA DICTIONARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATA DICTIONARY")
print("=" * 60)

print("\nPrediction:")
print("I expect the dataset to contain identifiers, descriptive")
print("text, restaurant attributes, ratings, review counts, and cost.")

# Column: (Meaning, Data Category, Suspected Problem)

data_dictionary = {
    "Name": (
        "Restaurant name",
        "Text / Identifier",
        "Different restaurants may share the same name"
    ),

    "URL": (
        "Restaurant webpage URL",
        "Identifier / URL",
        "Check URL validity if required"
    ),

    "Cuisines": (
        "Cuisines offered by the restaurant",
        "Multi-value Text",
        "One restaurant may list multiple cuisines"
    ),

    "Area": (
        "Area or locality of the restaurant",
        "Category",
        "Check repeated names across different areas"
    ),

    "Timing": (
        "Restaurant opening and closing timings",
        "Text",
        "Many missing values; format may vary"
    ),

    "Full_Address": (
        "Full restaurant address",
        "Text",
        "Check formatting consistency if required"
    ),

    "PhoneNumber": (
        "Restaurant contact number",
        "Identifier / Text",
        "Check formatting; phone numbers are not quantities"
    ),

    "IsHomeDelivery": (
        "Home delivery availability",
        "Category / Boolean-like",
        "Inspect distinct values and consistency"
    ),

    "isTakeaway": (
        "Takeaway availability",
        "Category / Boolean-like",
        "Inspect distinct values and consistency"
    ),

    "isIndoorSeating": (
        "Indoor seating availability",
        "Category / Boolean-like",
        "Inspect distinct values and consistency"
    ),

    "isVegOnly": (
        "Whether the restaurant is vegetarian-only",
        "Category / Boolean-like",
        "Inspect distinct values and consistency"
    ),

    "Dinner Ratings": (
        "Dinner rating",
        "Numeric-like Text",
        "Contains '-' placeholders; stored as strings"
    ),

    "Dinner Reviews": (
        "Number of dinner reviews",
        "Integer",
        "Check whether zero means no reviews"
    ),

    "Delivery Ratings": (
        "Delivery rating",
        "Numeric-like Text",
        "Contains '-' placeholders; stored as strings"
    ),

    "Delivery Reviews": (
        "Number of delivery reviews",
        "Integer",
        "Check whether zero means no reviews"
    ),

    "KnownFor": (
        "Things the restaurant is known for",
        "Text",
        "97.11% missing values"
    ),

    "PopularDishes": (
        "Popular dishes at the restaurant",
        "Text / Multi-value",
        "82.80% missing values"
    ),

    "PeopleKnownFor": (
        "Information about what people know the restaurant for",
        "Text",
        "60.95% missing values"
    ),

    "AverageCost": (
        "Average cost associated with the restaurant",
        "Integer",
        "Check range, units, and unusual values"
    )
}

for column, details in data_dictionary.items():
    print(f"\nColumn: {column}")
    print(f"Meaning: {details[0]}")
    print(f"Data Category: {details[1]}")
    print(f"Suspected Problem: {details[2]}")

print("\nActual finding:")
print("Data dictionary prepared for all 19 columns.")
print("Suspected problems must be verified before cleaning.")
pd.DataFrame(data_dictionary, index=["Meaning", "Category", "Problem"]).T.to_csv("data_dictionary.csv")


# ------------------------------------------------------------
# 4. DUPLICATE ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE ANALYSIS")
print("=" * 60)

# (a) Fully identical rows

print("\n(a) Fully identical duplicate rows")

print("Prediction:")
print("I expect some duplicate records may exist.")

full_duplicates = df.duplicated().sum()

print("\nActual finding:")
print("Fully identical duplicate count:", full_duplicates)

# (b) Repeated restaurant names

print("\n(b) Repeated restaurant names")

print("Prediction:")
print("Some restaurant names may repeat because restaurant")
print("chains can have multiple branches or locations.")

repeated_name_count = df["Name"].duplicated().sum()

distinct_repeated_names = (
    df.loc[df["Name"].duplicated(keep=False), "Name"]
    .nunique()
)

print("\nActual finding:")
print("Repeated name occurrences:", repeated_name_count)
print("Distinct names appearing more than once:",
      distinct_repeated_names)

print("\nTop 15 most frequent restaurant names:")
print(df["Name"].value_counts().head(15))

print("\nActual restaurant records with repeated names:")

print(
    df[df["Name"].duplicated(keep=False)]
    [["Name", "Area", "AverageCost"]]
    .sort_values(by="Name")
    .head(20)
)

# (c) Repeated Name + Area combinations

print("\n(c) Repeated Name + Area combinations")

print("Prediction:")
print("Some restaurant records may share both the same name")
print("and the same area. These need inspection before")
print("being treated as genuine duplicate records.")

name_area_duplicates = df.duplicated(
    subset=["Name", "Area"]
).sum()

print("\nActual finding:")
print("Repeated Name + Area occurrences:", name_area_duplicates)

print("\nActual records sharing Name + Area:")

print(
    df[
        df.duplicated(
            subset=["Name", "Area"],
            keep=False
        )
    ][["Name", "Area", "Full_Address", "AverageCost"]]
    .sort_values(by=["Name", "Area"])
    .head(20)
)

print("\nDuplicate analysis interpretation:")
print("Zero fully identical duplicate rows does not mean")
print("every restaurant record is unique.")
print("Repeated names do not automatically mean duplicates.")
print("Repeated Name + Area combinations need further checking.")
print("No records have been removed.")


# ------------------------------------------------------------
# 5. NUMERIC-RELATED COLUMN ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("NUMERIC-RELATED COLUMN ANALYSIS")
print("=" * 60)

print("\nPrediction:")
print("Ratings may contain placeholders instead of numeric values.")
print("Review counts and average cost may already be numeric.")

numeric_related_cols = [
    "Dinner Ratings",
    "Dinner Reviews",
    "Delivery Ratings",
    "Delivery Reviews",
    "AverageCost"
]

for col in numeric_related_cols:

    print("\n" + "-" * 60)
    print("Column:", col)

    print("\nData type:")
    print(df[col].dtype)

    print("\nNon-missing values:")
    print(df[col].count())

    print("\nTop 15 values:")
    print(df[col].value_counts().head(15))

    print("\nUnique values:")
    print(df[col].unique())

    # Rating columns are stored as strings.
    # Check for values that are not numeric-looking.

    if col in ["Dinner Ratings", "Delivery Ratings"]:

        numeric_values = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        non_numeric_mask = numeric_values.isna() & df[col].notna()

        print("\nValues that cannot be interpreted as numbers:")
        print(df.loc[non_numeric_mask, col].value_counts())

        print("\nNumber of non-numeric placeholder entries:")
        print(non_numeric_mask.sum())

    print("-" * 60)


# ------------------------------------------------------------
# 6. NUMERIC SUMMARY AND SKEWNESS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("NUMERIC SUMMARY AND SKEWNESS")
print("=" * 60)

print("\nPrediction:")
print("Review counts may have many small values and some")
print("very large values. Average cost may also be unevenly")
print("distributed. I will verify this using summary statistics.")

numeric_cols = [
    "Dinner Reviews",
    "Delivery Reviews",
    "AverageCost"
]

for col in numeric_cols:

    print("\nColumn:", col)

    print("\nDescriptive statistics:")
    print(df[col].describe())

    print("\nSkewness:")
    print(df[col].skew())

print("\nInterpretation guide:")
print("Skewness near 0: approximately symmetric distribution.")
print("Positive skewness: longer tail toward larger values.")
print("Negative skewness: longer tail toward smaller values.")
print("Use the actual skewness values before making a conclusion.")


# ------------------------------------------------------------
# 7. TOP 8 POTENTIAL DATA-QUALITY PROBLEMS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("TOP 8 POTENTIAL DATA-QUALITY PROBLEMS")
print("=" * 60)

print("""
Rank 1: KnownFor has 97.11% missing values.
        Impact: Very high for analysis using this column.

Rank 2: PopularDishes has 82.80% missing values.
        Impact: Very high for popular-dish analysis.

Rank 3: PeopleKnownFor has 60.95% missing values.
        Impact: High for analysis of restaurant reputation.

Rank 4: Timing has 34.78% missing values.
        Impact: High if analyzing opening hours.

Rank 5: Dinner Ratings is stored as text and contains '-'.
        Impact: Ratings cannot be treated directly as numeric.

Rank 6: Delivery Ratings is stored as text and contains '-'.
        Impact: Ratings cannot be treated directly as numeric.

Rank 7: 3,681 repeated restaurant-name occurrences exist.
        Impact: Could affect restaurant counts if names alone
        are treated as unique identifiers.

Rank 8: 124 repeated Name + Area occurrences exist.
        Impact: These records require inspection to determine
        whether they are duplicate listings or separate records.
""")

print("Note: This is a preliminary ranking based on observed")
print("missingness, data types, and repeated values.")
print("It is not proof that every suspected issue is an error.")


# ------------------------------------------------------------
# 8. FINAL DAY 1 SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DAY 1 SUMMARY")
print("=" * 60)

print("Dataset shape:", df.shape)
print("Number of columns:", len(df.columns))
print("Fully identical duplicate rows:", df.duplicated().sum())
print("Repeated restaurant-name occurrences:",
      df["Name"].duplicated().sum())

print("Repeated Name + Area occurrences:",
      df.duplicated(subset=["Name", "Area"]).sum())

print("\nDay 1 inspection completed.")
print("No cleaning or data modification was performed.")

# ============================================================
original_nulls = df.isna().sum()

print("=" * 60)
print("DAY 2 — CLEANING I: STRUCTURE AND TYPES")
print("=" * 60)
original_shape = df.shape
print("\nOriginal shape:", original_shape)
print("\nOriginal data types:")
print(df.dtypes)

print("\nOriginal missing-value counts:")
print(original_nulls)

# ------------------------------------------------------------

# STEP 1: STANDARDIZE COLUMN NAMES

# ------------------------------------------------------------

'''I expect the original column names to contain spaces,

uppercase letters, or special characters.'''

df.columns=df.columns.str.lower()

df.columns = df.columns.str.replace(r'[^\w]+', '_', regex=True)
df.columns=df.columns.str.strip('_')
print(df.columns.duplicated().sum())
print(df.columns.to_list())
'''
DECISION:
I will standardize column names by converting them to lowercase,
replacing spaces and punctuation with underscores, and removing
leading and trailing underscores.

REASON:
Consistent column names make the dataset easier to work with
and reduce the need to handle different naming styles.

VALIDATION:
I will check for duplicate column names after standardization.
If duplicates exist, I will investigate them before deciding
how to handle them.
'''


# ------------------------------------------------------------

# STEP 2: STRIP WHITESPACE FROM TEXT COLUMNS

# ------------------------------------------------------------

'''
PREDICTION:
Some text values may contain leading or trailing spaces,

which could create false categories or affect filtering.'''

text_col=df.select_dtypes(include=["string","object"]).columns
print("text columns:",text_col.to_list())

for col in text_col:
   df[col]=df[col].str.strip()

