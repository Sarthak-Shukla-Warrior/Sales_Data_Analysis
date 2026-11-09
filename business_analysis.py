import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CANDIDATE_PATHS = [
    os.path.join(BASE_DIR, "data", "sales.csv"),
    os.path.join(BASE_DIR, "sales.csv"),
    os.path.join(os.path.expanduser("~"), "Downloads", "sales.csv"),
]
DATA_PATH = next((p for p in CANDIDATE_PATHS if os.path.exists(p)), None)
if DATA_PATH is None:
    raise SystemExit(
        "\nsales.csv was not found. Please copy it into this folder:\n  "
        + os.path.join(BASE_DIR, "data")
        + "\n\n(I also looked in:\n  " + "\n  ".join(CANDIDATE_PATHS) + ")"
    )
print("Using data file:", DATA_PATH)
OUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

SHOW_PLOTS = True
if not SHOW_PLOTS:
    matplotlib.use("Agg")

# Set Seaborn style
sns.set_theme(style="whitegrid", palette="muted")


def save_and_show(filename):
    """Save the current chart as PNG into outputs/, then show it."""
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, filename), dpi=150, bbox_inches="tight")
    if SHOW_PLOTS:
        plt.show()
    plt.close()


# 1. Load Dataset
df = pd.read_csv(DATA_PATH)

# Basic Info
print(df.head())
print(df.tail())
print(df.shape)
print(df.columns)
print(df.dtypes)

# Missing & Duplicate Check
print("Missing Values:\n", df.isnull().sum())
print("Duplicate Rows:", df.duplicated().sum())

# Clean Data
df = df.drop_duplicates()
df["Date"] = pd.to_datetime(df["Order Date"])
df["Item Type"] = df["Item Type"].fillna("Unknown")
df["Total Revenue"] = df["Total Revenue"].fillna(0)

# Quick Stats
print("Transactions:", len(df))
print("Products:", df["Item Type"].unique())
print("Categories:", df["Item Type"].nunique())
print("Total Revenue:", df["Total Revenue"].sum())

# ---------------- Business Questions ---------------- #

# High Sales
high_sales = df[df["Total Revenue"] > 10000]
print(high_sales)

# Filter Example
fruits_sales = df[(df["Item Type"] == "Fruits") & (df["Total Revenue"] > 1000)]
print(fruits_sales)

# Sort by Revenue
sorted_sales = df.sort_values("Total Revenue", ascending=False)
print(sorted_sales.head())

# Total Revenue & Quantity
print("Total Sales:", df["Total Revenue"].sum())
print("Total Quantity:", df["Units Sold"].sum())

# Best Selling Product
product_sales = df.groupby("Item Type")["Total Revenue"].sum().sort_values(ascending=False)
print(product_sales)

# Product Quantity
product_quantity = df.groupby("Item Type")["Units Sold"].sum().sort_values(ascending=False)
print(product_quantity)

# Average Sales
print("Average Sale:", df["Total Revenue"].mean())

# Summary Table
summary = df.groupby("Item Type").agg(
    Total_Sales=("Total Revenue", "sum"),
    Average_Sales=("Total Revenue", "mean"),
    Total_Quantity=("Units Sold", "sum"),
    Transactions=("Item Type", "count")
)
print(summary)
summary.to_csv(os.path.join(OUT_DIR, "summary_table.csv"))  # also save the table

# ---------------- Time-Based Analysis ---------------- #

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.month_name()

# Daily Sales
daily_sales = df.groupby("Date")["Total Revenue"].sum()

# Monthly Sales
monthly_sales = df.groupby(["Year", "Month"])["Total Revenue"].sum()

# Best & Worst Month
print("Best Month:", monthly_sales.idxmax(), "Sales:", monthly_sales.max())
print("Worst Month:", monthly_sales.idxmin(), "Sales:", monthly_sales.min())

# Monthly Growth
monthly_growth = monthly_sales.pct_change() * 100
print("Monthly Growth:\n", monthly_growth)

# ---------------- Visualization with Seaborn ---------------- #

# 1. Monthly Sales Trend
plt.figure(figsize=(10, 6))
sns.lineplot(data=monthly_sales.reset_index(),
             x="Month", y="Total Revenue", hue="Year", marker="o",
             palette="deep", linewidth=2.5)
plt.xticks(range(1, 13))
plt.title("Monthly Sales Trend")
save_and_show("1_monthly_sales_trend.png")

# 2. Category-wise Sales
plt.figure(figsize=(10, 6))
sns.barplot(data=summary.reset_index(),
            x="Item Type", y="Total_Sales", hue="Item Type", palette="viridis", legend=False)
plt.title("Total Sales by Category")
plt.xticks(rotation=45)
save_and_show("2_sales_by_category.png")

# 3. Product Quantity Distribution
plt.figure(figsize=(10, 6))
sns.barplot(data=product_quantity.reset_index(),
            x="Item Type", y="Units Sold", hue="Item Type", palette="magma", legend=False)
plt.title("Units Sold by Product")
plt.xticks(rotation=45)
save_and_show("3_units_sold_by_product.png")

# 4. Monthly Revenue Heatmap
monthly_matrix = df.pivot_table(index="Year", columns="Month_Name",
                                values="Total Revenue", aggfunc="sum").fillna(0)
# show months in calendar order (Jan -> Dec), not alphabetical
month_order = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]
monthly_matrix = monthly_matrix.reindex(columns=[m for m in month_order if m in monthly_matrix.columns])
plt.figure(figsize=(12, 5))
sns.heatmap(monthly_matrix, annot=True, fmt=".0f", cmap="coolwarm")
plt.title("Monthly Revenue Heatmap")
save_and_show("4_monthly_revenue_heatmap.png")

print("Done! Charts saved in:", OUT_DIR)
