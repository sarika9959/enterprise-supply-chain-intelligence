-- ============================================
-- SUPPLY CHAIN INTELLIGENCE PLATFORM
-- SQL Analysis Queries
-- ============================================

-- Query 1: Overall order status breakdown
SELECT 
    status,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY status
ORDER BY order_count DESC;


-- Query 2: 10 worst-performing suppliers by on-time rate
-- FINDING: All 6 worst suppliers are Tier C, yet still receive 1,400+ orders each.
-- Recommendation: Reduce order volume to Tier C suppliers or renegotiate contracts.
SELECT 
    s.supplier_name,
    s.reliability_tier,
    s.region,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN o.status = 'Delivered' THEN 1 ELSE 0 END) AS on_time_orders,
    ROUND(SUM(CASE WHEN o.status = 'Delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS on_time_rate
FROM orders o
JOIN suppliers s ON o.supplier_id = s.supplier_id
GROUP BY s.supplier_name, s.reliability_tier, s.region
HAVING COUNT(*) > 50
ORDER BY on_time_rate ASC
LIMIT 10;


-- Query 3: Average delay days by supplier tier
-- FINDING: Tier C suppliers average 2.8 days late vs 0.78 days for Tier A (3.5x worse).
SELECT 
    s.reliability_tier,
    ROUND(AVG(o.delay_days), 2) AS avg_delay_days,
    COUNT(*) AS total_orders
FROM orders o
JOIN suppliers s ON o.supplier_id = s.supplier_id
WHERE o.status IN ('Delivered', 'Delayed')
GROUP BY s.reliability_tier
ORDER BY avg_delay_days DESC;

-- Query 4: Product category risk exposure from Tier C suppliers
-- FINDING: Chassis & Structural parts have the highest dollar exposure ($4B+) 
-- to unreliable (Tier C) suppliers, with 2.6-day average delays.
SELECT 
    p.category,
    COUNT(*) AS order_count,
    ROUND(AVG(o.delay_days), 2) AS avg_delay_days,
    SUM(o.order_value) AS total_value
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN suppliers s ON o.supplier_id = s.supplier_id
WHERE s.reliability_tier = 'C'
GROUP BY p.category
ORDER BY total_value DESC;

-- Query 5: Warehouse performance comparison
-- FINDING: All warehouses perform within a tight band (69-70%), ruling out
-- warehouse operations as a root cause. Confirms the issue is supplier-driven.
SELECT 
    w.warehouse_name,
    w.region,
    COUNT(*) AS total_orders,
    ROUND(SUM(CASE WHEN o.status = 'Delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS on_time_rate
FROM orders o
JOIN warehouses w ON o.warehouse_id = w.warehouse_id
GROUP BY w.warehouse_name, w.region
ORDER BY on_time_rate ASC;