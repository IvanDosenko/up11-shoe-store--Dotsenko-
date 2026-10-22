import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")

def analyze_database():
    """Собирает статистику по базе данных."""
    if not os.path.exists(DB_PATH):
        print("[!] База данных не найдена.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Размер файла
    size_bytes = os.path.getsize(DB_PATH)
    size_kb = size_bytes / 1024
    print(f"=== АНАЛИЗ БАЗЫ ДАННЫХ ===")
    print(f"Размер файла: {size_kb:.2f} KB")

    # 2. Количество записей в таблицах
    tables = ["users", "products", "orders", "order_items", "stock_items", "audit_log"]
    print("\nКоличество записей:")
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f" - {table}: {count}")
        except sqlite3.OperationalError:
            print(f" - {table}: таблица не найдена")

    # 3. Список индексов
    print("\nСписок индексов:")
    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    for row in cursor.fetchall():
        print(f" - {row[0]} (на таблице {row[1]})")

    conn.close()

if __name__ == "__main__":
    analyze_database()