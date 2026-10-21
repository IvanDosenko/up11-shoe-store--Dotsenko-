import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")

# 1. Функция определения статуса клиента
def get_client_status(total_spent):
    if total_spent is None:
        return "Нет заказов"
    if total_spent > 20000:
        return "VIP"
    elif total_spent > 5000:
        return "Постоянный"
    else:
        return "Новичок"

# 2. Функция красивого вывода цены
def format_price(price):
    if price is None:
        return "0.00 руб."
    return f"{price:,.2f} руб.".replace(",", " ")

# 3. Функция проверки наличия на складе
def check_stock(quantity):
    if quantity > 0:
        return "В наличии"
    return "Нет в наличии"

def register_udfs():
    """Регистрирует функции в базе данных."""
    conn = sqlite3.connect(DB_PATH)
    
    # Регистрируем функции (название_в_SQL, кол-во_аргументов, питон_функция)
    conn.create_function("client_status", 1, get_client_status)
    conn.create_function("fmt_price", 1, format_price)
    conn.create_function("stock_status", 1, check_stock)
    
    print("[OK] Пользовательские функции зарегистрированы в БД.")
    return conn

if __name__ == "__main__":
    conn = register_udfs()
    
    # Демонстрация работы функции в SQL-запросе
    cursor = conn.cursor()
    print("\n--- Тест UDF: fmt_price ---")
    cursor.execute("SELECT name, fmt_price(price) FROM products LIMIT 3")
    for row in cursor.fetchall():
        print(row)
        
    print("\n--- Тест UDF: stock_status ---")
    cursor.execute("SELECT product_id, stock_status(total_stock) FROM view_products_with_stock LIMIT 3")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()