# Как работать с SQLite базами данных

## Способ 1: Командная строка SQLite (везде)

### Установка SQLite

**Windows:**
1. Скачайте с https://www.sqlite.org/download.html
2. Файл: `sqlite-tools-win32-x86-*.zip`
3. Распакуйте в папку (например, `C:\sqlite`)
4. Добавьте путь в PATH или используйте полный путь

**Или используйте через Python (уже установлен):**
```powershell
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

### Основные команды SQLite

**Открыть базу данных:**
```bash
sqlite3 data/releases_database.db
```

**Внутри SQLite:**

```sql
-- Показать все таблицы
.tables

-- Показать структуру таблицы
.schema releases

-- Включить заголовки колонок
.headers on

-- Включить красивый вывод
.mode column

-- Выполнить запрос
SELECT * FROM releases LIMIT 5;

-- Количество записей
SELECT COUNT(*) FROM releases;

-- Фильтрация
SELECT project_id, version, published_at
FROM releases
WHERE project_id = 'kubernetes'
LIMIT 10;

-- Поиск
SELECT * FROM releases
WHERE description LIKE '%security%';

-- Сортировка
SELECT project_id, version, importance_score
FROM releases
ORDER BY importance_score DESC
LIMIT 10;

-- Выход
.quit
```

### Полезные команды .mode

```sql
.mode column    -- Колонки (красиво)
.mode line      -- По строкам (детально)
.mode csv       -- CSV формат
.mode json      -- JSON формат
.mode markdown  -- Markdown таблица
```

## Способ 2: Python скрипт

Создайте файл `query.py`:

```python
import sqlite3

# Подключиться к базе
conn = sqlite3.connect('data/releases_database.db')
cursor = conn.cursor()

# Выполнить запрос
cursor.execute('SELECT * FROM releases LIMIT 5')
rows = cursor.fetchall()

# Вывести результаты
for row in rows:
    print(row)

# Закрыть соединение
conn.close()
```

Запустить:
```bash
python query.py
```

## Способ 3: GUI программы (визуально)

### DB Browser for SQLite (лучший выбор)

**Установка:**
1. Скачать: https://sqlitebrowser.org/dl/
2. Установить
3. Открыть: File → Open Database → выбрать `data/releases_database.db`

**Возможности:**
- Визуальный просмотр таблиц
- Редактирование данных
- Выполнение SQL запросов
- Экспорт в CSV, JSON
- Графики и статистика

### DBeaver (универсальный)

**Установка:**
1. Скачать: https://dbeaver.io/download/
2. Установить
3. New Connection → SQLite → выбрать файл базы

**Возможности:**
- Работа с любыми БД
- ER-диаграммы
- Экспорт/импорт
- Визуальный query builder

## Способ 4: VS Code расширение

**Установка:**
1. Открыть VS Code
2. Extensions → искать "SQLite"
3. Установить "SQLite" by alexcvzz

**Использование:**
1. Открыть файл .db в VS Code
2. Правая кнопка → "Open Database"
3. В левой панели появится SQLITE EXPLORER
4. Можно выполнять запросы

## Примеры запросов для наших баз

### Releases Database

```sql
-- Топ-10 проектов по количеству релизов
SELECT project_id, COUNT(*) as count
FROM releases
GROUP BY project_id
ORDER BY count DESC
LIMIT 10;

-- Релизы с высоким importance_score
SELECT project_id, version, importance_score, published_at
FROM releases
WHERE importance_score > 8
ORDER BY importance_score DESC;

-- Релизы по месяцам 2025
SELECT
    strftime('%Y-%m', published_at) as month,
    COUNT(*) as count
FROM releases
WHERE strftime('%Y', published_at) = '2025'
GROUP BY month
ORDER BY month;

-- Релизы с security fix
SELECT project_id, version, name_ru
FROM releases
WHERE has_security_fix = 1
ORDER BY published_at DESC
LIMIT 20;

-- Поиск по описанию
SELECT project_id, version, description_ru
FROM releases
WHERE description_ru LIKE '%безопасность%'
OR description_ru LIKE '%уязвимость%';
```

### News Database

```sql
-- Топ-20 новостей по важности
SELECT title_ru, importance, pub_date
FROM news
ORDER BY importance DESC
LIMIT 20;

-- Новости по категориям
SELECT category, COUNT(*) as count
FROM news
GROUP BY category
ORDER BY count DESC;

-- Свежие новости за последние 30 дней
SELECT title_ru, source, pub_date
FROM news
WHERE pub_date >= date('now', '-30 days')
ORDER BY pub_date DESC;

-- Поиск по ключевым словам
SELECT title_ru, link
FROM news
WHERE title LIKE '%kubernetes%'
OR description LIKE '%kubernetes%';

-- Статистика по источникам
SELECT source, COUNT(*) as count
FROM news
GROUP BY source
ORDER BY count DESC;
```

### CVE Database

```sql
-- Критические уязвимости
SELECT cve_id, title, cvss_score, cvss_severity
FROM cve_vulnerabilities
WHERE cvss_severity = 'CRITICAL'
ORDER BY cvss_score DESC;

-- CVE с exploits
SELECT v.cve_id, v.title, v.cvss_score, e.exploit_url
FROM cve_vulnerabilities v
JOIN cve_exploits e ON v.cve_id = e.cve_id
WHERE e.exploit_exists = 1
ORDER BY v.intelligent_score DESC;

-- CVE по проектам
SELECT p.project_name, COUNT(*) as cve_count
FROM cve_affected_projects p
GROUP BY p.project_name
ORDER BY cve_count DESC;

-- Kubernetes уязвимости
SELECT v.cve_id, v.title, v.cvss_score
FROM cve_vulnerabilities v
JOIN cve_affected_projects p ON v.cve_id = p.cve_id
WHERE p.project_name = 'kubernetes'
ORDER BY v.intelligent_score DESC;
```

### Access Control Database

```sql
-- Логи скачиваний
SELECT username, database_name, download_date, download_time
FROM download_log
ORDER BY created_at DESC
LIMIT 20;

-- Топ пользователей
SELECT username, first_name, COUNT(*) as downloads
FROM download_log
GROUP BY user_id
ORDER BY downloads DESC;

-- Статистика по дням
SELECT download_date, COUNT(*) as downloads
FROM download_log
GROUP BY download_date
ORDER BY download_date DESC;
```

## Быстрый старт

### Вариант 1: Python (уже установлен)

```powershell
# Открыть базу
python -c "import sqlite3; conn = sqlite3.connect('data/releases_database.db'); conn.row_factory = sqlite3.Row; c = conn.cursor(); c.execute('SELECT * FROM releases LIMIT 5'); [print(dict(row)) for row in c.fetchall()]"
```

### Вариант 2: Интерактивный режим Python

```powershell
python
```

```python
import sqlite3

# Подключиться
conn = sqlite3.connect('data/releases_database.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Запрос
c.execute('SELECT * FROM releases LIMIT 5')

# Вывести
for row in c.fetchall():
    print(dict(row))

# Или так
c.execute('SELECT COUNT(*) FROM releases')
print(f"Всего релизов: {c.fetchone()[0]}")
```

### Вариант 3: Создать скрипт query_easy.py

```python
import sqlite3
import sys

db = sys.argv[1] if len(sys.argv) > 1 else 'data/releases_database.db'
query = sys.argv[2] if len(sys.argv) > 2 else 'SELECT * FROM sqlite_master'

conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute(query)
for row in c.fetchall():
    print(dict(row))

conn.close()
```

Использование:
```powershell
# Показать таблицы
python query_easy.py data/releases_database.db "SELECT name FROM sqlite_master WHERE type='table'"

# Топ-10 релизов
python query_easy.py data/releases_database.db "SELECT * FROM releases LIMIT 10"
```

## Рекомендации

**Для начинающих:**
1. DB Browser for SQLite - самый простой GUI
2. Не нужно учить команды, все визуально

**Для продвинутых:**
1. Python скрипты - для автоматизации
2. SQLite CLI - для быстрых запросов

**Для аналитики:**
1. DBeaver - мощные возможности
2. Jupyter Notebook + pandas - для анализа

## Шпаргалка SQL

```sql
-- Выбрать все
SELECT * FROM table_name;

-- Выбрать колонки
SELECT column1, column2 FROM table_name;

-- С условием
SELECT * FROM table_name WHERE column1 = 'value';

-- Сортировка
SELECT * FROM table_name ORDER BY column1 DESC;

-- Лимит
SELECT * FROM table_name LIMIT 10;

-- Группировка
SELECT column1, COUNT(*)
FROM table_name
GROUP BY column1;

-- Join
SELECT t1.*, t2.column
FROM table1 t1
JOIN table2 t2 ON t1.id = t2.id;

-- Поиск
SELECT * FROM table_name
WHERE column LIKE '%keyword%';

-- Подсчет
SELECT COUNT(*) FROM table_name;

-- Уникальные значения
SELECT DISTINCT column FROM table_name;
```

## Ссылки

- SQLite документация: https://www.sqlite.org/docs.html
- DB Browser: https://sqlitebrowser.org/
- DBeaver: https://dbeaver.io/
- SQL Tutorial: https://www.w3schools.com/sql/

---

**Совет:** Начните с DB Browser for SQLite - это самый простой способ увидеть и понять структуру баз данных!
