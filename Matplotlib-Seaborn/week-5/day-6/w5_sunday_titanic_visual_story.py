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
df['family_size'] = df['horizontal_family'] + df['vertical_family'] + 1
# df['family_size'] = df['horizontal_family'] + df['vertical_family']
print(df["family_size"].head(6))
print("Updated columns list:\n", df.columns)
# visual
plt.figure(figsize=(10, 6))
plt.title("Family Size Analysis")
sns.countplot(data=df, x='family_size', color="#E01B1B")
plt.xlabel("Family Size")
plt.ylabel("Count")
plt.show()

# 1. What was the overall survival rate? (pie or bar)
rate=df["Survived"].mean()*100
print(rate)

survivial_counts=df["Survived"].value_counts()
print(survivial_counts)

plt.pie(survivial_counts,labels=
        ['didnt survived','survived'],
        autopct='%1.1f%%',
        startangle=90)
plt.title('survuval rate')
plt.show()

# survival by age

df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[0, 12, 18, 35, 60, 100],
    labels=["Child", "Teen", "Young Adult", "Adult", "Senior"]
)
print("Updated columns list:\n", df.columns)

age_survival=df.groupby('AgeGroup',observed=True)['Survived'].mean()*100
print(age_survival)
plt.title("survival by age")
age_survival.plot(kind="bar")
plt.xlabel('Age group')
plt.ylabel('survival rate')
plt.grid(True,alpha=0.5)
plt.show()
# Did class affect survival? (barplot)
# survival by class

class_survival=df.groupby('Passenger_class',observed=True)['Survived'].mean()*100
print(class_survival)
plt.title("survival by class")
class_survival.plot(kind="bar")
plt.xlabel('class')
plt.ylabel('survival rate')
plt.grid(True,alpha=0.5)
plt.show()


# survival by sex

sex_survival=df.groupby('Sex',observed=True)['Survived'].mean()*100
print(sex_survival)
plt.title("survival by sex")
sex_survival.plot(kind="bar")
plt.xlabel('sex')
plt.ylabel('survival rate')
plt.grid(True,alpha=0.5)
plt.show()

#  Did gender affect survival? (barplot with hue)
plt.title("hue sex")
sns.countplot(data=df,x='Survived',hue='Sex')
plt.show()


# 4. Did age affect survival? (histplot with hue)
sns.histplot(
    data=df,
    x="Age",
    hue="Survived",
    bins=20,
    multiple='stack'
)

plt.title("Age Distribution by Survival")
plt.xlabel("Age")
plt.ylabel("Number of Passengers")
plt.show()
# 5. Did family size affect survival? (barplot or boxplot)
family_size_effect = df.groupby("family_size")["Survived"].mean() * 100

family_size_effect.plot(
    kind="bar",
    color="#CDF80A"
)

plt.title(
    "Family Size vs Survival",
    color="#F01212",
    fontweight="bold",
    fontsize=16
)

plt.xlabel("Family Size")
plt.ylabel("Survival Rate (%)")

plt.show()
# 6. What was the fare distribution by class? (boxplot)
df['fare dist']=pd.cut(
    df["Fare"],
    bins=[0,10,30,50,100,600],
    labels=['low','medium','moderate','high','very high']
)

print("Updated columns list:\n", df.columns)

sns.boxplot(
    data=df,
    x="fare dist",
    y="Passenger_class"
)

plt.title("Fare Distribution vs Passenger Class")
plt.xlabel("Fare Category")
plt.ylabel("Passenger Class")

plt.show()
# 7. Which combination of class+gender survived most/least? (heatmap)
class_gender_survival = df.pivot_table(
    values="Survived",
    index="Passenger_class",
    columns="Sex",
    aggfunc="mean"
) * 100

sns.heatmap(
    class_gender_survival,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu"
    
)

plt.title("Survival Rate by Class and Gender")
plt.xlabel("Gender")
plt.ylabel("Passenger Class")

plt.show()
# 8. How are passengers distributed across ports? (pie)
# 8. How are passengers distributed across ports? (pie)

port_counts = df["Embarked"].value_counts()

plt.pie(
    port_counts,
    labels=port_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Passenger Distribution Across Ports")
plt.show()






