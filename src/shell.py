import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")

def run_shell():
    """Консольный интерфейс для работы с базой."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    current_user = None
    current_role = None

    print("=== Добро пожаловать в консоль 'Чудо Обувь' ===")
    print("Доступные команды: login <логин>, view_orders, view_stock, exit")

    while True:
        cmd = input(f"\n[{current_role or 'guest'}]> ").strip().split()
        if not cmd:
            continue

        action = cmd[0].lower()

        if action == "exit":
            print("Выход...")
            break

        elif action == "login":
            if len(cmd) < 2:
                print("Укажите логин: login admin")
                continue
            
            login = cmd[1]
            cursor.execute("""
                SELECT u.first_name, r.role_name 
                FROM users u 
                JOIN roles r ON u.role_id = r.role_id 
                WHERE u.login = ?
            """, (login,))
            user = cursor.fetchone()
            
            if user:
                current_user = user[0]
                current_role = user[1]
                print(f"Вы вошли как {current_user} (Роль: {current_role})")
            else:
                print("Пользователь не найден.")

        elif action == "view_orders":
            if not current_role:
                print("Ошибка: Сначала авторизуйтесь (login admin).")
                continue
            print("\n--- Список заказов ---")
            cursor.execute("SELECT * FROM view_orders_with_clients LIMIT 10")
            for row in cursor.fetchall():
                print(row)

        elif action == "view_stock":
            print("\n--- Остатки на складе ---")
            cursor.execute("SELECT category, name, total_stock FROM view_products_with_stock LIMIT 10")
            for row in cursor.fetchall():
                print(row)

        else:
            print("Неизвестная команда.")

    conn.close()

if __name__ == "__main__":
    run_shell()