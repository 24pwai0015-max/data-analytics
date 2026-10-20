from pathlib import Path
import pandas as pd

# ==============================================================================
# SETUP CODE
# ==============================================================================
# Depth calculation: parents[0]=day-6, parents[1]=week-6, parents[2]=Matplotlib-Seaborn, parents[3]=Root
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
# PREDICTION: 


# ==============================================================================
# TASK 2: ~ (NOT)
# Titles NOT from the United States. Check that this count plus the US count equals 7787.
# ==============================================================================
# PREDICTION: 


# ==============================================================================
# TASK 3: str.contains()
# Titles with 'Horror' in listed_in.
# ==============================================================================
# PREDICTION: 


# ==============================================================================
# TASK 4: str.contains()
# Titles with 'Documentaries' in listed_in.
# Comment: Why can't isin() be used for 3 and 4?
# ==============================================================================
# PREDICTION: 


# ==============================================================================
# TASK 5: Combined Conditions (&)
# TV Shows released after 2017 rated 'TV-MA'.
# ==============================================================================
# PREDICTION: 


# ==============================================================================
# TASK 6: Combined Conditions (&)
# Comedy movies released before 2010.
# ==============================================================================
# PREDICTION: 


# ==============================================================================
# TASK 7: query()
# Rewrite Task 5 using .query().
# Comment: Why is Task 6 awkward with query()?
# ==============================================================================
# PREDICTION: 


# ==============================================================================
# TASK 8: Multi-group OR (|) with Named Conditions
# (Action movies from the United States) OR (Dramas from South Korea).
# Save each group as a named condition before combining.
# ==============================================================================
# PREDICTION: 


# ==============================================================================
# TASK 9: between()
# Titles released between 2015 and 2018 inclusive.
# ==============================================================================
# PREDICTION: 


# ==============================================================================
# TASK 10 (BONUS): Combined Missing Value Check
# director == 'Unknown' AND country == 'Unknown'.
# Count them and show the share (percentage) of the total dataset.
# ==============================================================================
# PREDICTION: 

