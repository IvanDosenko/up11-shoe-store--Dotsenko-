-- 1. Вывести всех пользователей (Фамилия, Имя) с их ролями
SELECT u.last_name, u.first_name, r.role_name
FROM users u
JOIN roles r ON u.role_id = r.role_id;

-- 2. Вывести список всех товаров, отсортированных по цене (от дешевых к дорогим)
SELECT name, price FROM products ORDER BY price ASC;

-- 3. Найти всех пользователей с фамилией 'Иванов'
SELECT * FROM users WHERE last_name = 'Иванов';

-- 4. Вывести 3 самых дорогих товара (LIMIT)
SELECT name, price FROM products ORDER BY price DESC LIMIT 3;

-- 5. Вывести уникальные категории товаров (DISTINCT)
SELECT DISTINCT category FROM products;

-- 6. Вывести уникальных производителей (DISTINCT)
SELECT DISTINCT manufacturer FROM products;

-- 7. Найти заказы за последние 15 дней (WHERE по дате)
SELECT order_id, order_date, user_id 
FROM orders 
WHERE order_date >= date('now', '-15 days');

-- 8. Вывести товары, в названии которых есть слово 'Кроссовки' (LIKE)
SELECT name, manufacturer FROM products WHERE name LIKE '%Кроссовки%';

-- 9. Вывести остатки на складе (количество) больше 10 пар
SELECT stock_item_id, product_id, size_id, quantity 
FROM stock_items 
WHERE quantity > 10;

-- 10. Вывести 5 самых дешевых товаров
SELECT name, price FROM products ORDER BY price ASC LIMIT 5;

-- 11. Вывести всех пользователей, у которых не указано отчество (NULL)
SELECT last_name, first_name FROM users WHERE middle_name IS NULL;

-- 12. Вывести список размеров обуви по убыванию
SELECT size_value FROM sizes ORDER BY size_value DESC;

-- 13. Найти товары с ценой от 5000 до 10000 рублей (BETWEEN)
SELECT name, price FROM products WHERE price BETWEEN 5000 AND 10000;

-- 14. Вывести список логинов пользователей и их роли, отсортированные по алфавиту (логин)
SELECT login, role_id FROM users ORDER BY login ASC;

-- 15. Вывести детали самого первого заказа в базе
SELECT * FROM order_items WHERE order_id = 1;