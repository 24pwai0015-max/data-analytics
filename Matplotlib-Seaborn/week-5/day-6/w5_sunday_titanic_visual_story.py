import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
df.to_csv("titanic_raw.csv", index=False)
print("Saved successfully!")

print("Columns list:\n", df.columns)
print("Shape analysis:\n", df.shape)

df = df.drop(columns=['PassengerId'])
print("Updated columns list:\n", df.columns)

# Survived column check
print(df['Survived'].isnull().sum())
# Confirmed there are no null values in Survived

# Rename Pclass
df.rename(columns={'Pclass': 'Passenger_class'}, inplace=True)
print("Updated columns list:\n", df.columns)

# Null check helper pattern
result = df["Passenger_class"].isnull().sum()
print("Null check result:\n", result)
if result == 0:
    print("No null values in Passenger_class — go ahead!")
else:
    print("Stop — nulls found, recheck this column")

print("*" * 50)

# Name analysis
result = df["Name"].isnull().sum()
print("Null check result for Name:\n", result)
if result == 0:
    print("No null values in Name — go ahead!")
else:
    print("Stop — nulls found, recheck this column")
print("strip applied successfully")
# alternative method for rare names,upload csv to ai tool,tool will give you names,
# then replace it throgh pandas .replacw( method)
df["Title"] = df["Name"].str.extract(r",\s*([^.]*)\.")
df["Title"] = df["Title"].str.strip()
print("strip applied successfully")

df["Title"] = df["Title"].replace(
    ["Capt", "Col", "Don", "Dr", "Jonkheer",
     "Lady", "Major", "Rev", "Sir", "Countess", "the Countess"],
    "Rare"
)

df["Title"] = df["Title"].replace(["Mlle", "Ms"], "Miss")
df["Title"] = df["Title"].replace("Mme", "Mrs")


# sex analysis
print(df['Sex'].isnull().sum())
print(df["Sex"].head(11))
print(df["Sex"].value_counts())

# passeneger class vs sex

print(df["Passenger_class"].head(11))
print(df.groupby(['Passenger_class','Sex']).size())

# age analysis

print(df['Age'].isnull().sum())
df["Age"]=df["Age"].fillna(df["Age"].mean())
print(df['Age'].isnull().sum())

# sibling and spouse ,parch
df.rename(columns={'SibSp':'horizontal_family'},inplace=True)
print("Updated columns list:\n", df.columns)
df.rename(columns={'Parch':'vertical_family'},inplace=True)
print("Updated columns list:\n", df.columns)

# ticket
print(df['Ticket'].isnull().sum())
# fare
print(df['Fare'].isnull().sum())
# cabin
print(df['Cabin'].value_counts())
print(df['Cabin'].isnull().sum())
df=df.drop(columns=["Cabin"])
print("Updated columns list:\n", df.columns)
# embarked analysis
print(df['Embarked'].isnull().sum())
print(df["Embarked"].head(11))
df["Embarked"]=df["Embarked"].fillna(df["Embarked"].mode()[0])
print(df['Embarked'].isnull().sum())

# deep analysis

df['family_size'] = df['horizontal_family'] + df['vertical_family']
print(df["family_size"].head(6))
print("Updated columns list:\n", df.columns)
# visual
value_counts=df['family_size'].value_counts()
plt.figure(figsize=(10, 6))
plt.title("Family Size Analysis")
sns.countplot(data=df, x='family_size', color="#E01B1B")
plt.xlabel("Family Size")
plt.ylabel("value_counts")
plt.show()





