# Advanced Filtering — Syntax Quick Reference

A one-page cheatsheet for daily filtering in Pandas.

---

## 1. Syntax Table for the 7 Core Concepts

| # | Concept | Python Syntax | Description |
|---|---|---|---|
| **1** | **`isin()`** | `df[df['country'].isin(['Japan', 'India'])]` | True if column value exactly matches any item in the list. |
| **2** | **`~` (NOT)** | `df[~(df['country'] == 'United States')]` | Inverts a boolean condition or Series mask. |
| **3** | **`str.contains()`** | `df[df['listed_in'].str.contains('Horror', na=False)]` | True if cell contains substring. Safe with `na=False`. |
| **4** | **Combined `&` / `\|`**| `df[(df['type'] == 'Movie') & (df['release_year'] > 2015)]` | Logical AND (`&`) and OR (`\|`). Requires parentheses. |
| **5** | **`.query()`** | `df.query("type == 'TV Show' and release_year > 2017")` | String expression evaluation. Supports `and`, `or`, `in`. |
| **6** | **Named Masks** | `mask = cond1 & cond2; df[mask \| cond3]` | Break complex multi-group logic into readable steps. |
| **7** | **`between()`** | `df[df['release_year'].between(2015, 2018)]` | Shorthand for `(df['year'] >= 2015) & (df['year'] <= 2018)`. |

---

## 2. Four Common Mistakes

### ❌ Mistake 1: Missing Parentheses Around Comparisons
```python
# FAILS: & has higher precedence than ==
df[df['type'] == 'Movie' & df['release_year'] > 2015]

# FIX: Wrap every condition in parentheses
df[(df['type'] == 'Movie') & (df['release_year'] > 2015)]
```

### ❌ Mistake 2: Forgetting `na=False` in `str.contains()`
```python
# FAILS if column has NaN: ValueError / Cannot mask with non-boolean array
df[df['listed_in'].str.contains('Documentaries')]

# FIX: Explicitly handle NA values
df[df['listed_in'].str.contains('Documentaries', na=False)]
```

### ❌ Mistake 3: Using `isin()` on Multi-Value / Delimited Cells
```python
# FAILS: Returns False for "Action, Comedies" because it expects exact string match
df[df['listed_in'].isin(['Action'])]

# FIX: Use str.contains() with regex or substring
df[df['listed_in'].str.contains('Action', na=False)]
```

### ❌ Mistake 4: Using Python Keywords `and` / `or` in Bracket Filters
```python
# FAILS: The truth value of a Series is ambiguous
df[(df['type'] == 'Movie') and (df['release_year'] > 2015)]

# FIX: Use bitwise & and |
df[(df['type'] == 'Movie') & (df['release_year'] > 2015)]
```

---

## 3. Three Pro Tips

> **💡 Pro Tip 1: The Post-Imputation Filter Check**  
> If you have executed `.fillna('Unknown')`, `df['col'].isnull()` will return 0 rows. To identify records that were originally missing, filter with `df['col'] == 'Unknown'`.

> **💡 Pro Tip 2: Named Boolean Masks for Clean Code**  
> Don't write 4-line expressions inside `df[...]`. Store intermediate boolean Series into variables (`is_recent = df['release_year'] > 2018`, `is_comedy = df['listed_in'].str.contains('Comedy', na=False)`), then combine: `df[is_recent & is_comedy]`.

> **💡 Pro Tip 3: External Variables in `.query()`**  
> Use the `@` prefix inside `.query()` to reference Python variables:
> ```python
> target_countries = ['Japan', 'India', 'South Korea']
> df.query("country in @target_countries")
> ```
