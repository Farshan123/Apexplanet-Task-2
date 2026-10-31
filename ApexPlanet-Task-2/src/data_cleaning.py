"""
ApexPlanet Software Pvt. Ltd. — Data Analytics Internship Task 2
Module: Data Cleaning & Preprocessing Pipeline
Filename: src/data_cleaning.py

Description:
This script performs production-quality data loading, auditing, cleaning,
feature engineering, and database staging for the ApexPlanet sales dataset.
"""

import os
import sys
import sqlite3
import pandas as pd
import numpy as np


def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load the raw Excel dataset from the given path."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Source file not found at: {filepath}")
    
    print(f"[INFO] Loading raw dataset from: {filepath}")
    # Load sheet 'Sales_Dataset'
    df = pd.read_excel(filepath, sheet_name="Sales_Dataset")
    print(f"[INFO] Successfully loaded {len(df)} records with {len(df.columns)} columns.")
    return df


def audit_raw_data(df: pd.DataFrame) -> dict:
    """Perform initial quality audit on raw dataframe."""
    audit = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "unique_order_ids": int(df["Order_ID"].nunique()) if "Order_ID" in df.columns else None,
    }
    return audit


def clean_and_transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply comprehensive data cleaning:
    1. Standardize column names to lowercase snake_case.
    2. Strip whitespace from string/text columns.
    3. Handle missing values transparently:
       - 'age': Impute with median (41) and cast to integer.
       - 'city': Impute with 'Unknown' to avoid distorting real city metrics.
    4. Resolve duplicate Order_ID collisions while preserving distinct transactions.
    5. Parse and validate order dates.
    6. Derive analytical features: year, month, month_name, quarter, year_month, age_group.
    7. Validate numerical integrity and round currency metrics.
    """
    df_clean = df.copy()

    # 1. Standardize column names
    df_clean.columns = [col.strip().lower().replace(" ", "_") for col in df_clean.columns]
    print("[INFO] Standardized column names to snake_case.")

    # 2. Trim string whitespace
    string_cols = df_clean.select_dtypes(include=["object", "string"]).columns
    for col in string_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip()
        # Replace string 'nan' with actual NaN for proper missing handling
        df_clean[col] = df_clean[col].replace({"nan": np.nan, "None": np.nan})

    # 3. Handle missing values
    # Age: Check median before imputation
    median_age = df_clean["age"].median()
    df_clean["age_imputed_flag"] = df_clean["age"].isnull().astype(int)
    df_clean["age"] = df_clean["age"].fillna(median_age).astype(int)
    print(f"[INFO] Imputed missing 'age' values ({df_clean['age_imputed_flag'].sum()} rows) with median: {int(median_age)}.")

    # City: Impute with 'Unknown'
    missing_city_count = df_clean["city"].isnull().sum()
    df_clean["city"] = df_clean["city"].fillna("Unknown")
    print(f"[INFO] Imputed missing 'city' values ({missing_city_count} rows) with 'Unknown'.")

    # 4. Resolve Order_ID collisions (e.g., ORD100050 appears 9 times for distinct purchases)
    # Generate unique order identifiers by suffixing duplicates with occurrence counter
    counts = df_clean.groupby("order_id").cumcount()
    df_clean["order_id_clean"] = np.where(
        counts > 0,
        df_clean["order_id"] + "_DUP" + counts.astype(str),
        df_clean["order_id"]
    )
    print(f"[INFO] Resolved {counts[counts > 0].count()} Order_ID collisions using deterministic suffixing.")

    # 5. Parse dates
    df_clean["order_date"] = pd.to_datetime(df_clean["order_date"], errors="raise")
    print(f"[INFO] Parsed 'order_date'. Range: {df_clean['order_date'].min().date()} to {df_clean['order_date'].max().date()}.")

    # 6. Feature Engineering
    df_clean["year"] = df_clean["order_date"].dt.year
    df_clean["month"] = df_clean["order_date"].dt.month
    df_clean["month_name"] = df_clean["order_date"].dt.strftime("%b")
    df_clean["year_month"] = df_clean["order_date"].dt.strftime("%Y-%m")
    df_clean["quarter"] = "Q" + df_clean["order_date"].dt.quarter.astype(str)
    df_clean["day_of_week"] = df_clean["order_date"].dt.day_name()

    # Demographic Age Groups
    bins = [17, 30, 50, 100]
    labels = ["Young Adult (18-30)", "Middle-Aged (31-50)", "Senior (51-65)"]
    df_clean["age_group"] = pd.cut(df_clean["age"], bins=bins, labels=labels, right=True)

    # 7. Validate and round numerical metrics
    df_clean["quantity"] = df_clean["quantity"].astype(int)
    df_clean["unit_price"] = df_clean["unit_price"].round(2)
    df_clean["total_sales"] = (df_clean["quantity"] * df_clean["unit_price"]).round(2)

    # Reorder columns logically
    ordered_cols = [
        "order_id_clean",
        "order_id",
        "order_date",
        "year",
        "month",
        "month_name",
        "year_month",
        "quarter",
        "day_of_week",
        "customer_id",
        "customer_name",
        "age",
        "age_group",
        "gender",
        "city",
        "product",
        "category",
        "quantity",
        "unit_price",
        "total_sales",
        "age_imputed_flag"
    ]
    df_clean = df_clean[ordered_cols]
    print(f"[INFO] Cleaned dataset prepared: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns.")
    return df_clean


def export_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned dataframe to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Format date as YYYY-MM-DD for standard CSV export
    df_export = df.copy()
    df_export["order_date"] = df_export["order_date"].dt.strftime("%Y-%m-%d")
    df_export.to_csv(output_path, index=False)
    print(f"[INFO] Exported cleaned data to: {output_path}")


def stage_in_sqlite(df: pd.DataFrame, db_path: str, table_name: str = "sales_transactions") -> None:
    """Stage the cleaned dataframe into an SQLite database for SQL analysis."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    df_sqlite = df.copy()
    df_sqlite["order_date"] = df_sqlite["order_date"].dt.strftime("%Y-%m-%d")
    df_sqlite["age_group"] = df_sqlite["age_group"].astype(str)

    conn = sqlite3.connect(db_path)
    df_sqlite.to_sql(table_name, conn, if_exists="replace", index=False)
    
    # Create indexes for optimized query performance
    cursor = conn.cursor()
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_order_id ON {table_name}(order_id_clean);")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_category ON {table_name}(category);")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_city ON {table_name}(city);")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_order_date ON {table_name}(order_date);")
    conn.commit()
    conn.close()
    print(f"[INFO] Staged data in SQLite database at: {db_path} (Table: '{table_name}')")


def main():
    raw_path = os.path.join("Data", "ApexPlanet_DataAnalytics_Dataset.xlsx")
    csv_output = os.path.join("data", "cleaned_data.csv")
    db_output = os.path.join("data", "apexplanet_sales.db")

    print("=" * 60)
    print("ApexPlanet Task 2: Data Cleaning & Preprocessing Pipeline")
    print("=" * 60)

    # Load
    raw_df = load_raw_data(raw_path)

    # Audit
    audit = audit_raw_data(raw_df)
    print(f"[AUDIT] Initial shape: {audit['total_rows']} rows x {audit['total_columns']} columns")
    print(f"[AUDIT] Missing values: {audit['missing_values']}")
    print(f"[AUDIT] Duplicate full rows: {audit['duplicate_rows']}")
    print(f"[AUDIT] Unique Order_IDs: {audit['unique_order_ids']}")

    # Clean & Transform
    cleaned_df = clean_and_transform_data(raw_df)

    # Export
    export_to_csv(cleaned_df, csv_output)
    stage_in_sqlite(cleaned_df, db_output)

    print("=" * 60)
    print("[SUCCESS] Data cleaning pipeline completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()

