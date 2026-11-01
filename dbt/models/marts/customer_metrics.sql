SELECT
    customer_id,
    COUNT(*) AS completed_orders,
    SUM(gross_amount)::NUMERIC(16,2) AS lifetime_value,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date
FROM {{ ref('stg_orders') }}
WHERE status = 'completed'
GROUP BY 1
