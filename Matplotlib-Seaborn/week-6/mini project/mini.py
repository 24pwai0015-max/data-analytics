import pandas as pd
df=pd.read_csv(r"D:\4th sem summer\data analytics\Matplotlib-Seaborn\week-6\mini project\BangaloreZomatoData.csv")
# initial analysis
# print(df.describe())
print("initial columns list:\n",df.columns)
print("initial shape:\n",df.shape)
print("null values:\n",df.isnull().sum())

# we will analyse one by one column
print(df['Name'].head(51))
print("dup",df[df["Name"].duplicated()])








