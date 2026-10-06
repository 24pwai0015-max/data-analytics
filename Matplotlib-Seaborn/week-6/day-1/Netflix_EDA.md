# Comprehensive Netflix Exploratory Data Analysis (EDA)

This document contains a comprehensive but beginner-friendly Exploratory Data Analysis for the Netflix dataset. The code is written in Python using `pandas` for data manipulation, and `matplotlib` & `seaborn` for visualizations.

## 1. Overview of the Approach
The goal of this EDA is to explore the Netflix dataset deeply without using overly complex logic. We focus on:
1. **Data Cleaning & Feature Engineering**: Handling missing values, fixing date formatting, extracting the numerical value of durations (minutes for movies, seasons for TV shows), and splitting text columns like genres and actors.
2. **Visualizations**: Creating easy-to-understand charts like bar charts, line graphs, and histograms to answer fundamental questions about the dataset.

## 2. The Python Code

You can run the following Python code to perform the data cleaning and generate the 8 comprehensive visualizations.

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------------------------------
# 1. LOAD THE DATA
# -------------------------------------------------------------------
print("Loading data...")
df = pd.read_csv('netflix_raw.csv', encoding='latin-1')

# -------------------------------------------------------------------
# 2. DATA CLEANING & FEATURE ENGINEERING
# -------------------------------------------------------------------
print("Cleaning data and engineering features...")
# Fill missing values
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Not Rated')

# Date added: extract year and month
df['date_added'] = df['date_added'].fillna(df['date_added'].mode()[0])
df['date_added'] = pd.to_datetime(df['date_added'].str.strip())
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month_name()

# Duration: separate into minutes for movies and seasons for TV Shows
# Extract the numeric part using regex
df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
movies_df = df[df['type'] == 'Movie'].copy()
tvshows_df = df[df['type'] == 'TV Show'].copy()

# -------------------------------------------------------------------
# 3. ADVANCED EXPLORATORY DATA ANALYSIS (EDA)
# -------------------------------------------------------------------
print("Generating visualizations...")
sns.set_theme(style="whitegrid")

# --- Plot 1: Movies vs TV Shows ---
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='type', hue='type', palette='pastel', legend=False)
plt.title('Count of Movies vs TV Shows on Netflix', fontsize=16)
plt.xlabel('Type of Content', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.savefig('1_movies_vs_tvshows.png', bbox_inches='tight')
plt.close()

# --- Plot 2: Top 10 Countries with Most Content ---
plt.figure(figsize=(12, 6))
top_countries = df[df['country'] != 'Unknown']['country'].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, hue=top_countries.index, palette='viridis', legend=False)
plt.title('Top 10 Countries with the Most Content', fontsize=16)
plt.xlabel('Number of Titles', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.savefig('2_top_countries.png', bbox_inches='tight')
plt.close()

# --- Plot 3: Content Added Over the Years by Type ---
plt.figure(figsize=(12, 6))
# Group by year and type
trend = df.groupby(['year_added', 'type']).size().reset_index(name='count')
sns.lineplot(data=trend, x='year_added', y='count', hue='type', marker='o', linewidth=2.5)
plt.title('Movies vs TV Shows Added Over the Years', fontsize=16)
plt.xlabel('Year Added', fontsize=12)
plt.ylabel('Number of Titles Added', fontsize=12)
plt.savefig('3_content_added_trend.png', bbox_inches='tight')
plt.close()

# --- Plot 4: Best Month to Release Content ---
plt.figure(figsize=(12, 6))
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
sns.countplot(data=df, x='month_added', hue='month_added', order=month_order, palette='coolwarm', legend=False)
plt.title('Content Added by Month', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45)
plt.savefig('4_content_by_month.png', bbox_inches='tight')
plt.close()

# --- Plot 5: Distribution of Movie Durations ---
plt.figure(figsize=(10, 6))
sns.histplot(data=movies_df, x='duration_num', bins=30, kde=True, color='skyblue')
plt.title('Distribution of Movie Durations (in minutes)', fontsize=16)
plt.xlabel('Duration (minutes)', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.savefig('5_movie_durations.png', bbox_inches='tight')
plt.close()

# --- Plot 6: Number of Seasons in TV Shows ---
plt.figure(figsize=(10, 6))
sns.countplot(data=tvshows_df, x='duration_num', hue='duration_num', palette='Set2', legend=False)
plt.title('Distribution of TV Show Seasons', fontsize=16)
plt.xlabel('Number of Seasons', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.savefig('6_tvshow_seasons.png', bbox_inches='tight')
plt.close()

# --- Plot 7: Top 10 Most Common Genres ---
plt.figure(figsize=(12, 6))
# Split genres that are separated by commas and count them
genres = df['listed_in'].str.split(', ').explode()
top_genres = genres.value_counts().head(10)
sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index, palette='rocket', legend=False)
plt.title('Top 10 Most Common Genres on Netflix', fontsize=16)
plt.xlabel('Number of Titles', fontsize=12)
plt.ylabel('Genre', fontsize=12)
plt.savefig('7_top_genres.png', bbox_inches='tight')
plt.close()

# --- Plot 8: Top 10 Actors on Netflix ---
plt.figure(figsize=(12, 6))
# Exclude 'Unknown' cast members
known_cast = df[df['cast'] != 'Unknown']['cast']
actors = known_cast.str.split(', ').explode()
top_actors = actors.value_counts().head(10)
sns.barplot(x=top_actors.values, y=top_actors.index, hue=top_actors.index, palette='mako', legend=False)
plt.title('Top 10 Actors with the Most Titles', fontsize=16)
plt.xlabel('Number of Titles', fontsize=12)
plt.ylabel('Actor', fontsize=12)
plt.savefig('8_top_actors.png', bbox_inches='tight')
plt.close()

print("Comprehensive EDA is complete! 8 visualizations have been saved as PNG images.")
```

## 3. Summary of Findings
- **Movies vs TV Shows**: Netflix has historically focused heavily on Movies, which vastly outnumber TV Shows in the dataset.
- **Top Countries**: The United States is by far the leading producer of content on Netflix, followed by India and the UK.
- **Content Added Over Years**: There was an exponential growth in content being added to Netflix starting around 2015. When split by type, we see movies heavily drove this peak, but TV show additions have remained steady or slightly increased recently.
- **Seasonality (Months)**: Content seems to be added fairly consistently throughout the year, but we can visualize specific high-volume months (like December or July).
- **Movie Durations**: The vast majority of movies on Netflix are between 80 to 120 minutes long, resembling a classic bell-curve distribution.
- **TV Show Seasons**: Most TV Shows on Netflix only have 1 season, indicating a trend of either limited series or shows getting cancelled early.
- **Top Genres**: International Movies, Dramas, and Comedies dominate the platform's library.
- **Top Actors**: By parsing the cast list, we can see that prolific actors (particularly from the Indian film industry like Anupam Kher or Shah Rukh Khan) appear most frequently in the catalog.
