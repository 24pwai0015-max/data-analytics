from pathlib import Path
import pandas as pd

# ==============================================================================
# SETUP CODE
# ==============================================================================
DATA = Path(__file__).resolve().parents[3] / "data"

netflix = pd.read_csv(DATA / "netflix_raw.csv", encoding="latin-1")
netflix["country"] = netflix["country"].fillna("Unknown")
netflix["director"] = netflix["director"].fillna("Unknown")
netflix["listed_in"] = netflix["listed_in"].fillna("Unknown")

print("Netflix data loaded successfully. Shape:", netflix.shape)

# ==============================================================================
# TASK 1: isin()
# Titles from Japan, South Korea, or India. Print len().
# ==============================================================================
# .isin() checks whether each value in a column matches any item in a given list.
asian_countries = ["Japan", "South Korea", "India"]
task1_df = netflix[netflix["country"].isin(asian_countries)]
print("Task 1 - Asian titles count:", len(task1_df))


# ==============================================================================
# TASK 2: ~ (NOT)
# Titles NOT from the United States. Check that this count plus the US count equals 7787.
# ==============================================================================
# The tilde (~) inverts a boolean condition (turns True to False and False to True).
not_us = netflix[~(netflix["country"] == "United States")]
is_us = netflix[netflix["country"] == "United States"]

count_not_us = len(not_us)
count_us = len(is_us)
total = count_not_us + count_us

print(f"Task 2 - Non-US: {count_not_us}, US: {count_us}, Total: {total}")
print("Task 2 - Check passes:", total == 7787)


# ==============================================================================
# TASK 3: str.contains()
# Titles with 'Horror' in listed_in.
# ==============================================================================
# .str.contains() searches for a substring inside text strings.
# na=False ensures missing values are safely treated as False rather than raising errors.
horror_titles = netflix[netflix["listed_in"].str.contains("Horror", na=False)]
print("Task 3 - Horror titles count:", len(horror_titles))


# ==============================================================================
# TASK 4: str.contains()
# Titles with 'Documentaries' in listed_in.
# Comment: Why can't isin() be used for 3 and 4?
# ==============================================================================
# Explanation:
# isin() requires an exact full-string match (e.g., cell must be exactly "Horror").
# In 'listed_in', genres are combined lists like "Horror Movies, International Movies".
# str.contains() finds partial matches anywhere within the text.
docs = netflix[netflix["listed_in"].str.contains("Documentaries", na=False)]
print("Task 4 - Documentaries count:", len(docs))


# ==============================================================================
# TASK 5: Combined Conditions (&)
# TV Shows released after 2017 rated 'TV-MA'.
# ==============================================================================
# In pandas:
# - Always wrap each individual condition in parentheses (...)
# - Use '&' for AND, not the Python word 'and'
task5_df = netflix[
    (netflix["type"] == "TV Show")
    & (netflix["release_year"] > 2017)
    & (netflix["rating"] == "TV-MA")
]
print("Task 5 - TV-MA shows after 2017:", len(task5_df))


# ==============================================================================
# TASK 6: Combined Conditions (&)
# Comedy movies released before 2010.
# ==============================================================================
task6_df = netflix[
    (netflix["type"] == "Movie")
    & (netflix["release_year"] < 2010)
    & (netflix["listed_in"].str.contains("Comedies", na=False))
]
print("Task 6 - Comedy movies before 2010:", len(task6_df))


# ==============================================================================
# TASK 7: query()
# Rewrite Task 5 using .query().
# Comment: Why is Task 6 awkward with query()?
# ==============================================================================
# Explanation for Task 6 with query():
# Task 6 uses string methods (.str.contains()). Inside query(), string operations
# require complex engine syntax like `.query('listed_in.str.contains("Comedies")')`,
# which is less readable and harder to debug than standard boolean indexing.
task7_df = netflix.query(
    "type == 'TV Show' and release_year > 2017 and rating == 'TV-MA'"
)
print("Task 7 - TV-MA shows after 2017 via query():", len(task7_df))


# ==============================================================================
# TASK 8: Multi-group OR (|) with Named Conditions
# (Action movies from the United States) OR (Dramas from South Korea).
# Save each group as a named condition before combining.
# ==============================================================================
# Group 1: Action movies from the US
cond_us_action = (
    (netflix["type"] == "Movie")
    & (netflix["country"] == "United States")
    & (netflix["listed_in"].str.contains("Action", na=False))
)

# Group 2: Dramas from South Korea
cond_sk_drama = (netflix["country"] == "South Korea") & (
    netflix["listed_in"].str.contains("Dramas", na=False)
)

# Combine using pipe '|' (OR)
task8_df = netflix[cond_us_action | cond_sk_drama]
print("Task 8 - US Action OR SK Drama titles:", len(task8_df))


# ==============================================================================
# TASK 9: between()
# Titles released between 2015 and 2018 inclusive.
# ==============================================================================
# .between(start, end, inclusive='both') checks boundaries (inclusive by default).
task9_df = netflix[netflix["release_year"].between(2015, 2018)]
print("Task 9 - Titles released between 2015 and 2018:", len(task9_df))


# ==============================================================================
# TASK 10 (BONUS): Combined Missing Value Check
# director == 'Unknown' AND country == 'Unknown'.
# Count them and show the share (percentage) of the total dataset.
# ==============================================================================
both_unknown = netflix[
    (netflix["director"] == "Unknown") & (netflix["country"] == "Unknown")
]
count_unknown = len(both_unknown)
total_rows = len(netflix)
percentage = (count_unknown / total_rows) * 100

print(f"Task 10 - Both Unknown count: {count_unknown}")
print(f"Task 10 - Share of dataset: {percentage:.2f}%")