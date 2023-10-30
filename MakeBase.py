import psycopg2

# Підключення до сервера PostgreSQL
conn = psycopg2.connect(
    dbname="prog_comp",
    user="root",
    password="root",
    host="localhost",  # Адреса сервера PostgreSQL
    port="5432"
)

# Створення курсора для виконання SQL-запитів
cur = conn.cursor()

# Створення таблиці "Помилки"
cur.execute("""
    CREATE TABLE IF NOT EXISTS errors (
        error_code SERIAL PRIMARY KEY,
        error_description TEXT,
        error_date TIMESTAMP,
        error_severity TEXT,
        error_category TEXT,
        error_source TEXT
    )
""")

# Створення таблиці "Програмісти"
cur.execute("""
    CREATE TABLE IF NOT EXISTS programmers (
        programmer_code SERIAL PRIMARY KEY,
        last_name TEXT,
        first_name TEXT,
        phone_number TEXT
    )
""")

# Створення таблиці "Виправлення помилок"
cur.execute("""
    CREATE TABLE IF NOT EXISTS error_fixes (
        fix_code SERIAL PRIMARY KEY,
        error_code INT REFERENCES errors(error_code),
        fix_start_date TIMESTAMP,
        fix_duration INT,
        programmer_code INT REFERENCES programmers(programmer_code),
        work_cost NUMERIC
    )
""")

# Збереження змін у базі даних
conn.commit()

# Закриття підключення
cur.close()
conn.close()
