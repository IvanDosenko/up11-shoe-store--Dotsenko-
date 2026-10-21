import sqlite3
import os
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")

def seed_data():
    """Заполняет базу тестовыми данными."""
    if not os.path.exists(DB_PATH):
        print("[!] База данных не найдена. Сначала запустите src/db_init.py")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    # Очищаем таблицы перед заполнением (чтобы можно было запускать много раз)
    cur.executescript("""
        DELETE FROM order_items;
        DELETE FROM orders;
        DELETE FROM stock_items;
        DELETE FROM products;
        DELETE FROM users;
        DELETE FROM roles;
        DELETE FROM sizes;
        -- Сбрасываем автоинкремент (опционально, для чистоты ID)
        DELETE FROM sqlite_sequence;
    """)

    # 1. Роли
    roles = [("admin",), ("manager",), ("user",), ("reader",)]
    cur.executemany("INSERT INTO roles (role_name) VALUES (?)", roles)

    # 2. Размеры (36-45)
    for size in range(36, 46):
        cur.execute("INSERT INTO sizes (size_value) VALUES (?)", (size,))

    # 3. Пользователи (id ролей: 1-admin, 2-manager, 3-user, 4-reader)
    users = [
        ("Иванов", "Иван", "Иванович", "admin", 1),
        ("Петров", "Петр", "Петрович", "manager1", 2),
        ("Сидорова", "Анна", "Сергеевна", "user1", 3),
        ("Кузнецов", "Алексей", "Владимирович", "user2", 3),
        ("Смирнов", "Дмитрий", "Олегович", "user3", 3),
        ("Попова", "Елена", "Игоревна", "reader1", 4)
    ]
    cur.executemany("""
        INSERT INTO users (last_name, first_name, middle_name, login, role_id) 
        VALUES (?, ?, ?, ?, ?)
    """, users)

    # 4. Товары (Продукты)
    products = [
        ("Мужская", "Кроссовки", "Nike", "Air Max 270", "img/nike270.jpg", "Текстиль, резина", "Легкие кроссовки для бега", 8990.00),
        ("Женская", "Туфли", "Ecco", "Shape 55", "img/ecco55.jpg", "Натуральная кожа", "Классические туфли на каблуке", 12500.00),
        ("Мужская", "Ботинки", "Caterpillar", "Colorado", "img/cat_col.jpg", "Кожа, нубук", "Прочные ботинки для зимы", 15900.00),
        ("Детская", "Сандалии", "Adidas", "Water Sandal", "img/adidas_sand.jpg", "Синтетика", "Удобные сандалии для пляжа", 3200.00),
        ("Женская", "Кроссовки", "Puma", "Suede Classic", "img/puma_suede.jpg", "Замша", "Стильные повседневные кроссовки", 7400.00),
        ("Мужская", "Классика", "Salvatore Ferragamo", "Derby", "img/sf_derby.jpg", "Кожа", "Оксфорды для деловых встреч", 45000.00)
    ]
    cur.executemany("""
        INSERT INTO products (category, subcategory, manufacturer, name, image_path, composition, description, price) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, products)

    # 5. Товарные позиции (склад). 
    # Сгенерируем для каждого товара несколько размеров со случайным количеством.
    stock_data = []
    # Предположим, у нас создалось 6 товаров (product_id от 1 до 6) и 10 размеров (size_id от 1 до 10)
    for product_id in range(1, 7):
        # Для каждого товара возьмем 3 случайных размера
        sizes_for_product = random.sample(range(1, 11), 3)
        for size_id in sizes_for_product:
            qty = random.randint(0, 15) # от 0 до 15 пар
            stock_data.append((product_id, size_id, qty))
            
    cur.executemany("""
        INSERT INTO stock_items (product_id, size_id, quantity) 
        VALUES (?, ?, ?)
    """, stock_data)

    # 6. Заказы и 7. Состав заказов
    # Сгенерируем 5 заказов от разных пользователей (user_id от 3 до 5)
    for i in range(1, 6):
        order_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        user_id = random.randint(3, 5)
        
        cur.execute("INSERT INTO orders (order_date, user_id) VALUES (?, ?)", (order_date, user_id))
        order_id = cur.lastrowid
        
        # Добавим в каждый заказ по 1-2 позиции
        num_items = random.randint(1, 2)
        for _ in range(num_items):
            # Берем случайную позицию со склада
            cur.execute("SELECT stock_item_id, quantity FROM stock_items WHERE quantity > 0 ORDER BY RANDOM() LIMIT 1")
            stock_item = cur.fetchone()
            
            if stock_item:
                stock_item_id = stock_item[0]
                # Покупаем 1 или 2 пары
                qty_bought = min(random.randint(1, 2), stock_item[1]) 
                
                # Получаем цену товара для фиксации в заказе
                cur.execute("""
                    SELECT p.price FROM products p 
                    JOIN stock_items si ON p.product_id = si.product_id 
                    WHERE si.stock_item_id = ?
                """, (stock_item_id,))
                price = cur.fetchone()[0]
                
                cur.execute("""
                    INSERT INTO order_items (order_id, stock_item_id, quantity, price_at_order) 
                    VALUES (?, ?, ?, ?)
                """, (order_id, stock_item_id, qty_bought, price))
                
                # Уменьшаем остаток на складе
                cur.execute("UPDATE stock_items SET quantity = quantity - ? WHERE stock_item_id = ?", (qty_bought, stock_item_id))

    conn.commit()
    conn.close()
    print("[OK] Тестовые данные успешно добавлены в базу!")

if __name__ == "__main__":
    seed_data()