# =====================================================
# WEEK 5 SUNDAY — Titanic Survival Visual Story
# =====================================================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('whitegrid')

# =====================================================
# SECTION 1: LOAD + SAVE OFFLINE COPY
# =====================================================

df = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
df.to_csv("titanic_raw.csv", index=False)
print("Saved successfully!")
print("Shape:", df.shape)

# =====================================================
# SECTION 2: CLEANING
# =====================================================

df = df.drop(columns=['PassengerId'])
df.rename(columns={'Pclass': 'Passenger_class'}, inplace=True)

# Title extraction
df["Title"] = df["Name"].str.extract(r",\s*([^.]*)\.")
df["Title"] = df["Title"].str.strip()
df["Title"] = df["Title"].replace(
    ["Capt", "Col", "Don", "Dr", "Jonkheer",
     "Lady", "Major", "Rev", "Sir", "Countess", "the Countess"],
    "Rare"
)
df["Title"] = df["Title"].replace(["Mlle", "Ms"], "Miss")
df["Title"] = df["Title"].replace("Mme", "Mrs")

# Age
df["Age"] = df["Age"].fillna(df["Age"].mean())

# Rename family columns
df.rename(columns={'SibSp': 'horizontal_family'}, inplace=True)
df.rename(columns={'Parch': 'vertical_family'}, inplace=True)

# Cabin — too many missing, drop it
df = df.drop(columns=["Cabin"])

# Embarked
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# Family size (includes the passenger themselves)
df['family_size'] = df['horizontal_family'] + df['vertical_family'] + 1

# Age groups
df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[0, 12, 18, 35, 60, 100],
    labels=["Child", "Teen", "Young Adult", "Adult", "Senior"]
)

# Fare categories
df['FareCategory'] = pd.cut(
    df["Fare"],
    bins=[0, 10, 30, 50, 100, 600],
    labels=['Low', 'Medium', 'Moderate', 'High', 'Very High']
)

print("\nFinal cleaned shape:", df.shape)
print("Missing values:\n", df.isnull().sum())
print("Final columns:\n", df.columns.tolist())

# =====================================================
# SECTION 3: DASHBOARD 1 — Core Survival Story
# =====================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# --- Top left: Overall survival rate (pie) ---
survival_counts = df["Survived"].value_counts()
axes[0, 0].pie(survival_counts,
               labels=['Did not survive', 'Survived'],
               autopct='%1.1f%%',
               colors=['#E74C3C', '#2ECC71'],
               startangle=90)
axes[0, 0].set_title('Overall Survival Rate', fontsize=13, fontweight='bold')
# FINDING: Only ~38% of passengers survived —
# nearly 2 out of 3 people on board died.

# --- Top right: Survival by class (bar) ---
class_survival = df.groupby('Passenger_class', observed=True)['Survived'].mean() * 100
axes[0, 1].bar(class_survival.index.astype(str), class_survival.values,
               color=['#3498DB', '#F39C12', '#E74C3C'])
axes[0, 1].set_title('Survival Rate by Class', fontsize=13, fontweight='bold')
axes[0, 1].set_xlabel('Passenger Class')
axes[0, 1].set_ylabel('Survival Rate (%)')
axes[0, 1].grid(True, alpha=0.5)
# FINDING: 1st class survived at roughly double the rate of 3rd class —
# wealth strongly predicted survival.

# --- Bottom left: Survival by sex (bar) ---
sex_survival = df.groupby('Sex', observed=True)['Survived'].mean() * 100
axes[1, 0].bar(sex_survival.index, sex_survival.values,
               color=['#E67E22', '#9B59B6'])
axes[1, 0].set_title('Survival Rate by Sex', fontsize=13, fontweight='bold')
axes[1, 0].set_xlabel('Sex')
axes[1, 0].set_ylabel('Survival Rate (%)')
axes[1, 0].grid(True, alpha=0.5)
# FINDING: Women survived at a far higher rate than men —
# confirms "women and children first" was a real policy in practice.

# --- Bottom right: Age distribution by survival (histplot) ---
sns.histplot(data=df, x='Age', hue='Survived', bins=20,
             multiple='stack', ax=axes[1, 1])
axes[1, 1].set_title('Age Distribution by Survival', fontsize=13, fontweight='bold')
axes[1, 1].set_xlabel('Age')
axes[1, 1].set_ylabel('Count')
# FINDING: Young children had noticeably better survival odds
# than adults in the same histogram bins.

fig.suptitle('Titanic Survival — Dashboard 1: Core Factors', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('titanic_dashboard_1.png')
plt.show()

# =====================================================
# SECTION 4: DASHBOARD 2 — Deeper Patterns
# =====================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# --- Top left: Family size vs survival (bar) ---
family_size_effect = df.groupby("family_size")["Survived"].mean() * 100
axes[0, 0].bar(family_size_effect.index.astype(str), family_size_effect.values,
               color='#16A085')
axes[0, 0].set_title('Survival Rate by Family Size', fontsize=13, fontweight='bold')
axes[0, 0].set_xlabel('Family Size')
axes[0, 0].set_ylabel('Survival Rate (%)')
axes[0, 0].grid(True, alpha=0.5)
# FINDING: Small families (2-4 people) survived better than solo
# travelers or very large families — mid-size groups had the advantage.

# --- Top right: Fare distribution by class (boxplot) ---
sns.boxplot(data=df, x="Passenger_class", y="Fare", ax=axes[0, 1])
axes[0, 1].set_title('Fare Distribution by Class', fontsize=13, fontweight='bold')
axes[0, 1].set_xlabel('Passenger Class')
axes[0, 1].set_ylabel('Fare ($)')
# FINDING: 1st class fares vary widely with several high outliers;
# 3rd class fares are tightly clustered near the low end.

# --- Bottom left: Class + Gender survival heatmap ---
class_gender_survival = df.pivot_table(
    values="Survived",
    index="Passenger_class",
    columns="Sex",
    aggfunc="mean"
) * 100

sns.heatmap(class_gender_survival, annot=True, fmt=".1f",
            cmap="YlGnBu", vmin=0, vmax=100, ax=axes[1, 0])
axes[1, 0].set_title('Survival Rate — Class x Gender', fontsize=13, fontweight='bold')
axes[1, 0].set_xlabel('Sex')
axes[1, 0].set_ylabel('Passenger Class')
# FINDING: 1st class women had the highest survival rate of any group;
# 3rd class men had the lowest — a gap of roughly 80 percentage points.

# --- Bottom right: Passenger distribution by port (pie) ---
port_counts = df["Embarked"].value_counts()
axes[1, 1].pie(port_counts, labels=port_counts.index,
               autopct="%1.1f%%", startangle=90,
               colors=['#9B59B6', '#F39C12', '#1ABC9C'])
axes[1, 1].set_title('Passenger Distribution by Port', fontsize=13, fontweight='bold')
# FINDING: The large majority of passengers boarded at Southampton (S) —
# the other two ports contributed far smaller shares.

fig.suptitle('Titanic Survival — Dashboard 2: Deeper Patterns', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('titanic_dashboard_2.png')
plt.show()

# =====================================================
# SECTION 5: SUMMARY OF FINDINGS
# =====================================================

print("\n" + "=" * 60)
print("KEY FINDINGS SUMMARY")
print("=" * 60)
print("1. Overall survival rate: {:.1f}%".format(df['Survived'].mean() * 100))
print("2. Survival by class:\n", class_survival)
print("3. Survival by sex:\n", sex_survival)
print("4. Best family size range: 2-4 people")
print("5. Highest survival group: 1st class women")
print("6. Lowest survival group: 3rd class men")