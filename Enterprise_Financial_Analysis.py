import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Load Dataset

df = pd.read_csv(r"D:\Study2\Python\NEW CLASS\PYTHON JIGAR SIR CLASS\Machine Learning\annual-enterprise-survey-2023-financial-year-provisional.csv")

#  Basic Info & Null Values

print(df.info())
print(df.isnull().sum())


#  Data Cleaning

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Fill missing numeric columns with mean
num_cols = df.select_dtypes(include=np.number).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].mean())

# Fill missing text columns with 'Unknown'
obj_cols = df.select_dtypes(include='object').columns
df[obj_cols] = df[obj_cols].fillna('Unknown')

# Identify Columns

possible_sales = [c for c in df.columns if "value" in c]
possible_date = [c for c in df.columns if "year" in c]
possible_category = [c for c in df.columns if "industry_name_nzsioc" in c]

print(" Sales column:", possible_sales)
print(" Date column:", possible_date)
print(" Category column:", possible_category)

sales_col = "value"
year_col = "year"
cat_col = "industry_name_nzsioc"

# Convert year to datetime
df[year_col] = pd.to_datetime(df[year_col], format='%Y', errors='coerce')

# Convert value to numeric
df[sales_col] = pd.to_numeric(df[sales_col], errors='coerce')

#  Split Revenue & Expense

sales_df = df[df['variable_name'] == 'Total income']
expense_df = df[df['variable_name'] == 'Total expenditure']

# Convert to numeric
sales_df['value'] = pd.to_numeric(sales_df['value'], errors='coerce')
expense_df['value'] = pd.to_numeric(expense_df['value'], errors='coerce')

#  KPI Calculations

total_revenue = sales_df['value'].sum()
total_expense = expense_df['value'].sum()
total_profit = total_revenue - total_expense
profit_margin = (total_profit / total_revenue) * 100

print(" Total Revenue:", round(total_revenue, 2))
print(" Total Expense:", round(total_expense, 2))
print(" Total Profit:", round(total_profit, 2))
print(" Profit Margin (%):", round(profit_margin, 2))

# Yearly Revenue vs Profit

sales_yearly = sales_df.groupby(year_col)['value'].sum().reset_index(name='Revenue')
expense_yearly = expense_df.groupby(year_col)['value'].sum().reset_index(name='Expense')

profit_yearly = pd.merge(sales_yearly, expense_yearly, on=year_col, how='inner')
profit_yearly['Profit'] = profit_yearly['Revenue'] - profit_yearly['Expense']

plt.figure(figsize=(10,5))
sns.lineplot(data=profit_yearly, x=year_col, y='Revenue', marker='o', label="Revenue")
sns.lineplot(data=profit_yearly, x=year_col, y='Profit', marker='o', label="Profit")
plt.title(" Yearly Revenue vs Profit")
plt.xlabel("Year")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# Top 10 Industries by Revenue

top_cats = sales_df.groupby(cat_col)['value'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(8,5))
sns.barplot(x=top_cats.values, y=top_cats.index)
plt.title(" Top 10 Industries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Industry")
plt.tight_layout()
plt.show()