from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------------------------------
# 1. LOAD THE DATA
# -------------------------------------------------------------------
print("Loading data...")
DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "netflix_raw.csv"
df = pd.read_csv(DATA_PATH, encoding='latin-1')

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
