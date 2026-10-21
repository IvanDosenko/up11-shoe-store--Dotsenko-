import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")

def test_joins():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- Проверка запроса 5: Общая сумма каждого заказа ---")
    cursor.execute("""
        SELECT order_id, SUM(quantity * price_at_order) AS total_amount
        FROM order_items
        GROUP BY order_id;
    """)
    for row in cursor.fetchall():
        print(f"Заказ №{row[0]}: {row[1]} руб.")

    print("\n--- Проверка запроса 12: Топ-3 клиента по сумме заказов ---")
    cursor.execute("""
        SELECT u.last_name, u.first_name, SUM(oi.quantity * oi.price_at_order) AS total_spent
        FROM users u
        JOIN orders o ON u.user_id = o.user_id
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY u.user_id
        ORDER BY total_spent DESC
        LIMIT 3;
    """)
    for row in cursor.fetchall():
        print(f"{row[0]} {row[1]}: потратил {row[2]} руб.")

    print("\n--- Проверка запроса 8: Товары без заказов ---")
    cursor.execute("""
        SELECT p.product_id, p.name
        FROM products p
        LEFT JOIN stock_items si ON p.product_id = si.product_id
        LEFT JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
        WHERE oi.order_item_id IS NULL;
    """)
    rows = cursor.fetchall()
    if not rows:
        print("Все товары хотя бы раз заказывали (это нормально для тестовых данных).")
    else:
        for row in rows:
            print(f"Товар {row[0]}: {row[1]}")

    conn.close()

if __name__ == "__main__":
    test_joins()