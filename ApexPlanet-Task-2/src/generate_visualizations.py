"""
ApexPlanet Software Pvt. Ltd. — Data Analytics Internship Task 2
Module: Visualization & Dashboard Generator
Filename: src/generate_visualizations.py

Description:
Generates publication-quality charts for univariate, bivariate, multivariate
analysis, and the static executive Business Intelligence dashboard mock-up.
"""

import os
import matplotlib
# Use Agg backend for headless generation
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np

# Set cohesive professional styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#CCCCCC"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#EAEAEA"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.7

PRIMARY_BLUE = "#1B365D"    # Deep Navy
SECONDARY_TEAL = "#008080"  # Teal Accent
ACCENT_CORAL = "#E06D53"    # Warm Coral
SLATE_GRAY = "#5A6B7C"      # Neutral Slate
LIGHT_BG = "#F8F9FA"        # Off-white / light slate
CARD_BG = "#FFFFFF"         # Pure white

FIGURES_DIR = os.path.join("reports", "figures")
DASHBOARD_PATH = os.path.join("reports", "dashboard_mockup.png")
DATA_PATH = os.path.join("data", "cleaned_data.csv")


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


def plot_univariate_numerical(df: pd.DataFrame):
    """Plot histograms and boxplots for numerical columns."""
    fig, axes = plt.subplots(2, 4, figsize=(18, 9), facecolor="white")
    num_cols = ["age", "quantity", "unit_price", "total_sales"]
    titles = ["Age (Years)", "Quantity (Units)", "Unit Price (₹)", "Total Sales (₹)"]
    
    for i, col in enumerate(num_cols):
        # Histogram + KDE
        ax_hist = axes[0, i]
        sns.histplot(df[col], kde=True, color=PRIMARY_BLUE, ax=ax_hist, bins=15, edgecolor="white", alpha=0.75)
        ax_hist.set_title(f"Distribution of {titles[i]}", fontsize=12, fontweight="bold", pad=8)
        ax_hist.set_xlabel(titles[i], fontsize=10)
        ax_hist.set_ylabel("Frequency", fontsize=10)
        if col in ["unit_price", "total_sales"]:
            ax_hist.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"₹{x*1e-3:.0f}K"))
        
        # Mean & Median lines
        mean_val = df[col].mean()
        median_val = df[col].median()
        ax_hist.axvline(mean_val, color=ACCENT_CORAL, linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:,.1f}")
        ax_hist.axvline(median_val, color=SECONDARY_TEAL, linestyle="-", linewidth=1.5, label=f"Median: {median_val:,.1f}")
        ax_hist.legend(fontsize=8, loc="upper right")

        # Boxplot
        ax_box = axes[1, i]
        sns.boxplot(x=df[col], ax=ax_box, color="#D0E1F9", flierprops={"marker": "o", "color": ACCENT_CORAL, "alpha": 0.5})
        ax_box.set_title(f"Box Plot: {titles[i]}", fontsize=11, fontweight="bold", pad=8)
        ax_box.set_xlabel(titles[i], fontsize=10)
        if col in ["unit_price", "total_sales"]:
            ax_box.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"₹{x*1e-3:.0f}K"))

    plt.suptitle("Univariate Analysis: Numerical Variable Distributions & Outlier Audits", fontsize=15, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = os.path.join(FIGURES_DIR, "01_univariate_numerical_distributions.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved: {out_path}")


def plot_univariate_categorical(df: pd.DataFrame):
    """Plot bar charts for key categorical distributions."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 11), facecolor="white")

    # 1. Category Distribution
    ax1 = axes[0, 0]
    cat_counts = df["category"].value_counts()
    bars1 = ax1.bar(cat_counts.index, cat_counts.values, color=PRIMARY_BLUE, edgecolor="white", width=0.6)
    ax1.set_title("Order Volume by Category", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Order Count", fontsize=10)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{yval} ({yval/len(df)*100:.1f}%)", ha="center", va="bottom", fontsize=9)

    # 2. Gender Distribution
    ax2 = axes[0, 1]
    gender_counts = df["gender"].value_counts()
    colors_gender = [PRIMARY_BLUE, SECONDARY_TEAL]
    bars2 = ax2.bar(gender_counts.index, gender_counts.values, color=colors_gender, edgecolor="white", width=0.5)
    ax2.set_title("Order Volume by Customer Gender", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Order Count", fontsize=10)
    ax2.grid(axis="y", linestyle="--", alpha=0.7)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{yval} ({yval/len(df)*100:.1f}%)", ha="center", va="bottom", fontsize=9)

    # 3. City Distribution
    ax3 = axes[1, 0]
    city_counts = df["city"].value_counts().sort_values(ascending=True)
    bars3 = ax3.barh(city_counts.index, city_counts.values, color=SLATE_GRAY, edgecolor="white", height=0.65)
    ax3.set_title("Order Volume by City", fontsize=12, fontweight="bold")
    ax3.set_xlabel("Order Count", fontsize=10)
    ax3.grid(axis="x", linestyle="--", alpha=0.7)
    for bar in bars3:
        xval = bar.get_width()
        ax3.text(xval + 1.5, bar.get_y() + bar.get_height()/2, f"{xval}", ha="left", va="center", fontsize=9)

    # 4. Age Group Distribution
    ax4 = axes[1, 1]
    age_group_counts = df["age_group"].value_counts().loc[["Young Adult (18-30)", "Middle-Aged (31-50)", "Senior (51-65)"]]
    bars4 = ax4.bar(age_group_counts.index, age_group_counts.values, color=SECONDARY_TEAL, edgecolor="white", width=0.5)
    ax4.set_title("Order Volume by Demographic Age Group", fontsize=12, fontweight="bold")
    ax4.set_ylabel("Order Count", fontsize=10)
    ax4.grid(axis="y", linestyle="--", alpha=0.7)
    for bar in bars4:
        yval = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{yval} ({yval/len(df)*100:.1f}%)", ha="center", va="bottom", fontsize=9)

    plt.suptitle("Univariate Analysis: Categorical Field Frequencies", fontsize=15, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = os.path.join(FIGURES_DIR, "02_univariate_categorical_distributions.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved: {out_path}")


def plot_monthly_sales_trend(df: pd.DataFrame):
    """Plot monthly revenue and transaction volume trends across 2025."""
    monthly = df[df["year"] == 2025].groupby(["year_month", "month_name"]).agg(
        revenue=("total_sales", "sum"),
        orders=("order_id_clean", "count")
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(13, 6), facecolor="white")

    # Primary axis: Revenue bar chart
    x = np.arange(len(monthly))
    width = 0.55
    bars = ax1.bar(x, monthly["revenue"] / 1e6, width=width, color=PRIMARY_BLUE, alpha=0.85, label="Monthly Revenue (₹M)")
    ax1.set_ylabel("Total Revenue (₹ Millions)", fontsize=11, fontweight="bold", color=PRIMARY_BLUE)
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly["month_name"], fontsize=10)
    ax1.set_ylim(0, monthly["revenue"].max() / 1e6 * 1.25)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    # Annotate revenue values
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height + 0.25, f"₹{height:.2f}M", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    # Secondary axis: Orders line chart
    ax2 = ax1.twinx()
    line = ax2.plot(x, monthly["orders"], color=ACCENT_CORAL, marker="o", linewidth=2.5, markersize=7, label="Order Count")
    ax2.set_ylabel("Number of Orders", fontsize=11, fontweight="bold", color=ACCENT_CORAL)
    ax2.set_ylim(40, monthly["orders"].max() * 1.2)
    ax2.grid(False)

    # Annotate order counts
    for i, txt in enumerate(monthly["orders"]):
        ax2.annotate(f"{txt}", (x[i], txt + 1.8), ha="center", fontsize=8.5, color=ACCENT_CORAL, fontweight="bold")

    plt.title("2025 Monthly Revenue Trend & Transaction Volume", fontsize=14, fontweight="bold", pad=15)
    
    # Combined legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper left", frameon=True)

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "03_monthly_sales_trend.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved: {out_path}")


def plot_category_performance(df: pd.DataFrame):
    """Plot category revenue and unit volume breakdown."""
    cat_df = df.groupby("category").agg(
        revenue=("total_sales", "sum"),
        units=("quantity", "sum"),
        orders=("order_id_clean", "count"),
        aov=("total_sales", "mean")
    ).sort_values("revenue", ascending=False).reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor="white")

    # 1. Total Revenue by Category
    bars1 = ax1.bar(cat_df["category"], cat_df["revenue"] / 1e6, color=PRIMARY_BLUE, width=0.55)
    ax1.set_title("Total Revenue by Category (₹ Millions)", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Revenue (₹M)", fontsize=10)
    ax1.set_ylim(0, cat_df["revenue"].max() / 1e6 * 1.2)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.8, f"₹{yval:.2f}M", ha="center", va="bottom", fontsize=9, fontweight="bold")

    # 2. Units Sold by Category
    bars2 = ax2.bar(cat_df["category"], cat_df["units"], color=SECONDARY_TEAL, width=0.55)
    ax2.set_title("Total Units Sold by Category", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Units Sold", fontsize=10)
    ax2.set_ylim(0, cat_df["units"].max() * 1.2)
    ax2.grid(axis="y", linestyle="--", alpha=0.7)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 30, f"{yval:,}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.suptitle("Category Performance: Revenue vs Units Sold", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = os.path.join(FIGURES_DIR, "04_category_revenue_and_volume.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved: {out_path}")


def plot_city_performance(df: pd.DataFrame):
    """Plot regional sales revenue and average order value by city."""
    city_df = df.groupby("city").agg(
        revenue=("total_sales", "sum"),
        aov=("total_sales", "mean"),
        orders=("order_id_clean", "count")
    ).sort_values("revenue", ascending=False).reset_index()

    fig, ax1 = plt.subplots(figsize=(13, 6), facecolor="white")

    x = np.arange(len(city_df))
    bars = ax1.bar(x, city_df["revenue"] / 1e6, width=0.5, color=PRIMARY_BLUE, alpha=0.85, label="Total Revenue (₹M)")
    ax1.set_ylabel("Total Revenue (₹ Millions)", fontsize=11, fontweight="bold", color=PRIMARY_BLUE)
    ax1.set_xticks(x)
    ax1.set_xticklabels(city_df["city"], fontsize=10, rotation=15)
    ax1.set_ylim(0, city_df["revenue"].max() / 1e6 * 1.25)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 0.3, f"₹{h:.2f}M", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    # Line for AOV
    ax2 = ax1.twinx()
    ax2.plot(x, city_df["aov"] / 1e3, color=ACCENT_CORAL, marker="s", linewidth=2, markersize=7, label="Average Order Value (₹K)")
    ax2.set_ylabel("Average Order Value (₹ Thousands)", fontsize=11, fontweight="bold", color=ACCENT_CORAL)
    ax2.set_ylim(80, 180)
    ax2.grid(False)

    for i, aov in enumerate(city_df["aov"]):
        ax2.annotate(f"₹{aov/1e3:.0f}K", (x[i], aov/1e3 + 3), ha="center", fontsize=8.5, color=ACCENT_CORAL, fontweight="bold")

    plt.title("Regional Performance: Revenue & Average Order Value by City", fontsize=14, fontweight="bold", pad=15)
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper right")

    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "05_city_sales_comparison.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved: {out_path}")


def plot_correlation_heatmap(df: pd.DataFrame):
    """Plot correlation matrix between numerical features."""
    num_cols = ["age", "quantity", "unit_price", "total_sales", "month"]
    corr_matrix = df[num_cols].corr(method="pearson")

    fig, ax = plt.subplots(figsize=(8, 7), facecolor="white")
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".3f",
        cmap="Blues",
        vmin=-0.2,
        vmax=1.0,
        square=True,
        linewidths=1.2,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation Coefficient"},
        ax=ax
    )
    ax.set_title("Multivariate Correlation Heatmap (Pearson)", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "06_multivariate_correlation_heatmap.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved: {out_path}")


def plot_multivariate_relationships(df: pd.DataFrame):
    """Plot bivariate/multivariate relationships."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor="white")

    # 1. Unit Price vs Total Sales colored by Quantity
    scatter = ax1.scatter(
        df["unit_price"] / 1e3,
        df["total_sales"] / 1e3,
        c=df["quantity"],
        cmap="viridis",
        alpha=0.65,
        edgecolors="none",
        s=35
    )
    ax1.set_title("Unit Price vs Total Sales (Colored by Quantity)", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Unit Price (₹ Thousands)", fontsize=10)
    ax1.set_ylabel("Total Sales (₹ Thousands)", fontsize=10)
    cbar = plt.colorbar(scatter, ax=ax1)
    cbar.set_label("Quantity (Units)", fontsize=9)
    ax1.grid(True, linestyle="--", alpha=0.7)

    # 2. Boxplot: Total Sales by Category with Gender Hue
    sns.boxplot(
        x="category",
        y=df["total_sales"] / 1e3,
        hue="gender",
        data=df,
        palette=[PRIMARY_BLUE, SECONDARY_TEAL],
        ax=ax2,
        fliersize=3
    )
    ax2.set_title("Total Sales Distribution by Category & Gender", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Category", fontsize=10)
    ax2.set_ylabel("Total Sales (₹ Thousands)", fontsize=10)
    ax2.legend(title="Gender", frameon=True)
    ax2.grid(True, linestyle="--", alpha=0.7)

    plt.suptitle("Multivariate Analysis: Cross-Feature Interactions", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = os.path.join(FIGURES_DIR, "07_multivariate_scatter_and_relationships.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved: {out_path}")


def plot_demographic_spending(df: pd.DataFrame):
    """Plot spending distribution across age groups and gender."""
    grouped = df.groupby(["age_group", "gender"], observed=True)["total_sales"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
    sns.barplot(
        x="age_group",
        y=grouped["total_sales"] / 1e6,
        hue="gender",
        data=grouped,
        palette=[PRIMARY_BLUE, SECONDARY_TEAL],
        ax=ax
    )
    ax.set_title("Demographic Revenue Contribution by Age Group & Gender", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Age Group", fontsize=10)
    ax.set_ylabel("Revenue (₹ Millions)", fontsize=10)
    ax.set_ylim(0, grouped["total_sales"].max() / 1e6 * 1.25)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f"₹{height:.2f}M",
                        (p.get_x() + p.get_width() / 2., height + 0.4),
                        ha='center', va='bottom', fontsize=9, fontweight="bold")

    ax.legend(title="Gender", loc="upper left", frameon=True)
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "08_demographic_spending_distribution.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved: {out_path}")


def generate_bi_dashboard(df: pd.DataFrame):
    """
    Generate an executive-grade, static Business Intelligence dashboard mock-up.
    Contains:
    - Executive Header & Reporting Meta
    - 4 Top KPI Cards (Revenue, Orders, AOV, Top Category)
    - Monthly Sales & Volume Trend
    - Category Revenue Share
    - Regional City Performance
    - Key Business Insights Summary Panel
    """
    total_revenue = df["total_sales"].sum()
    total_orders = len(df)
    avg_order_value = df["total_sales"].mean()
    total_units = df["quantity"].sum()
    top_cat = df.groupby("category")["total_sales"].sum().idxmax()
    top_cat_rev = df.groupby("category")["total_sales"].sum().max()
    top_cat_pct = (top_cat_rev / total_revenue) * 100

    fig = plt.figure(figsize=(18, 11), facecolor="#F4F6F9")

    # Grid specification: 4 rows, 3 columns
    # Row 0: Header & KPIs
    # Row 1-2: Main Visualizations
    # Row 3: Insights Panel
    gs = fig.add_gridspec(4, 3, height_ratios=[0.45, 1.2, 1.2, 0.45], hspace=0.35, wspace=0.25)

    # -------------------------------------------------------------
    # 1. HEADER TITLE
    # -------------------------------------------------------------
    fig.text(0.05, 0.96, "APEXPLANET SOFTWARE PVT. LTD. — BUSINESS INTELLIGENCE DASHBOARD", 
             fontsize=17, fontweight="bold", color="#112233")
    fig.text(0.05, 0.935, "Exploratory Data Analysis & Commercial Insights | Period: FY 2025 (Jan 2025 – Dec 2025) | 1,000 Validated Orders", 
             fontsize=10.5, color="#556677")

    # -------------------------------------------------------------
    # 2. FOUR KPI CARDS (Row 0)
    # -------------------------------------------------------------
    kpis = [
        ("TOTAL REVENUE", f"₹{total_revenue/1e6:.2f} M", "Gross Sales across all products", PRIMARY_BLUE),
        ("TOTAL ORDERS", f"{total_orders:,}", "Processed & fulfilled transactions", SECONDARY_TEAL),
        ("AVG ORDER VALUE", f"₹{avg_order_value/1e3:.1f} K", "Mean transaction spend per order", ACCENT_CORAL),
        ("TOP CATEGORY", f"{top_cat}", f"₹{top_cat_rev/1e6:.1f}M ({top_cat_pct:.1f}% Share)", "#2E7D32")
    ]

    for i, (title, value, subtitle, accent_col) in enumerate(kpis):
        ax_kpi = fig.add_subplot(gs[0, :].subgridspec(1, 4)[0, i])
        ax_kpi.set_facecolor(CARD_BG)
        ax_kpi.patch.set_edgecolor("#DDE2E6")
        ax_kpi.patch.set_linewidth(1.2)

        # Colored left accent bar
        ax_kpi.axvline(0.02, ymin=0.1, ymax=0.9, color=accent_col, linewidth=5)

        ax_kpi.text(0.09, 0.72, title, fontsize=9.5, fontweight="bold", color="#6C7A89", transform=ax_kpi.transAxes)
        ax_kpi.text(0.09, 0.38, value, fontsize=17, fontweight="bold", color=PRIMARY_BLUE, transform=ax_kpi.transAxes)
        ax_kpi.text(0.09, 0.14, subtitle, fontsize=8, color="#7F8C8D", transform=ax_kpi.transAxes)

        ax_kpi.set_xticks([])
        ax_kpi.set_yticks([])
        for spine in ax_kpi.spines.values():
            spine.set_color("#E2E8F0")

    # -------------------------------------------------------------
    # 3. CHART 1: MONTHLY REVENUE & ORDER COUNT (Row 1, Cols 0-1)
    # -------------------------------------------------------------
    ax_trend = fig.add_subplot(gs[1, :2])
    ax_trend.set_facecolor(CARD_BG)
    monthly_2025 = df[df["year"] == 2025].groupby(["year_month", "month_name"]).agg(
        rev=("total_sales", "sum"),
        orders=("order_id_clean", "count")
    ).reset_index()

    x_idx = np.arange(len(monthly_2025))
    bars = ax_trend.bar(x_idx, monthly_2025["rev"] / 1e6, width=0.5, color=PRIMARY_BLUE, alpha=0.85, label="Monthly Revenue (₹M)")
    ax_trend.set_ylabel("Revenue (₹ Millions)", fontsize=9.5, fontweight="bold", color=PRIMARY_BLUE)
    ax_trend.set_xticks(x_idx)
    ax_trend.set_xticklabels(monthly_2025["month_name"], fontsize=9)
    ax_trend.set_ylim(0, monthly_2025["rev"].max() / 1e6 * 1.25)
    ax_trend.set_title("Monthly Revenue & Order Volume Trend (2025)", fontsize=11, fontweight="bold", pad=10, loc="left", color="#112233")
    ax_trend.grid(axis="y", linestyle="--", alpha=0.6)

    # Line overlay for orders
    ax_line = ax_trend.twinx()
    ax_line.plot(x_idx, monthly_2025["orders"], color=ACCENT_CORAL, marker="o", linewidth=2, markersize=5, label="Order Count")
    ax_line.set_ylabel("Orders", fontsize=9.5, fontweight="bold", color=ACCENT_CORAL)
    ax_line.set_ylim(40, monthly_2025["orders"].max() * 1.25)
    ax_line.grid(False)

    lines1, lab1 = ax_trend.get_legend_handles_labels()
    lines2, lab2 = ax_line.get_legend_handles_labels()
    ax_trend.legend(lines1 + lines2, lab1 + lab2, loc="upper right", fontsize=8.5, frameon=True)

    # -------------------------------------------------------------
    # 4. CHART 2: CATEGORY REVENUE SHARE (Row 1, Col 2)
    # -------------------------------------------------------------
    ax_cat = fig.add_subplot(gs[1, 2])
    ax_cat.set_facecolor(CARD_BG)
    cat_summary = df.groupby("category")["total_sales"].sum().sort_values(ascending=True)
    bars_cat = ax_cat.barh(cat_summary.index, cat_summary.values / 1e6, color=SECONDARY_TEAL, height=0.55)
    ax_cat.set_title("Revenue by Product Category (₹M)", fontsize=11, fontweight="bold", pad=10, loc="left", color="#112233")
    ax_cat.set_xlabel("Revenue (₹ Millions)", fontsize=9.5)
    ax_cat.grid(axis="x", linestyle="--", alpha=0.6)
    for b in bars_cat:
        w = b.get_width()
        pct = (w / (total_revenue / 1e6)) * 100
        ax_cat.text(w + 0.5, b.get_y() + b.get_height()/2, f"₹{w:.1f}M ({pct:.0f}%)", va="center", fontsize=8.5, fontweight="bold")
    ax_cat.set_xlim(0, cat_summary.max() / 1e6 * 1.35)

    # -------------------------------------------------------------
    # 5. CHART 3: REGIONAL / CITY PERFORMANCE (Row 2, Cols 0-1)
    # -------------------------------------------------------------
    ax_city = fig.add_subplot(gs[2, :2])
    ax_city.set_facecolor(CARD_BG)
    city_summary = df.groupby("city").agg(
        rev=("total_sales", "sum"),
        aov=("total_sales", "mean")
    ).sort_values("rev", ascending=False).reset_index()

    x_city = np.arange(len(city_summary))
    bars_city = ax_city.bar(x_city, city_summary["rev"] / 1e6, width=0.55, color="#34495E", alpha=0.9)
    ax_city.set_title("Geographic Market Revenue & AOV by City", fontsize=11, fontweight="bold", pad=10, loc="left", color="#112233")
    ax_city.set_xticks(x_city)
    ax_city.set_xticklabels(city_summary["city"], fontsize=9)
    ax_city.set_ylabel("Revenue (₹M)", fontsize=9.5, fontweight="bold")
    ax_city.grid(axis="y", linestyle="--", alpha=0.6)
    ax_city.set_ylim(0, city_summary["rev"].max() / 1e6 * 1.25)

    for b in bars_city:
        h = b.get_height()
        ax_city.text(b.get_x() + b.get_width()/2, h + 0.25, f"₹{h:.1f}M", ha="center", va="bottom", fontsize=8, fontweight="bold")

    # -------------------------------------------------------------
    # 6. CHART 4: DEMOGRAPHIC AGE GROUP SHARE (Row 2, Col 2)
    # -------------------------------------------------------------
    ax_demo = fig.add_subplot(gs[2, 2])
    ax_demo.set_facecolor(CARD_BG)
    demo_summary = df.groupby("age_group", observed=True)["total_sales"].sum().loc[
        ["Young Adult (18-30)", "Middle-Aged (31-50)", "Senior (51-65)"]
    ]
    colors_demo = ["#5DADE2", PRIMARY_BLUE, "#F39C12"]
    wedges, texts, autotexts = ax_demo.pie(
        demo_summary.values,
        labels=["Young (18-30)", "Middle (31-50)", "Senior (51-65)"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors_demo,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5, "width": 0.45}  # Donut chart
    )
    plt.setp(autotexts, size=8.5, weight="bold", color="white")
    plt.setp(texts, size=8.5)
    ax_demo.set_title("Demographic Revenue Share", fontsize=11, fontweight="bold", pad=10, loc="left", color="#112233")

    # -------------------------------------------------------------
    # 7. EXECUTIVE INSIGHTS PANEL (Row 3, Span all columns)
    # -------------------------------------------------------------
    ax_ins = fig.add_subplot(gs[3, :])
    ax_ins.set_facecolor("#FFFFFF")
    ax_ins.patch.set_edgecolor("#CCD1D9")
    ax_ins.patch.set_linewidth(1.0)
    ax_ins.set_xticks([])
    ax_ins.set_yticks([])

    insights_text = (
        "EXECUTIVE BUSINESS TAKEAWAYS & ACTIONABLE RECOMMENDATIONS:\n"
        "• Core Revenue Driver: Electronics dominates revenue with ₹50.78M (36.4%), driven by steady demand for Laptops and Mobiles.\n"
        "• Seasonality & Peaks: Q1 peak in March (₹13.06M) and mid-year peak in June (₹12.91M); Q3 experiences a mild lull before Q4 holiday rebound.\n"
        "• Geographic Balance: Tier-1 & Tier-2 cities demonstrate balanced revenue contribution (~10-14% each); Bengaluru posts highest AOV (₹153.9K).\n"
        "• Core Customer Persona: Middle-aged customers (31-50) generate 43.3% of total revenue. Recommended focus: Targeted VIP loyalty & financing programs."
    )
    ax_ins.text(0.02, 0.5, insights_text, fontsize=8.8, color="#2C3E50", va="center", transform=ax_ins.transAxes, linespacing=1.4)

    plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.93])
    plt.savefig(DASHBOARD_PATH, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[INFO] Successfully generated executive dashboard mock-up at: {DASHBOARD_PATH}")


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    df = load_data()
    print("=" * 60)
    print("Generating EDA Figures and Business Intelligence Dashboard")
    print("=" * 60)
    
    plot_univariate_numerical(df)
    plot_univariate_categorical(df)
    plot_monthly_sales_trend(df)
    plot_category_performance(df)
    plot_city_performance(df)
    plot_correlation_heatmap(df)
    plot_multivariate_relationships(df)
    plot_demographic_spending(df)
    generate_bi_dashboard(df)

    print("=" * 60)
    print("[SUCCESS] All figures and dashboard mock-up created successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()
