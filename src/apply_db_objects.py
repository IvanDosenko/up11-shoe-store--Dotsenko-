import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")
VIEWS_PATH = os.path.join(BASE_DIR, "db", "views_indexes.sql")
TRIGGERS_PATH = os.path.join(BASE_DIR, "db", "triggers.sql")

def apply_objects():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Загрузка VIEWS...")
    with open(VIEWS_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    print("Загрузка TRIGGERS...")
    with open(TRIGGERS_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print("[OK] Представления и триггеры успешно загружены в базу!")

if __name__ == "__main__":
    apply_objects() 