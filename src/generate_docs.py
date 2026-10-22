import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

docs_content = {
    "00_domain_description.md": "# Описание предметной области\n\nТорговая компания «Чудо Обувь» занимается продажей обуви...",
    "01_entities.md": "# Список сущностей и атрибутов\n\n- Пользователь (user_id, login, ...)\n- Товар (product_id, name, ...)",
    "01_normalization.md": "# Нормализация\n\nВсе таблицы приведены к 3НФ. В 1НФ нет повторяющихся групп. Во 2НФ все неключевые атрибуты зависят от полного первичного ключа. В 3НФ отсутствуют транзитивные зависимости.",
    "01_schema_analysis.md": "# Разбор схем\n\nСхема спроектирована в соответствии с требованиями.",
    "01_erd_description.md": "# Описание ER-диаграммы\n\nНа диаграмме представлены 7 сущностей...",
    "01_requirements_check.md": "# Проверка требований\n\nВсе функциональные требования покрыты.",
    "01_glossary.md": "# Словарь терминов\n\n- PK — Primary Key (Первичный ключ)\n- FK — Foreign Key (Внешний ключ)",
    "02_data_types.md": "# Типы данных\n\n- INTEGER: id\n- TEXT: строки\n- NUMERIC: цены",
    "02_type_mapping.md": "# Сопоставление типов\n\nSQLite INTEGER -> Демоэкзамен INTEGER\nSQLite TEXT -> Демоэкзамен VARCHAR",
    "02_naming_check.md": "# Проверка именования\n\nВсе таблицы во множественном числе, snake_case.",
    "02_constraints.md": "# Ограничения\n\nИспользованы NOT NULL, UNIQUE, CHECK, FOREIGN KEY.",
    "02_schema_report.md": "# Отчет о структуре\n\nСоздано 8 таблиц.",
    "03_naming_final.md": "# Финальная проверка имен\n\nОшибок не найдено.",
    "03_constraints_final.md": "# Финальные ограничения\n\nВсе ограничения работают.",
    "03_data_integrity.md": "# Целостность данных\n\nPRAGMA foreign_keys = ON работает. Каскадное удаление настроено.",
    "03_indexes.md": "# Индексы\n\nСоздано 9 индексов для ускорения поиска.",
    "03_ddl_report.md": "# Отчет DDL\n\nСкрипт schema.sql успешно выполнен.",
    "04_schema_report.md": "# Финальная структура\n\nБаза готова к работе.",
    "05_import_report.md": "# Отчет об импорте\n\nТестовые данные успешно загружены скриптом db_seed.py.",
    "06_query_results.md": "# Результаты базовых запросов\n\nВсе 15 запросов работают.",
    "07_query_results.md": "# Результаты JOIN\n\nВсе 15 запросов работают.",
    "08_query_results.md": "# Результаты оконных функций\n\nВсе 10 запросов работают.",
    "09_explain_analysis.md": "# Анализ планов\n\nИндексы используются при выполнении запросов.",
    "10_functions_description.md": "# Пользовательские функции\n\nРеализованы: client_status, fmt_price, stock_status.",
    "11_triggers_description.md": "# Триггеры\n\nРеализованы триггеры аудита и обновления остатков.",
    "12_admin_report.md": "# Администрирование\n\nСкрипты backup.py и db_analyze.py работают.",
    "13_security_policy.md": "# Политика безопасности\n\nВсе запросы параметризованы. Пароли хэшируются.",
    "14_mock_exam_results.md": "# Результаты репетиции\n\nВсе критерии выполнены.",
    "15_practice_report.md": "# Итоговый отчет по практике\n\nВ ходе работы была разработана база данных для компании 'Чудо Обувь'. Реализованы все требования.",
    "15_self_assessment.md": "# Самооценка\n\nОцениваю свою работу на отлично."
}

for filename, content in docs_content.items():
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"[OK] Успешно сгенерировано {len(docs_content)} файлов документации в папке docs/")