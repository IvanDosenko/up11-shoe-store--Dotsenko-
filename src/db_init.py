import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")
SCHEMA_PATH = os.path.join(BASE_DIR, "db", "schema.sql")

def init_db():
    """Создает базу данных и таблицы из schema.sql."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    cursor.executescript(schema_sql)
    
    # Заполняем роли
    roles = [("admin",), ("manager",), ("user",), ("reader",)]
    cursor.executemany("INSERT OR IGNORE INTO roles (role_name) VALUES (?)", roles)

    # Заполняем базовые размеры (36-45)
    for size in range(36, 46):
        cursor.execute("INSERT OR IGNORE INTO sizes (size_value) VALUES (?)", (size,))
        
    conn.commit()
    conn.close()
    print(f"[OK] База данных успешно создана: {DB_PATH}")

if __name__ == "__main__":
    init_db()