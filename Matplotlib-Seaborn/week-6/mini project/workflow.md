# Zomato Bangalore Mini Project - 7-Day Plan

A full exploratory data analysis (EDA) on the Bangalore Zomato restaurant dataset,
built to revise every technique from Months 1 and 2. Time-boxed to 7 days.

## The workflow (what every EDA follows)

```
QUESTION -> INSPECT -> CLEAN -> ENGINEER -> ANALYZE -> VISUALIZE -> COMMUNICATE
   what do     look,     fix the    build new    answer      show it      write what
   I want     don't      mess       columns      questions   in charts    you found
   to know    touch
```

Every step ends with two things: a saved file, and a written note (a DECISION when
you changed data, a FINDING when you learned something).

## Rules

1. The raw CSV is never edited. Work on `df = pd.read_csv(...)` then `df = df.copy()`.
2. Cleaned data goes to a NEW file (never overwrite the raw one).
3. Write a PREDICTION before running, and a FINDING after.
4. Every cleaning step needs a DECISION comment: what you did and why.
5. 15-minute struggle rule before asking for help.
6. Commit to Git at the end of every day.
7. One file per day: `day1_inspect.py`, `day2_clean_types.py`, and so on.

## Short on time? (mid-term weeks)

Each day lists a MUST (about 45 minutes) and a STRETCH. Do the MUST items first.
If a day is lost, do not skip a day: do the MUSTs of two days together.

---

## Day 1 - Load and Inspect (read-only: do not change the data)

**MUST**
1. Load the file. Print shape, columns, dtypes, `info()`, `head()`, `tail()`, `sample(5)`.
2. Missing values: count AND percentage per column, sorted high to low.
3. Build a data dictionary (as comments or a small table). For EVERY column write:
   what it means | type (number / category / text / multi-value / ID) | suspected problem.
4. Duplicates, three ways. Predict first, then check:
   (a) fully identical rows, (b) same Name, (c) same Name + Address (or Name + Location).
   Look at actual examples of rows that share a Name. Are they copies, or something else?
5. For each column that SHOULD be numeric (rating, cost, votes), print `value_counts().head(15)`
   and `unique()`. List every value that is not a clean number.

**STRETCH**
6. `describe()` for numbers and `describe(include='object')` for text.
7. Check for leading/trailing spaces in text columns.
8. Write your Top 8 problems list, ranked by how much damage each would do to an analysis.

**Deliverable:** `day1_inspect.py` + the problems list.
**Share with me:** output of columns, shape, null counts, and your problems list.

---

## Day 2 - Cleaning I: structure and types

**MUST**
1. Copy the data. Standardize column names (lowercase, underscores, no special characters).
2. Strip whitespace from every text column.
3. Duplicates: decide what counts as a duplicate in THIS dataset, remove them, report how many.
   DECISION comment required.
4. Missing values: one decision per column (fill with Unknown, fill with median, drop rows,
   or leave as NaN). Do not use the same answer for every column. DECISION comment each.
5. Convert number-like text columns (rating, cost, votes) to real numbers. Count how many
   values failed to convert and what they were.

**STRETCH**
6. Standardize categories (spelling, casing) in location and type columns.
7. Convert Yes/No columns to True/False or 1/0.
8. Before vs after: shape, null counts, dtypes. Write the row-loss summary.

**Deliverable:** `day2_clean_types.py` saving `zomato_stage1.csv`.
**Share with me:** your DECISION comments and the before/after summary.

---

## Day 3 - Cleaning II and Feature Engineering

**MUST**
1. Load `zomato_stage1.csv`. Find the multi-value columns (cuisines, dishes, etc.).
   Create `n_cuisines` (how many items in each cell) and `primary_cuisine` (the first item).
2. Create a price band from the cost column (`pd.cut` or `pd.qcut`). Comment: why did you
   choose those bin edges?
3. Create a rating band (for example Low / Average / Good / Excellent) from the rating column.
4. Create a popularity band from votes.

**STRETCH**
5. Build a "long" table: one row per restaurant per cuisine (`str.split` then `explode`).
   Comment: why would counting cuisines WITHOUT this step give a wrong answer?
6. Check cost and votes for outliers using the IQR method. Decision: keep, cap, or flag?
7. One feature of your own invention, with a one-line reason.

**Deliverable:** `day3_features.py` saving `zomato_features.csv`.
**Share with me:** your three bands and the reasoning for the bin edges.

---

## Day 4 - Analysis I (groupby, agg, pivot, crosstab, value_counts)

Format for every question: QUESTION | TOOL CHOSEN (and why) | PREDICTION | CODE | FINDING.

**MUST**
1. Top 10 locations by number of restaurants.
2. Average rating by location. Only include locations with enough restaurants
   (decide the minimum and justify it).
3. Does online ordering relate to rating? Use `groupby` with `agg` (mean, median, count).
4. Price band vs rating band: `crosstab` normalized by row.

**STRETCH**
5. `pivot_table`: location x price band, values = average rating.
6. Top 10 cuisines using the long table from Day 3. Compare with a count that uses only
   `primary_cuisine`. How do the rankings differ?
7. Does table booking relate to cost?

**Deliverable:** `day4_analysis1.py` with 7 answered questions.
**Share with me:** your three most surprising findings.

---

## Day 5 - Analysis II (filtering, outliers, correlation)

**MUST** (use a DIFFERENT filtering tool for each)
1. `isin`: restaurants in 3 locations you choose.
2. `~`: everything EXCEPT one restaurant type.
3. `str.contains(na=False)`: restaurants serving a cuisine you choose.
4. `between`: restaurants in a cost range you choose.
5. A multi-group OR using two named conditions.

**STRETCH**
6. "Best value": high rating AND low cost. Define "high" and "low" with numbers, not feelings.
7. "Overrated": high cost AND low rating. How many?
8. Chains: which restaurant names have the most branches? (This links back to your Day 1
   duplicates question.)
9. Correlation matrix of the numeric columns. Which pair is strongest? Does it make sense?
10. Compare medians (not only means) for one comparison. Why can the two differ?

**Deliverable:** `day5_analysis2.py`.
**Share with me:** your "best value" definition and the result.

---

## Day 6 - Visualization

Rules: every chart has a title, labeled axes, and a question it answers.
Save with `plt.savefig()` BEFORE `plt.show()`, then `plt.close()`.

**MUST**
1. Dashboard 1 (2x2 with `plt.subplots`): top locations (bar), rating distribution (hist),
   price band counts (bar), online order vs rating (boxplot).
2. Add `fig.suptitle`. Save as a PNG.

**STRETCH**
3. Dashboard 2 (2x2): location x price band heatmap (use `vmin` and `vmax`), top cuisines,
   cost vs rating scatter with `hue`, a chart of your choice.
4. One "story chart" with an annotation on the key point. Write 2 sentences on why it matters.

**Deliverable:** `day6_visuals.py` + PNG files in an `outputs` folder.
**Share with me:** the PNGs.

---

## Day 7 - Report, Polish, Ship

**MUST**
1. Run every day-file top to bottom in a fresh terminal. Fix any errors.
2. Write `FINDINGS.md`: your 8 best findings, each with a number and one plain sentence.
3. Commit and push to GitHub.

**STRETCH**
4. Write a project `README.md`: what the dataset is, the workflow, the 3 charts you are proudest
   of (embed the PNGs), how to run it.
5. Reflection (5 lines): what you would do differently, 3 mistakes you made and fixed,
   one thing you now do automatically.
6. Compare with your Netflix EDA: what did you catch this time that you missed before?

**Deliverable:** pushed repo folder with scripts, PNGs, FINDINGS.md, README.md.
**Share with me:** the GitHub folder link and your reflection.

---

## Daily commit

```powershell
git add .
git commit -m "Zomato mini project - Day N complete"
git push origin main
```

## Large files

GitHub rejects files over 100 MB. If the raw CSV is large, add it to `.gitignore`
and push only your scripts and outputs.