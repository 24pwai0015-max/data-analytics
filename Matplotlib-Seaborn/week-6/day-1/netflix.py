import pandas as pd

netflix = pd.read_csv(
    'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv'
)
netflix.to_csv('netflix_raw.csv', index=False)
print("Saved successfully!")
print(netflix.shape)
print("Columns list:\n", netflix.columns.tolist())

# 1. Full inspection — shape, columns, dtypes, missing values, head()
print("\nData types:\n", netflix.dtypes)
print("\nMissing values:\n", netflix.isnull().sum())
print("\nFirst 5 rows:\n", netflix.head())

# 2. Predict then check: type value_counts (Movie vs TV Show)
print("\nType counts:\n", netflix['type'].value_counts())

# 3. Predict then check: top 10 countries by title count
print("\nTop 10 countries:\n", netflix['country'].value_counts().head(10))

# 4. Predict then check: release_year range
print("\nRelease year stats:\n", netflix['release_year'].describe())

# 5. Look at 'cast' column
print("\nCast sample:\n", netflix['cast'].head(5))

# 6. Look at 'listed_in' column
print("\nGenres sample:\n", netflix['listed_in'].head(5))

# 7. Look at 'duration' column — check both types separately
print("\nMovie durations:\n", netflix[netflix['type']=='Movie']['duration'].head(5))
print("\nTV Show durations:\n", netflix[netflix['type']=='TV Show']['duration'].head(5))

'''
"""
this is the inspection stage,on next day we will dive deeply into it,
"""'''
