import shutil
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")
BACKUP_DIR = os.path.join(BASE_DIR, "db", "backups")

def create_backup():
    """Создает резервную копию базы данных."""
    if not os.path.exists(DB_PATH):
        print("[!] Файл базы данных не найден.")
        return

    # Создаем папку для бэкапов, если ее нет
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Генерируем имя файла с датой и временем
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(BACKUP_DIR, f"shoe_store_backup_{timestamp}.sqlite")
    
    try:
        shutil.copy2(DB_PATH, backup_path)
        print(f"[OK] Резервная копия создана: {backup_path}")
    except Exception as e:
        print(f"[ERROR] Ошибка при создании копии: {e}")

if __name__ == "__main__":
    create_backup()