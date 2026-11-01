SELECT * FROM {{ ref('daily_revenue') }} WHERE gross_revenue < 0
