SELECT
    order_date,
    category,
    COUNT(*) AS completed_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(gross_amount)::NUMERIC(16,2) AS gross_revenue
FROM {{ ref('stg_orders') }}
WHERE status = 'completed'
GROUP BY 1, 2
