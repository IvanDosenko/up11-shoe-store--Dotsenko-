import shutil
import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "shoe_store.sqlite")
BACKUP_DIR = os.path.join(BASE_DIR, "db", "backups")

def restore_backup():
    """Восстанавливает базу данных из последней резервной копии."""
    backups = glob.glob(os.path.join(BACKUP_DIR, "*.sqlite"))
    if not backups:
        print("[!] Резервные копии не найдены.")
        return

    # Берем самый свежий бэкап
    latest_backup = max(backups, key=os.path.getctime)
    print(f"Найдена последняя копия: {latest_backup}")

    try:
        shutil.copy2(latest_backup, DB_PATH)
        print("[OK] База данных успешно восстановлена из резервной копии!")
    except Exception as e:
        print(f"[ERROR] Ошибка восстановления: {e}")

if __name__ == "__main__":
    restore_backup()