-- ==========================================
-- ДЕНЬ 8: ПОДЗАПРОСЫ И ОКОННЫЕ ФУНКЦИИ (10 штук)
-- ==========================================

-- 1. Подзапрос с IN: Вывести названия товаров, которые хотя бы раз заказывали
SELECT name 
FROM products 
WHERE product_id IN (
    SELECT product_id FROM stock_items WHERE stock_item_id IN (
        SELECT stock_item_id FROM order_items
    )
);

-- 2. Подзапрос с EXISTS: Вывести логины пользователей, которые сделали хотя бы один заказ
SELECT login 
FROM users u 
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.user_id
);

-- 3. Подзапрос в SELECT: Вывести название товара и общее количество проданных пар этого товара
SELECT 
    p.name,
    COALESCE((
        SELECT SUM(oi.quantity) 
        FROM order_items oi 
        JOIN stock_items si ON oi.stock_item_id = si.stock_item_id 
        WHERE si.product_id = p.product_id
    ), 0) AS total_sold
FROM products p;

-- 4. Подзапрос в FROM: Вывести заказы, сумма которых больше средней суммы заказа по всей базе
SELECT order_id, total 
FROM (
    SELECT order_id, SUM(quantity * price_at_order) AS total 
    FROM order_items 
    GROUP BY order_id
) AS order_sums
WHERE total > (
    SELECT AVG(total) FROM (
        SELECT SUM(quantity * price_at_order) AS total 
        FROM order_items 
        GROUP BY order_id
    )
);

-- 5. Подзапрос с NOT EXISTS: Вывести товары, которые ни разу не заказывали
SELECT p.name 
FROM products p 
WHERE NOT EXISTS (
    SELECT 1 
    FROM stock_items si 
    JOIN order_items oi ON si.stock_item_id = oi.stock_item_id 
    WHERE si.product_id = p.product_id
);

-- 6. Оконная функция ROW_NUMBER(): Пронумеровать все товары по убыванию цены
SELECT 
    name, 
    price, 
    ROW_NUMBER() OVER(ORDER BY price DESC) AS row_num
FROM products;

-- 7. Оконная функция RANK(): Вывести рейтинг клиентов по сумме их покупок
SELECT 
    u.last_name, 
    SUM(oi.quantity * oi.price_at_order) AS total_spent,
    RANK() OVER(ORDER BY SUM(oi.quantity * oi.price_at_order) DESC) AS client_rank
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id;

-- 8. Оконная функция DENSE_RANK() с PARTITION BY: Пронумеровать товары по цене внутри каждой категории
SELECT 
    category,
    name, 
    price,
    DENSE_RANK() OVER(PARTITION BY category ORDER BY price DESC) AS rank_in_category
FROM products;

-- 9. Оконная функция SUM() с PARTITION BY: Показать цену товара в заказе и общую сумму этого заказа
SELECT 
    oi.order_id,
    p.name,
    (oi.quantity * oi.price_at_order) AS line_total,
    SUM(oi.quantity * oi.price_at_order) OVER(PARTITION BY oi.order_id) AS order_total
FROM order_items oi
JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
JOIN products p ON si.product_id = p.product_id;

-- 10. Оконная функция AVG() с PARTITION BY: Показать разницу между ценой товара и средней ценой в его категории
SELECT 
    category,
    name,
    price,
    AVG(price) OVER(PARTITION BY category) AS avg_category_price,
    price - AVG(price) OVER(PARTITION BY category) AS diff_from_avg
FROM products;