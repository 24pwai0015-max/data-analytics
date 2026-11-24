import pandas as pd

# ==========================================
# 1. Initial Date Conversion & Verification
# ==========================================

data = {
    'Date': ['2026-01-01', '2026-01-02', '2026-01-03'],
    'Sales': [1200, 1500, 1800]
}

df = pd.DataFrame(data)

# Initially, Pandas may recognize the Date column as object (string)
print("before datetime")
print(df.info())

# Convert to datetime and verify
df['Date'] = pd.to_datetime(df['Date'])
print("after datetime")
print(df.info())
# verified, the datatype is datetime


# ==========================================
# 2. Handling Formats & Date Properties
# ==========================================

# Handling Different Date Formats:
# Real datasets don't always store dates in the same format.
# Examples:
#   24-11-2026
#   11/24/2026
#   2026-11-24
#   24 Nov 2026

df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
print(df)
print("*" * 60)
print(df['Date'].dt.year)
print("*" * 60)
print(df['Date'].dt.day)
print("*" * 60)
print(df['Date'].dt.month)
print("*" * 60)
print(df['Date'].dt.month_name())
print("*" * 60)
print(df['Date'].dt.is_month_end)
print("*" * 60)
print(df['Date'].dt.is_month_start)
print("*" * 60)

# Note for invalid or problematic dates:
# df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
# errors='coerce' converts invalid dates into NaT (Not a Time).


# ==========================================
# 3. Date Component Extraction & Indexing
# ==========================================

data1 = {
    'Date': [
        '01-01-2026', '05-01-2026',
        '12-02-2026', '18-03-2026',
        '25-04-2026', '10-05-2026',
        '15-06-2026', '20-07-2026'
    ],
    'Sales': [
        1200, 1500, 1800, 2200,
        1900, 2500, 3000, 2800
    ]
}

df = pd.DataFrame(data1)

# Convert dates
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Extract date components
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.month_name()
df['Day'] = df['Date'].dt.day
df['Day_Name'] = df['Date'].dt.day_name()
df['Quarter'] = df['Date'].dt.quarter

# Set Date as index
df.set_index('Date', inplace=True)
print(df)

print("*/"*60)

# tasks

data = {
    'Order_Date': [
        '12-03-2026',
        '15-03-2026',
        '18-03-2026',
        '22-04-2026',
        '25-04-2026',
        '02-05-2026',
        '10-05-2026',
        '15-06-2026'
    ],

    'Product': [
        'Laptop', 'Mouse', 'Keyboard', 'Monitor',
        'Laptop', 'Headphones', 'Mouse', 'Keyboard'
    ],

    'Sales': [
        120000, 2500, 4500, 35000,
        115000, 8000, 3000, 5000
    ],

    'Quantity': [2, 5, 3, 2, 1, 4, 6, 3]
}

df = pd.DataFrame(data)

# task 1 display 1st five records
print(df.head())
print("*/"*60)
# task 2 Check DataFrame information using df.info().
print(df.info())
print("*/"*60)
# task 3 Convert Order_Date into datetime format.
df['Order_Date']=pd.to_datetime(df['Order_Date'],dayfirst=True)
print(df.info())
print("*/"*60)
# task 4 Set Order_Date as the DataFrame index.
df.set_index('Order_Date',inplace=True)
print(df)
print("*/"*60)
# task 5 Display the index using df.index
print(df.index)
print("*/"*60)
# task 6 Retrieve the record for 18 March 2026.
print(df.loc['18-03-2026'])
# task 7 Retrieve records between 15 March and 25 April 2026.
print(df.loc['15-03-2026':'25-04-2026'])