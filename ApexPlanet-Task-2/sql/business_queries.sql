-- ==============================================================================
-- ApexPlanet Software Pvt. Ltd. — Data Analytics Internship Task 2
-- Project: Exploratory Data Analysis (EDA) & Business Intelligence
-- File: sql/business_queries.sql
-- Database: SQLite (data/apexplanet_sales.db)
-- Table: sales_transactions
-- ==============================================================================

-- ==============================================================================
-- BUSINESS QUESTION 1: Category Revenue & Volume Performance
-- Business Context:
-- Which product categories contribute the most revenue, what is their revenue
-- share, and how many units were sold in each category?
-- Strategic Implication:
-- Identifies profit engines and core product pillars to guide inventory budgeting
-- and merchandising strategies.
-- ==============================================================================
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


-- ==============================================================================
-- BUSINESS QUESTION 2: Monthly Sales Trends and Seasonality
-- Business Context:
-- How does sales revenue and order volume trend month-over-month throughout 2025,
-- and which periods show demand spikes or slowdowns?
-- Strategic Implication:
-- Essential for cash flow management, inventory replenishment planning, and
-- scheduling quarterly marketing promotions.
-- ==============================================================================
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


-- ==============================================================================
-- BUSINESS QUESTION 3: Regional Sales Performance & Market Share by City
-- Business Context:
-- Which geographic markets (cities) generate the highest sales revenue, and how
-- do average order values (AOV) compare across tier-1 and tier-2 locations?
-- Strategic Implication:
-- Guides logistics hub placement, regional marketing allocation, and localized
-- promotional pricing.
-- ==============================================================================
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


-- ==============================================================================
-- BUSINESS QUESTION 4: Demographic Segment Analysis: Gender & Age Groups
-- Business Context:
-- How is customer spending distributed across gender and age tiers
-- (Young Adult, Middle-Aged, Senior)?
-- Strategic Implication:
-- Critical for tailoring brand communication, ad targeting on social platforms,
-- and personalized loyalty programs.
-- ==============================================================================
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


-- ==============================================================================
-- BUSINESS QUESTION 5: Top 10 High-Value Customers
-- Business Context:
-- Who are the top 10 highest-spending customers, how many orders have they
-- placed, and what is their average spend per transaction?
-- Strategic Implication:
-- Enables customer success teams to initiate high-touch VIP relationship
-- management, bespoke offers, and loyalty incentives.
-- ==============================================================================
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


-- ==============================================================================
-- BUSINESS QUESTION 6: Product-Level Performance and Unit Economics
-- Business Context:
-- What are the specific sales volumes, realized unit prices, and revenue
-- totals for every product across all categories?
-- Strategic Implication:
-- Informs SKU rationalization, supplier negotiation for high-demand items,
-- and bundle opportunities.
-- ==============================================================================
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


-- ==============================================================================
-- BUSINESS QUESTION 7: Transaction Tier Segmentation (Revenue Concentration Risk)
-- Business Context:
-- How is revenue distributed between high-value (>= ₹250k), mid-value
-- (₹100k - ₹250k), and standard (< ₹100k) orders?
-- Strategic Implication:
-- Evaluates the Pareto distribution of sales and highlights whether business
-- revenue is overly vulnerable to large transaction volatility.
-- ==============================================================================
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

