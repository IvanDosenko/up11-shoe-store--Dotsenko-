-- ==========================================
-- ДЕНЬ 7: JOIN и АГРЕГАТНЫЕ ФУНКЦИИ (15 штук)
-- ==========================================

-- 1. Вывести список всех заказов с ФИО клиента (INNER JOIN)
SELECT o.order_id, o.order_date, u.last_name, u.first_name
FROM orders o
JOIN users u ON o.user_id = u.user_id;

-- 2. Вывести детали заказов: ID заказа, название товара и количество (INNER JOIN 3 таблиц)
SELECT oi.order_id, p.name, oi.quantity
FROM order_items oi
JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
JOIN products p ON si.product_id = p.product_id;

-- 3. Посчитать общее количество товаров каждого бренда (GROUP BY, COUNT)
SELECT manufacturer, COUNT(product_id) AS models_count
FROM products
GROUP BY manufacturer;

-- 4. Посчитать среднюю цену товаров по категориям (GROUP BY, AVG)
SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category;

-- 5. Вывести общую сумму каждого заказа (SUM, JOIN)
SELECT order_id, SUM(quantity * price_at_order) AS total_amount
FROM order_items
GROUP BY order_id;

-- 6. Вывести суммарные продажи по каждому производителю (SUM)
SELECT p.manufacturer, SUM(oi.quantity * oi.price_at_order) AS total_revenue
FROM order_items oi
JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
JOIN products p ON si.product_id = p.product_id
GROUP BY p.manufacturer;

-- 7. Найти клиентов, сделавших больше 1 заказа (GROUP BY, HAVING)
SELECT user_id, COUNT(order_id) AS orders_count
FROM orders
GROUP BY user_id
HAVING COUNT(order_id) > 1;

-- 8. Вывести товары, которые ни разу не заказывали (LEFT JOIN)
SELECT p.product_id, p.name
FROM products p
LEFT JOIN stock_items si ON p.product_id = si.product_id
LEFT JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
WHERE oi.order_item_id IS NULL;

-- 9. Вывести пользователей, у которых нет заказов (LEFT JOIN)
SELECT u.user_id, u.last_name, u.first_name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL;

-- 10. Вывести общее количество пар обуви на складе (SUM)
SELECT SUM(quantity) AS total_pairs_in_stock
FROM stock_items;

-- 11. Вывести среднюю сумму одного заказа (AVG от подзапроса агрегатов)
SELECT AVG(total_amount) AS avg_order_value
FROM (
    SELECT SUM(quantity * price_at_order) AS total_amount
    FROM order_items
    GROUP BY order_id
);

-- 12. Вывести топ-3 клиентов по сумме заказов (JOIN, GROUP BY, ORDER BY, LIMIT)
SELECT u.last_name, u.first_name, SUM(oi.quantity * oi.price_at_order) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id
ORDER BY total_spent DESC
LIMIT 3;

-- 13. Вывести количество доступных размеров для каждой модели (COUNT, GROUP BY)
SELECT p.name, COUNT(si.size_id) AS available_sizes
FROM products p
JOIN stock_items si ON p.product_id = si.product_id
WHERE si.quantity > 0
GROUP BY p.product_id;

-- 14. Вывести заказы, в которых общая сумма превышает 10 000 рублей (HAVING)
SELECT order_id, SUM(quantity * price_at_order) AS total
FROM order_items
GROUP BY order_id
HAVING total > 10000;

-- 15. Вывести самую дорогую и самую дешевую пару обуви в каталоге (MAX, MIN)
SELECT MAX(price) AS max_price, MIN(price) AS min_price
FROM products;