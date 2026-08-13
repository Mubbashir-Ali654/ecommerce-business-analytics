-- ============================================================
-- E-COMMERCE BUSINESS ANALYTICS
-- SQL BUSINESS ANALYSIS
-- ============================================================


-- ============================================================
-- 1. OVERALL BUSINESS PERFORMANCE
-- ============================================================

SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_revenue,
    ROUND(
        SUM(p.payment_value) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN order_payments p
    ON o.order_id = p.order_id;


-- ============================================================
-- 2. ORDER STATUS DISTRIBUTION
-- ============================================================

SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM orders),
        2
    ) AS percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


-- ============================================================
-- 3. REVENUE BY PAYMENT METHOD
-- ============================================================

SELECT
    payment_type,
    ROUND(SUM(payment_value), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(
        SUM(payment_value) * 100.0 /
        (SELECT SUM(payment_value) FROM order_payments),
        2
    ) AS revenue_percentage
FROM order_payments
GROUP BY payment_type
ORDER BY revenue DESC;


-- ============================================================
-- 4. AVERAGE ORDER VALUE BY PAYMENT METHOD
-- ============================================================

WITH order_payment_totals AS (
    SELECT
        order_id,
        payment_type,
        SUM(payment_value) AS order_value
    FROM order_payments
    GROUP BY order_id, payment_type
)

SELECT
    payment_type,
    COUNT(*) AS orders,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM order_payment_totals
GROUP BY payment_type
ORDER BY average_order_value DESC;


-- ============================================================
-- 5. MONTHLY REVENUE TREND
-- ============================================================

WITH order_revenue AS (
    SELECT
        order_id,
        SUM(payment_value) AS revenue
    FROM order_payments
    GROUP BY order_id
)

SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS month,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(r.revenue), 2) AS revenue
FROM orders o
JOIN order_revenue r
    ON o.order_id = r.order_id
GROUP BY month
ORDER BY month;


-- ============================================================
-- 6. TOP 10 PRODUCT CATEGORIES BY REVENUE
-- ============================================================

SELECT
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS category,
    ROUND(SUM(oi.price), 2) AS revenue,
    COUNT(DISTINCT oi.order_id) AS orders,
    COUNT(*) AS items_sold
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation ct
    ON p.product_category_name =
       ct.product_category_name
GROUP BY category
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 7. TOP 10 SELLERS BY REVENUE
-- ============================================================

SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    ROUND(SUM(oi.price), 2) AS revenue,
    COUNT(DISTINCT oi.order_id) AS orders,
    COUNT(*) AS items_sold
FROM sellers s
JOIN order_items oi
    ON s.seller_id = oi.seller_id
GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 8. TOP 10 SELLERS BY ORDER VOLUME
-- ============================================================

SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT oi.order_id) AS orders,
    ROUND(SUM(oi.price), 2) AS revenue
FROM sellers s
JOIN order_items oi
    ON s.seller_id = oi.seller_id
GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state
ORDER BY orders DESC
LIMIT 10;


-- ============================================================
-- 9. SELLER REVENUE VS ORDER VOLUME
-- ============================================================

SELECT
    s.seller_id,
    COUNT(DISTINCT oi.order_id) AS orders,
    ROUND(SUM(oi.price), 2) AS revenue,
    ROUND(
        SUM(oi.price) /
        COUNT(DISTINCT oi.order_id),
        2
    ) AS revenue_per_order
FROM sellers s
JOIN order_items oi
    ON s.seller_id = oi.seller_id
GROUP BY s.seller_id
ORDER BY revenue DESC;


-- ============================================================
-- 10. TOP 10 CUSTOMERS BY REVENUE
-- ============================================================

SELECT
    c.customer_unique_id,
    ROUND(SUM(p.payment_value), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY c.customer_unique_id
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 11. CUSTOMER ORDER FREQUENCY
-- ============================================================

WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)

SELECT
    CASE
        WHEN order_count = 1
            THEN 'One-time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,
    COUNT(*) AS customers,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM customer_orders),
        2
    ) AS percentage
FROM customer_orders
GROUP BY customer_type
ORDER BY customers DESC;


-- ============================================================
-- 12. TOP REPEAT CUSTOMERS
-- ============================================================

SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
HAVING COUNT(DISTINCT o.order_id) > 1
ORDER BY orders DESC
LIMIT 10;


-- ============================================================
-- 13. CUSTOMER VALUE BY CUSTOMER TYPE
-- ============================================================

WITH customer_revenue AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS orders,
        SUM(p.payment_value) AS revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_payments p
        ON o.order_id = p.order_id
    GROUP BY c.customer_unique_id
)

SELECT
    CASE
        WHEN orders = 1
            THEN 'One-time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,
    COUNT(*) AS customers,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS average_revenue
FROM customer_revenue
GROUP BY customer_type
ORDER BY average_revenue DESC;


-- ============================================================
-- 14. REVIEW SCORE DISTRIBUTION
-- ============================================================

SELECT
    review_score,
    COUNT(*) AS reviews,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM order_reviews),
        2
    ) AS percentage
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;


-- ============================================================
-- 15. AVERAGE REVIEW SCORE
-- ============================================================

SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM order_reviews;


-- ============================================================
-- 16. DELIVERY PERFORMANCE
-- ============================================================

SELECT
    ROUND(
        AVG(
            julianday(order_delivered_customer_date)
            - julianday(order_purchase_timestamp)
        ),
        2
    ) AS average_delivery_days,

    ROUND(
        AVG(
            julianday(order_delivered_customer_date)
            - julianday(order_estimated_delivery_date)
        ),
        2
    ) AS average_difference_from_estimate
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;


-- ============================================================
-- 17. LATE DELIVERY RATE
-- ============================================================

SELECT
    CASE
        WHEN julianday(order_delivered_customer_date)
             > julianday(order_estimated_delivery_date)
        THEN 'Late'
        ELSE 'On Time'
    END AS delivery_status,

    COUNT(*) AS orders,

    ROUND(
        COUNT(*) * 100.0 /
        (
            SELECT COUNT(*)
            FROM orders
            WHERE order_delivered_customer_date IS NOT NULL
        ),
        2
    ) AS percentage

FROM orders

WHERE order_delivered_customer_date IS NOT NULL

GROUP BY delivery_status
ORDER BY orders DESC;


-- ============================================================
-- 18. MONTHLY LATE DELIVERY RATE
-- ============================================================

SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS month,

    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN julianday(order_delivered_customer_date)
                 > julianday(order_estimated_delivery_date)
            THEN 1
            ELSE 0
        END
    ) AS late_orders,

    ROUND(
        SUM(
            CASE
                WHEN julianday(order_delivered_customer_date)
                     > julianday(order_estimated_delivery_date)
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage

FROM orders

WHERE order_delivered_customer_date IS NOT NULL

GROUP BY month
ORDER BY month;


-- ============================================================
-- 19. REVIEW SCORE BY DELIVERY STATUS
-- ============================================================

SELECT
    CASE
        WHEN julianday(o.order_delivered_customer_date)
             > julianday(o.order_estimated_delivery_date)
        THEN 'Late'
        ELSE 'On Time'
    END AS delivery_status,

    COUNT(r.review_id) AS reviews,

    ROUND(AVG(r.review_score), 2) AS average_review_score

FROM orders o

JOIN order_reviews r
    ON o.order_id = r.order_id

WHERE o.order_delivered_customer_date IS NOT NULL

GROUP BY delivery_status
ORDER BY average_review_score DESC;


-- ============================================================
-- 20. POSITIVE VS NEGATIVE REVIEWS
-- ============================================================

SELECT
    CASE
        WHEN review_score >= 4
            THEN 'Positive'
        WHEN review_score <= 2
            THEN 'Negative'
        ELSE 'Neutral'
    END AS review_sentiment,

    COUNT(*) AS reviews,

    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM order_reviews),
        2
    ) AS percentage

FROM order_reviews

GROUP BY review_sentiment

ORDER BY reviews DESC;


-- ============================================================
-- END OF BUSINESS ANALYSIS
-- ============================================================