import psycopg2

# Підключення до сервера PostgreSQL
conn = psycopg2.connect(
    dbname="prog_comp",
    user="root",
    password="root",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Запити на видалення таблиць
cur.execute("DROP TABLE IF EXISTS error_fixes;")
cur.execute("DROP TABLE IF EXISTS programmers;")
cur.execute("DROP TABLE IF EXISTS errors;")

# Підтвердження та закриття підключення
conn.commit()
cur.close()
conn.close()