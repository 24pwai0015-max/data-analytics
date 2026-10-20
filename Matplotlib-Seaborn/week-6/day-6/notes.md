# Advanced Filtering in Pandas

A practical guide to filtering Pandas DataFrames with precision, readable syntax, and high performance.

---

## 1. What is Advanced Filtering?

In basic pandas, you filter rows using simple boolean comparisons like `df[df['type'] == 'Movie']`. 
However, real-world data analytics involves:
- Matching against lists of categories without chaining dozens of `==` statements.
- Searching for substrings within comma-separated tag columns (like genres or cast).
- Combining multiple logical constraints (`AND`, `OR`, `NOT`) while respecting operator precedence.
- Expressing complex queries cleanly using SQL-like expressions or named boolean masks.

Mastering advanced filtering allows you to slice multidimensional datasets quickly, cleanly, and without bugs.

---

## 2. Core Concepts & Practical Examples

### 2.1 `isin()` — Membership Filtering
Instead of writing `(df['country'] == 'India') | (df['country'] == 'Japan')`, `isin()` lets you pass a Python list or set:
```python
asian_titles = df[df['country'].isin(['Japan', 'South Korea', 'India'])]
```
- **Rule:** `isin()` checks for **exact whole-value matches**. If a cell contains `'Japan, South Korea'`, `isin(['Japan'])` will evaluate to `False`.

---

### 2.2 `~` (Tilde) — Negation / NOT Operator
In Pandas, the Python keyword `not` cannot operate element-wise on Series. Use the bitwise NOT operator `~`:
```python
# Select all titles NOT produced in the United States
non_us = df[~df['country'].isin(['United States'])]
# or simple inequality:
non_us = df[~(df['country'] == 'United States')]
```
- **Rule:** Always wrap the condition you are negating in parentheses: `~(df['col'] == val)`.

---

### 2.3 `str.contains()` with `na=False` — Substring Search
When columns contain comma-separated tags (like `listed_in = "Dramas, International Movies"`), `isin()` fails because it looks for exact strings. Use vectorized string methods:
```python
horror_titles = df[df['listed_in'].str.contains('Horror', na=False)]
```
- **Crucial Argument:** `na=False` ensures that any missing (`NaN`) values evaluate to `False` rather than `NaN`. Without `na=False`, pandas raises `Cannot mask with non-boolean array containing NA / NaN values`.
- **Case Insensitivity:** Add `case=False` if you want case-insensitive matching.

---

### 2.4 Combined Conditions with `&` and Parentheses
To combine multiple conditions, use bitwise `&` (AND) and `|` (OR). Python keywords `and` / `or` evaluate the truth value of the whole Series and will crash.
```python
# Both conditions must be met:
recent_tv_ma = df[(df['type'] == 'TV Show') & (df['release_year'] > 2017) & (df['rating'] == 'TV-MA')]
```
- **Golden Rule:** Every individual comparison **must** be enclosed in parentheses `()` because bitwise `&` has higher precedence than comparison operators like `>`, `<`, `==`.

---

### 2.5 `.query()` — String Expression Filtering
Pandas `.query()` lets you write concise, expressive filter queries without repeating `df[...]`:
```python
recent_tv_ma = df.query("type == 'TV Show' and release_year > 2017 and rating == 'TV-MA'")
```
- **Referencing External Variables:** Use `@var_name` inside the query string.
- **Handling Column Names with Spaces or Hyphens:** If a column name has spaces (e.g., `date added`) or special characters, you must enclose it in backticks: `` `release year` > 2017 ``.
- **Limitation:** String operations like `.str.contains()` are awkward and less readable inside `.query()`.

---

### 2.6 Multi-Group OR (`|`) with Named Conditions
Complex queries with mixed AND and OR clauses quickly become illegible when written in one line. Best practice is to define **named boolean masks**:
```python
# (Action movies from the United States) OR (Dramas from South Korea)
cond_us_action = (df['type'] == 'Movie') & (df['country'] == 'United States') & (df['listed_in'].str.contains('Action', na=False))
cond_korea_drama = (df['country'] == 'South Korea') & (df['listed_in'].str.contains('Dramas', na=False))

result = df[cond_us_action | cond_korea_drama]
```
- **Advantage:** Easy to read, debug individual masks, and test row counts independently.

---

### 2.7 `between()` and Handling Imputed / Missing Data
To filter numeric ranges inclusively:
```python
titles_2015_2018 = df[df['release_year'].between(2015, 2018, inclusive='both')]
```

#### The Imputation Rule for Missing Values:
> **Crucial Rule:** If you previously ran `df['country'] = df['country'].fillna('Unknown')`, pandas converts all nulls into the string `'Unknown'`.
> Consequently:
> - `df['country'].isnull()` will return **0 rows**!
> - To find missing/unspecified records after fillna, filter explicitly with:
>   `df['country'] == 'Unknown'`

---

## 3. Summary Table

| Concept | Syntax Example | Best Used For | Watch Out For |
|---|---|---|---|
| **`isin()`** | `df[df['col'].isin(['A', 'B'])]` | Categorical multi-value match | Exact match only (won't find substrings) |
| **`~` (NOT)** | `df[~df['col'].isin(['A'])]` | Inverting boolean mask | Missing parentheses: `~(cond)` |
| **`str.contains()`** | `df[df['col'].str.contains('text', na=False)]` | Substring & tag search | Forgetting `na=False` |
| **Combined `&`** | `df[(cond1) & (cond2)]` | Multiple simultaneous filters | Using `and` instead of `&` |
| **Combined `\|`** | `df[(cond1) \| (cond2)]` | Either condition holds | Operator precedence without `()` |
| **`.query()`** | `df.query("age > 20 and sex == 'F'")` | Clean, SQL-like syntax | Columns with spaces need backticks |
| **`between()`** | `df[df['year'].between(2010, 2020)]` | Numeric and date ranges | `inclusive='both'` vs `'neither'` |
| **Imputed Filter**| `df[df['col'] == 'Unknown']` | Locating filled missing entries| `isnull()` finds nothing after `fillna` |

---

## 4. Today's 10 Tasks (Practice Scaffold)

Work through these 10 exercises in `w6_06_advanced_filtering.py`:
1. **`isin()`:** Titles from Japan, South Korea, or India. Print count.
2. **`~` (NOT):** Titles NOT from the United States. Verify non-US + US == 7787.
3. **`str.contains()`:** Titles with `'Horror'` in `listed_in`.
4. **`str.contains()`:** Titles with `'Documentaries'` in `listed_in` (explain why `isin()` cannot work).
5. **Combined `&`:** TV Shows released after 2017 rated `'TV-MA'`.
6. **Combined `&`:** Comedy movies released before 2010.
7. **`.query()`:** Rewrite Task 5 with `.query()`. Note why Task 6 is awkward in `.query()`.
8. **Multi-group `|`:** (Action movies from US) OR (Dramas from South Korea) using named conditions.
9. **`between()`:** Titles released between 2015 and 2018 inclusive.
10. **Bonus:** `director == 'Unknown'` AND `country == 'Unknown'` count and dataset share.
