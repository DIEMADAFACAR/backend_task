import sqlite3
import re
import os

# Определение абсолютного пути к базе данных
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/domains.db'))

# Подключение к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получение уникальных проектов из таблицы domains
cursor.execute("SELECT DISTINCT project_id FROM domains")
project_ids = [row[0] for row in cursor.fetchall()]

# Создание регулярных выражений для каждого проекта
for project_id in project_ids:
    cursor.execute("SELECT DISTINCT name FROM domains WHERE project_id=?", (project_id,))
    domains = [row[0] for row in cursor.fetchall()]

    # Генерация регулярного выражения для "мусорных" доменов
    regex_pattern = "|".join(re.escape(domain) for domain in domains)

    # Вставка регулярного выражения в таблицу rules
    cursor.execute("INSERT INTO rules (project_id, regexp) VALUES (?, ?)", (project_id, regex_pattern))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
