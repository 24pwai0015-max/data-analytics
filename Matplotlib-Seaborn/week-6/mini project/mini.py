
'''
========================================================================================================================
                                                    DATA DICTIONARY
========================================================================================================================
Column Name          | What It Means                                  | Type        | Suspected Problem
---------------------+------------------------------------------------+-------------+-----------------------------------
Name                 | Name of the restaurant                         | text        | Duplicate names (chain branches), special characters
URL                  | Unique web link to restaurant's Zomato page    | ID          | High cardinality, redundant if Name + Area is used
Cuisines             | List of food styles/cuisines served            | multi-value | Comma-separated string, needs parsing/one-hot encoding
Area                 | Neighborhood / locality of the restaurant      | category    | Inconsistent casing, trailing spaces, granular naming
Timing               | Daily operational opening and closing hours    | text        | 34.78% missing (3,103 nulls), irregular non-standard text
Full_Address         | Complete street address of the venue           | text        | Unstructured free text, messy punctuation, noise
PhoneNumber          | Contact phone number(s)                        | text        | Mixed formatting, multiple numbers, invalid placeholders
IsHomeDelivery       | Whether home delivery is available (0 or 1)    | category    | Stored as int64 instead of boolean, naming casing
isTakeaway           | Whether takeaway / parcel is available (0 or 1)| category    | Inconsistent camelCase naming vs PascalCase, int64
isIndoorSeating      | Whether dine-in seating is available (0 or 1)  | category    | Stored as int64 instead of boolean
isVegOnly            | Whether restaurant serves pure veg food only   | category    | High class imbalance (majority non-veg), int64
Dinner Ratings       | Average customer rating for dine-in            | number      | Stored as str (object) instead of float; contains non-numeric strings ('-', 'NEW')
Dinner Reviews       | Total number of dine-in customer reviews       | number      | Severe right-skew, high volume of 0-review venues
Delivery Ratings     | Average customer rating for delivery orders    | number      | Stored as str (object) instead of float; contains non-numeric strings ('-', 'NEW')
Delivery Reviews     | Total number of delivery customer reviews      | number      | Severe right-skew, zero review counts
KnownFor             | Special highlight / signature feature          | text        | Massive missingness (97.11% / 8,665 nulls) - candidate for drop
PopularDishes        | Customer favorite / frequently ordered items   | multi-value | Severe missingness (82.80% / 7,388 nulls), comma-separated
PeopleKnownFor       | Customer vibe / ambiance tags and descriptors  | multi-value | Heavy missingness (60.95% / 5,439 nulls), multi-label text
AverageCost          | Estimated cost for two people (INR)            | number      | Right-skewed distribution, potential extreme luxury outliers
========================================================================================================================
'''
import pandas as pd

df_raw = pd.read_csv(r"D:\4th sem summer\data analytics\Matplotlib-Seaborn\week-6\mini project\BangaloreZomatoData.csv")
df = df_raw.copy()
print("copied successfully")

# 1. Load the file. Print shape, columns, dtypes, `info()`, `head()`, `tail()`, `sample(5)`.
print("shape of zomato", df.shape)
print("columns:\n", df.columns)
print("data type info:\n", df.dtypes)
print("overall summery:\n")
df.info()
print("1st 50 heads:\n", df.head(51))
print("end data:\n", df.tail(51))
print("*" * 50)
'''
Method          What it returns
df.head(5)      First 5 rows
df.tail(5)      Last 5 rows
df.sample(5)    Random 5 rows from anywhere in the dataset'''

# 2. Missing values: count AND percentage per column, sorted high to low.
print("missing value and count analysis:")
print("null values:\n", df.isnull().sum())
print("proportion of null values per column:\n", df.isnull().mean() * 100)
print("count analysis:\n", df.count().sort_values(ascending=False))
print("*" * 50)
print("*" * 50)

# 4. Duplicates, three ways. Predict first, then check:
#    (a) fully identical rows, (b) same Name, (c) same Name + Address (or Name + Location).
percentage = df['Name'].duplicated().mean() * 100
print(f"dublicate ones:{percentage:.2f}%")
print("actual duplicate rows:\n", df["Name"].duplicated(keep=False).head(21))

# brutal version
# 1. View actual restaurant records with duplicate names
print("Actual restaurant records with duplicate names:")
duplicate_rows = df[df["Name"].duplicated(keep=False)]
print(duplicate_rows[["Name", "Area", "AverageCost"]].head(10))
print("*" * 50)

# 2. Count non-missing values in each column
print("Total non-null values per column:\n")
print(df.count())
print("*" * 50)

# 3. Count repeated restaurant names beyond their first occurrence
feature_dup_count = df["Name"].duplicated().sum()
print("Repeated restaurant name occurrences:", feature_dup_count)
print("*" * 50)

# 4. Count restaurants sharing the same name
branch_count = df["Name"].value_counts()
dup_names = branch_count[branch_count > 1]
print("Restaurant names appearing more than once:\n")
print(dup_names)
print("*" * 50)

# 5. Count distinct restaurant names appearing more than once
print("Total distinct repeated restaurant names:", len(dup_names))
print("*" * 50)

# 5. For each column that SHOULD be numeric (rating, cost, votes), print `value_counts().head(15)`
#    and `unique()`. List every value that is not a clean number.
numeric_cols = ['Dinner Ratings', 'Delivery Ratings']
for col in numeric_cols:
    print(f"\n--- Top 15 for {col} ---")
    print(df[col].value_counts().head(15))
    print(f"\n--- Unique values in {col} ---")
    print(df[col].unique())
    print("*" * 50)