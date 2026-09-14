import pandas as pd

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