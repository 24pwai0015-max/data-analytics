
import sys
import numpy as np
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_csv('netflix_raw.csv')

df.to_csv('netflix_raw.csv', index=False)
print("Saved successfully!")
print(df.shape)
print("Columns list:\n", df.columns.tolist())


# 1. Full inspection — shape, columns, dtypes, missing values, head()
print("\nData types:\n", df.dtypes)

print("\nMissing values:\n", df.isnull().sum())

print("\nFirst 5 rows:\n", df.head())


# 2. Predict then check: type value_counts (Movie vs TV Show)
print("\nType counts:\n", df['type'].value_counts())


# 3. Predict then check: top 10 countries by title count
print("\nTop 10 countries:\n", df['country'].value_counts().head(10))


# 4. Predict then check: release_year range
print("\nRelease year stats:\n", df['release_year'].describe())


# 5. Look at 'cast' column
print("\nCast sample:\n", df['cast'].head(5))


# 6. Look at 'listed_in' column
print("\nGenres sample:\n", df['listed_in'].head(5))


# 7. Look at 'duration' column — check both types separately
print(
    "\nMovie durations:\n",
    df[df['type'] == 'Movie']['duration'].head(5)
)

print(
    "\nTV Show durations:\n",
    df[df['type'] == 'TV Show']['duration'].head(5)
)


# ============================================================
# DATA CLEANING
# ============================================================


# 1. Check for duplicate rows — how many are there?
print("\n" + "*" * 50)

print("Duplicates in Netflix:", df.duplicated().sum())

# Returned zero means there are no duplicate rows.


# 2. director: Check missing values
print("*" * 50)

print("Analysis of null values:\n", df['director'].isnull().sum())

print("Data type:\n", df['director'].dtype)

print("Analysis of data:\n", df['director'].head(51))

df["director"]=df["director"].fillna('unknown')
print("after fillna:\n",df["director"].isnull().sum())
print("analysis of unknown rows:\n",df["director"].where(df["director"]==('unknown')).head(51))

print(
    "Analysis of unknown rows:\n",
    df[df["director"] == "unknown"].head(51)
)
print("*" * 50)
# we cannot drop the null rows,because it will disturb the hole anatomy of the dataset
# 3. cast: fill missing with 'Unknown'.
print("Analysis of null values:\n", df['cast'].isnull().sum())
print("Data type:\n", df['cast'].dtype)
print("Analysis of data:\n", df['cast'].head(51))
df["cast"]=df["cast"].fillna('unknown')
print("after fillna:\n",df["cast"].isnull().sum())
print("analysis of unknown rows:\n",df["cast"].where(df["cast"]==('unknown')).head(13))

print(
    "Analysis of unknown rows:\n",
    df[df["cast"] == "unknown"].head(51)
    
    
)

print(df["cast"].head(15))
print("*" * 50)
# 4. country: fill missing with the mode, OR with 'Unknown'.
#    Comment: which did you choose and why?

print(df["country"].head(21))
country_null=df["country"].isnull().sum()
print("null value analysis:\n",country_null)
print(df["country"].unique())
print(df['country'].where(df["country"]=='United States').value_counts())
print(df["country"].unique())
# United States    2555



# 5. rating (7 missing) and date_added (10 missing):
#    look at the affected rows first, then decide how to handle them.

# 6. Convert date_added to datetime.
#    Then create two new columns: year_added and month_added.

# 7. Split duration into two columns:
#    - duration_min (Movies only)
#    - seasons (TV Shows only)
#    Verify: Movies should have NaN in seasons, TV Shows NaN in duration_min.

# 8. Investigate the � characters in cast.
#    Hint: reload with encoding='latin-1' or 'utf-8' and compare.
#    Comment: what did you find?

# 9. Verify: print isnull().sum() and confirm what's left.

# 10. Save the cleaned file as netflix_cleaned.csv