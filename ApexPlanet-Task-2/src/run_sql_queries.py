"""
ApexPlanet Software Pvt. Ltd. — Data Analytics Internship Task 2
Module: SQL Query Execution & Result Exporter
Filename: src/run_sql_queries.py
"""

import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("data", "apexplanet_sales.db")
OUTPUT_DIR = os.path.join("sql", "query_results")

QUERIES = {
    "q1_category_performance": """
        SELECT 
            category,
            COUNT(order_id_clean) AS total_orders,
            SUM(quantity) AS total_units_sold,
            ROUND(SUM(total_sales), 2) AS total_revenue,
            ROUND(AVG(total_sales), 2) AS average_order_value,
            ROUND(SUM(total_sales) * 100.0 / (SELECT SUM(total_sales) FROM sales_transactions), 2) AS revenue_share_pct
        FROM sales_transactions
        GROUP BY category
        ORDER BY total_revenue DESC;
    """,
    "q2_monthly_trend": """
        SELECT 
            year_month,
            month_name,
            COUNT(order_id_clean) AS total_orders,
            SUM(quantity) AS total_units_sold,
            ROUND(SUM(total_sales), 2) AS monthly_revenue,
            ROUND(AVG(total_sales), 2) AS avg_order_value
        FROM sales_transactions
        WHERE year = 2025
        GROUP BY year_month, month_name
        ORDER BY year_month ASC;
    """,
    "q3_city_performance": """
        SELECT 
            city,
            COUNT(order_id_clean) AS order_count,
            SUM(quantity) AS units_sold,
            ROUND(SUM(total_sales), 2) AS total_revenue,
            ROUND(AVG(total_sales), 2) AS avg_order_value,
            ROUND(SUM(total_sales) * 100.0 / (SELECT SUM(total_sales) FROM sales_transactions), 2) AS city_revenue_share_pct
        FROM sales_transactions
        GROUP BY city
        ORDER BY total_revenue DESC;
    """,
    "q4_demographic_segments": """
        SELECT 
            gender,
            age_group,
            COUNT(order_id_clean) AS transaction_count,
            ROUND(SUM(total_sales), 2) AS segment_revenue,
            ROUND(AVG(total_sales), 2) AS avg_ticket_size,
            ROUND(SUM(total_sales) * 100.0 / (SELECT SUM(total_sales) FROM sales_transactions), 2) AS segment_share_pct
        FROM sales_transactions
        GROUP BY gender, age_group
        ORDER BY segment_revenue DESC;
    """,
    "q5_top_customers": """
        SELECT 
            customer_id,
            customer_name,
            gender,
            city,
            COUNT(order_id_clean) AS total_purchases,
            SUM(quantity) AS total_units_bought,
            ROUND(SUM(total_sales), 2) AS cumulative_spend,
            ROUND(AVG(total_sales), 2) AS avg_spend_per_order
        FROM sales_transactions
        GROUP BY customer_id, customer_name, gender, city
        ORDER BY cumulative_spend DESC
        LIMIT 10;
    """,
    "q6_product_economics": """
        SELECT 
            product,
            category,
            COUNT(order_id_clean) AS transaction_count,
            SUM(quantity) AS units_sold,
            ROUND(AVG(unit_price), 2) AS avg_unit_price,
            ROUND(SUM(total_sales), 2) AS total_revenue,
            ROUND(AVG(total_sales), 2) AS avg_revenue_per_order
        FROM sales_transactions
        GROUP BY product, category
        ORDER BY total_revenue DESC;
    """,
    "q7_transaction_tiers": """
        SELECT 
            CASE 
                WHEN total_sales >= 250000 THEN 'High-Value (>= 250k)'
                WHEN total_sales >= 100000 THEN 'Mid-Value (100k - 250k)'
                ELSE 'Standard (< 100k)'
            END AS transaction_tier,
            COUNT(order_id_clean) AS order_count,
            ROUND(COUNT(order_id_clean) * 100.0 / (SELECT COUNT(*) FROM sales_transactions), 2) AS order_count_pct,
            ROUND(SUM(total_sales), 2) AS tier_revenue,
            ROUND(SUM(total_sales) * 100.0 / (SELECT SUM(total_sales) FROM sales_transactions), 2) AS revenue_pct,
            ROUND(AVG(total_sales), 2) AS avg_tier_ticket
        FROM sales_transactions
        GROUP BY transaction_tier
        ORDER BY tier_revenue DESC;
    """
}


def run_and_save_queries():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    print(f"[INFO] Executing business queries against SQLite database: {DB_PATH}")
    for name, query in QUERIES.items():
        df_res = pd.read_sql_query(query, conn)
        out_csv = os.path.join(OUTPUT_DIR, f"{name}.csv")
        df_res.to_csv(out_csv, index=False)
        print(f"[SUCCESS] Query '{name}' returned {len(df_res)} rows -> Saved to {out_csv}")
        print(df_res.head(3))
        print("-" * 50)
    
    conn.close()
    print("[INFO] All SQL queries successfully executed and stored.")


if __name__ == "__main__":
    run_and_save_queries()

