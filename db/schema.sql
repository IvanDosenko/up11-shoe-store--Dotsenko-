PRAGMA foreign_keys = ON;

-- 1. Справочник ролей
CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL
);

-- 2. Пользователи
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    login TEXT UNIQUE NOT NULL CHECK(length(login) BETWEEN 3 AND 20),
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT
);

-- 3. Товары (модели обуви)
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    subcategory TEXT,
    manufacturer TEXT NOT NULL,
    name TEXT NOT NULL,
    image_path TEXT,
    composition TEXT,
    description TEXT,
    price NUMERIC NOT NULL CHECK(price > 0)
);

-- 4. Справочник размеров
CREATE TABLE sizes (
    size_id INTEGER PRIMARY KEY AUTOINCREMENT,
    size_value NUMERIC NOT NULL CHECK(size_value > 15 AND size_value < 55)
);

-- 5. Товарные позиции (модель + размер = конкретная пара)
CREATE TABLE stock_items (
    stock_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    size_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity >= 0),
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    FOREIGN KEY (size_id) REFERENCES sizes(size_id) ON DELETE RESTRICT
);

-- 6. Заказы
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TEXT NOT NULL, -- ISO 8601 (YYYY-MM-DD)
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- 7. Состав заказов
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    stock_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price_at_order NUMERIC NOT NULL CHECK(price_at_order > 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (stock_item_id) REFERENCES stock_items(stock_item_id) ON DELETE RESTRICT
);

-- 8. Таблица аудита (требование из п.11)
CREATE TABLE audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    action TEXT NOT NULL,
    record_id INTEGER,
    changed_at TEXT DEFAULT (datetime('now'))
);

-- Индексы на внешние ключи и поля поиска
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_users_login ON users(login);
CREATE INDEX idx_stock_items_product_id ON stock_items(product_id);
CREATE INDEX idx_stock_items_size_id ON stock_items(size_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_stock_item_id ON order_items(stock_item_id);
CREATE INDEX idx_products_name ON products(name);