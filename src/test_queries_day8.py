import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")

def test_window_functions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- Проверка запроса 6: ROW_NUMBER() (Товары по убыванию цены) ---")
    cursor.execute("""
        SELECT name, price, ROW_NUMBER() OVER(ORDER BY price DESC) AS row_num
        FROM products LIMIT 5;
    """)
    for row in cursor.fetchall():
        print(f"Место {row[2]}: {row[0]} (Цена: {row[1]} руб.)")

    print("\n--- Проверка запроса 7: RANK() (Рейтинг клиентов) ---")
    cursor.execute("""
        SELECT 
            u.last_name, 
            SUM(oi.quantity * oi.price_at_order) AS total_spent,
            RANK() OVER(ORDER BY SUM(oi.quantity * oi.price_at_order) DESC) AS client_rank
        FROM users u
        JOIN orders o ON u.user_id = o.user_id
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY u.user_id;
    """)
    for row in cursor.fetchall():
        print(f"Место {row[2]}: {row[0]} (Потрачено: {row[1]} руб.)")

    print("\n--- Проверка запроса 8: PARTITION BY (Ранги внутри категорий) ---")
    cursor.execute("""
        SELECT 
            category, name, price,
            DENSE_RANK() OVER(PARTITION BY category ORDER BY price DESC) AS rank_in_category
        FROM products LIMIT 6;
    """)
    for row in cursor.fetchall():
        print(f"[{row[0]}] Место {row[3]}: {row[1]} (Цена: {row[2]} руб.)")

    conn.close()

if __name__ == "__main__":
    test_window_functions()