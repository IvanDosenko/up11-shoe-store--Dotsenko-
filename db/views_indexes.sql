-- ==========================================
-- ПРЕДСТАВЛЕНИЯ (VIEWS)
-- ==========================================

-- 1. Список заказов с ФИО клиента
CREATE VIEW IF NOT EXISTS view_orders_with_clients AS
SELECT 
    o.order_id, 
    o.order_date, 
    u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '') AS client_fio,
    u.login
FROM orders o
JOIN users u ON o.user_id = u.user_id;

-- 2. Товары с остатками на складе
CREATE VIEW IF NOT EXISTS view_products_with_stock AS
SELECT 
    p.product_id, 
    p.category,
    p.manufacturer,
    p.name, 
    p.price, 
    COALESCE(SUM(si.quantity), 0) AS total_stock
FROM products p
LEFT JOIN stock_items si ON p.product_id = si.product_id
GROUP BY p.product_id;

-- 3. Топ клиентов по сумме заказов
CREATE VIEW IF NOT EXISTS view_top_clients AS
SELECT 
    u.user_id, 
    u.last_name, 
    u.first_name, 
    SUM(oi.quantity * oi.price_at_order) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id
ORDER BY total_spent DESC;

-- (Индексы у нас уже созданы в файле schema.sql при инициализации)