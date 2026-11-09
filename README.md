# 📊 Business Sales Analysis (Python)

Sales data analysis using **pandas, NumPy, Matplotlib and Seaborn**: data cleaning, business questions, monthly trends and charts.

**Dataset:** 72 transactions · 7 product categories · Jan to Dec 2024 (`data/sales.csv`)

## 🔑 Key Findings
| Metric | Result |
|--------|--------|
| Total revenue | **641,250** (8,432 units sold) |
| Average sale | 8,906.25 |
| Top category by revenue | **Cereal** (203,200), then Beverages (171,550) |
| Top category by units | **Cereal** (2,765 units) |
| Weakest category | Fruits (27,550 revenue) |
| Best month | **December** (70,700) |
| Worst month | **February** (35,500) |
| Biggest monthly jump | March (+35.9%), November (+30.1%) |

- Cereal and Beverages together make up about **58%** of all revenue.
- Sales trend upward through the year and peak in **Nov-Dec**.
- Fruits and Vegetables bring the lowest revenue per sale; Household and Personal Care sell few units but each unit earns far more (about 169 and 124 revenue per unit vs about 59 for Fruits).

## 📈 Charts

### Monthly Sales Trend
![Monthly Sales Trend](outputs/1_monthly_sales_trend.png)

### Total Sales by Category
![Sales by Category](outputs/2_sales_by_category.png)

### Units Sold by Product
![Units Sold](outputs/3_units_sold_by_product.png)

### Monthly Revenue Heatmap
![Heatmap](outputs/4_monthly_revenue_heatmap.png)

Full console output is in [`outputs/analysis_output.txt`](outputs/analysis_output.txt) and the category table in [`outputs/summary_table.csv`](outputs/summary_table.csv).

## ▶️ How to run
1. Install libraries: `pip install -r requirements.txt`
2. Run: `python business_analysis.py`

The script reads `data/sales.csv` (columns: `Order Date`, `Item Type`, `Units Sold`, `Total Revenue`) and saves the charts into `outputs/`.

## 📁 Project structure
```
business-analysis/
├── business_analysis.py
├── requirements.txt
├── data/sales.csv
└── outputs/        (charts + summary table)
```

## Tech
Python · pandas · NumPy · Matplotlib · Seaborn
