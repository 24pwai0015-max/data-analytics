
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
# we have to select unknown,because mode extarct repitative feature,so the saturated feature will appear in very large
# amount and will dominate other country names,so according to me no mode for today task,the proof is,i have checked the unitaed states ,
# which was 2k plus in the dataset
df["country"]=df["country"].fillna('unknown')
print("null analysis after fillna:\n",df["country"].isnull().sum())
print(
    "Analysis of unknown rows:\n",
    df[df["country"] == "unknown"].head(51)
    
)
print("*" * 50)
# United States    2555



# 5. rating (7 missing) and date_added (10 missing):
#    look at the affected rows first, then decide how to handle them.
print("rating column analysis:\n",df["rating"].head(21))
print("null value analysis:\n",df["rating"].isnull().sum())
print("value counts column analysis:\n",df["rating"].value_counts())
# print("top 3 ratings:\n",df["rating"].sort_values())
print(df[df['rating'].isnull()][['title', 'type', 'release_year']])
# rating: 7 missing values, spanning both Movies and TV Shows,
# no clear pattern by year or genre (documentaries, comedy specials, anime).
# Decision: fillna with 'Not Rated' — keeps rows intact for other
# analyses, and 'Not Rated' is a realistic real-world category
# for unrated content like specials/documentaries.
df['rating'] = df['rating'].fillna('Not Rated')
print("*" * 50)
# 6. Convert date_added to datetime.
#    Then create two new columns: year_added and month_added.
print("analysis of date_added:\n",df['date_added'].head(21))
print(df["date_added"].isnull().sum())
df["date_added"]=pd.to_datetime(df["date_added"].str.strip())
print("datatype confirmation:\n",df["date_added"].dtype)

print("analysis of date_added:\n", df['date_added'].head(21))
print("Nulls before filling:", df["date_added"].isnull().sum())

# Correct way to impute nulls with the mode
mode_date = df["date_added"].mode()[0]
df["date_added"] = df["date_added"].fillna(mode_date)

print("Nulls after filling:", df["date_added"].isnull().sum())
print("datatype confirmation:\n", df["date_added"].dtype)
print("done successfully")
print("*" * 50)
      

# 7. Split duration into two columns:
# the rule:
        #    first we will analyse the series,the we will decide what to do
print("series data analysis using head(21):\n",df["duration"].head(21))
# deep dive
print("intial analysis of duration series:\n",df['duration'].agg(['max','min','count']))
print("types of features it has:\n",df["duration"].str.split().str[-1].value_counts())
# after running this specific line of code above,we found an issue ,with spellings,check the outputs,ll know:
correction=df["duration"].str.split().str[-1].str.rstrip('s')
print("final value counts:\n",correction.value_counts())

#    - duration_min (Movies only)
#    - seasons (TV Shows only)
#    Verify: Movies should have NaN in seasons, TV Shows NaN in duration_min.

# 8. Investigate the � characters in cast.
#    Hint: reload with encoding='latin-1' or 'utf-8' and compare.
#    Comment: what did you find?

# 9. Verify: print isnull().sum() and confirm what's left.

# 10. Save the cleaned file as netflix_cleaned.csv