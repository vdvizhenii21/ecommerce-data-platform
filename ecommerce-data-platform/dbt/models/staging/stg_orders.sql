SELECT
    order_id,
    customer_id,
    ordered_at,
    ordered_at::date AS order_date,
    category,
    quantity,
    unit_price,
    (quantity * unit_price)::NUMERIC(14,2) AS gross_amount,
    status
FROM {{ source('raw', 'orders') }}
