import psycopg2

# Підключення до сервера PostgreSQL
conn = psycopg2.connect(
    dbname="prog_comp",
    user="root",
    password="root",
    host="localhost",
    port="5432"
)

# Створення курсора
cur = conn.cursor()


# 1. Відобразити всі критичні помилки з форматованою датою та часом
cur.execute("""
    SELECT 
        e.error_description, 
        to_char(e.error_date, 'YYYY:MM:DD HH24:MI:SS') as formatted_error_date, 
        e.error_severity, 
        e.error_category, 
        e.error_source
    FROM errors e
    WHERE e.error_severity = 'критична'
    ORDER BY e.error_code;
""")
formatted_critical_errors = cur.fetchall()
print("\n1. Всі критичні помилки з форматованою датою та часом:")
for row in formatted_critical_errors:
    print(f"Опис помилки: {row[0]}, Дата та час помилки: {row[1]}, Рівень помилки: {row[2]}, Категорія помилки: {row[3]}, Джерело помилки: {row[4]}")


# 2. Порахувати кількість помилок кожного рівня (підсумковий запит)
cur.execute("""
    SELECT error_severity, COUNT(*) FROM errors GROUP BY error_severity;
""")
error_severity_counts = cur.fetchall()
print("\n2. Кількість помилок кожного рівня:")
for row in error_severity_counts:
    print(f"Рівень помилки: {row[0]}, Кількість помилок: {row[1]}")

# 3. Порахувати вартість роботи програміста при виправленні кожної помилки (запит з обчислювальним полем)
cur.execute("""
    SELECT e.error_description, p.last_name || ' ' || p.first_name AS programmer_full_name,
           ef.work_cost, ef.work_cost * ef.fix_duration AS cost_per_hour
    FROM error_fixes ef
    JOIN programmers p ON ef.programmer_code = p.programmer_code
    JOIN errors e ON ef.error_code = e.error_code;
""")
error_fix_costs = cur.fetchall()
print("\n3. Вартість роботи програміста при виправленні кожної помилки:")
for row in error_fix_costs:
    print(f"Назва помилки: {row[0]}, Прізвище та Ім'я програміста: {row[1]}, Вартість за день: {row[2]}, Вартість усього: {row[3]}")



# 4. Відобразити всі помилки з форматованою датою та часом
cur.execute("""
    SELECT 
        e.error_description, 
        to_char(e.error_date, 'YYYY:MM:DD HH24:MI:SS') as formatted_error_date, 
        e.error_severity, 
        e.error_category, 
        e.error_source
    FROM errors e;
""")
formatted_errors = cur.fetchall()
print("\n4. Помилки з форматованою датою та часом:")
for row in formatted_errors:
    print(f"Опис помилки: {row[0]}, Дата та час помилки: {row[1]}, Рівень помилки: {row[2]}, Категорія помилки: {row[3]}, Джерело помилки: {row[4]}")


# 5. Порахувати кількість помилок, які надійшли від користувачів та тестувальників (підсумковий запит)
cur.execute("""
    SELECT error_source, COUNT(*) FROM errors WHERE error_source IN ('користувач', 'тестувальник') GROUP BY error_source;
""")
user_tester_counts = cur.fetchall()
print("\n5. Кількість помилок від користувачів та тестувальників:")
for row in user_tester_counts:
    print(f"Джерело помилки: {row[0]}, Кількість помилок: {row[1]}")

# 6. Порахувати кількість критичних, важливих, незначних помилок, виправлених кожним програмістом (перехресний запит)
cur.execute("""
    SELECT p.last_name, p.first_name, 
        COUNT(CASE WHEN e.error_severity = 'критична' THEN 1 ELSE NULL END) AS critical_errors,
        COUNT(CASE WHEN e.error_severity = 'важлива' THEN 1 ELSE NULL END) AS important_errors,
        COUNT(CASE WHEN e.error_severity = 'незначна' THEN 1 ELSE NULL END) AS minor_errors
    FROM error_fixes ef
    JOIN programmers p ON ef.programmer_code = p.programmer_code
    JOIN errors e ON ef.error_code = e.error_code
    GROUP BY p.last_name, p.first_name;
""")
programmer_error_counts = cur.fetchall()
print("\n6. Кількість критичних, важливих, незначних помилок, виправлених кожним програмістом:")
for row in programmer_error_counts:
    print(f"Програміст: {row[0]} {row[1]}, Кількість критичних помилок: {row[2]}, Кількість важливих помилок: {row[3]}, Кількість незначних помилок: {row[4]}")

# Закриття підключення до бази даних
cur.close()
conn.close()