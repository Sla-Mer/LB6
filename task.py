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

# Функція для форматування дати та часу
def format_datetime(dt):
    return dt.strftime("%Y:%m:%d %H:%M:%S")

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
print("\n1. Всі критичні помилки з форматовою датою та часом:")
print(f"{'Опис помилки':<30} | {'Дата та час помилки':<30} | {'Рівень помилки':<30} | {'Категорія помилки':<30} | {'Джерело помилки':<30}")
print("-" * 154)
for row in formatted_critical_errors:
    print(f"{row[0]:<30} | {row[1]:<30} | {row[2]:<30} | {row[3]:<30} | {row[4]:<30}")

# Роздільник
print('-' * 100)

# 2. Порахувати кількість помилок кожного рівня (підсумковий запит)
cur.execute("""
    SELECT error_severity, COUNT(*) FROM errors GROUP BY error_severity;
""")
error_severity_counts = cur.fetchall()
print("\n2. Кількість помилок кожного рівня:")
print(f"{'Рівень помилки':<30} | {'Кількість помилок':<30}")
print("-" * 64)
for row in error_severity_counts:
    print(f"{row[0]:<30} | {row[1]:<30}")

# Роздільник
print('-' * 100)

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
print(f"{'Назва помилки':<30} | {'Програміст':<30} | {'Вартість за день':<30} | {'Вартість усього':<30}")
print("-" * 160)
for row in error_fix_costs:
    print(f"{row[0]:<30} | {row[1]:<30} | {row[2]:<30} | {row[3]:<30}")

# Роздільник
print('-' * 100)

# 4. Відобразити всі помилки, які надійшли із заданого джерела (запит з параметром)
source = 'користувач'  # Задайте бажане джерело тут

cur.execute("""
    SELECT 
        e.error_description, 
        to_char(e.error_date, 'YYYY:MM:DD HH24:MI:SS') as formatted_error_date, 
        e.error_severity, 
        e.error_category, 
        e.error_source
    FROM errors e
    WHERE e.error_source = %s;
""", (source,))
source_errors = cur.fetchall()
print(f"\n4. Помилки із джерела '{source}':")
print(f"{'Опис помилки':<30} | {'Дата та час помилки':<30} | {'Рівень помилки':<30} | {'Категорія помилки':<30} | {'Джерело помилки':<30}")
print("-" * 154)
for row in source_errors:
    print(f"{row[0]:<30} | {row[1]:<30} | {row[2]:<30} | {row[3]:<30} | {row[4]:<30}")


# Роздільник
print('-' * 100)

# 5. Порахувати кількість помилок, які надійшли від користувачів та тестувальників (підсумковий запит)
cur.execute("""
    SELECT error_source, COUNT(*) FROM errors WHERE error_source IN ('користувач', 'тестувальник') GROUP BY error_source;
""")
user_tester_counts = cur.fetchall()
print("\n5. Кількість помилок від користувачів та тестувальників:")
print(f"{'Джерело помилки':<30} | {'Кількість помилок':<30}")
print("-" * 64)
for row in user_tester_counts:
    print(f"{row[0]:<30} | {row[1]:<30}")

# Роздільник
print('-' * 100)

# 6. Порахувати кількість критичних, важливих, незначних помилок, виправлених кожним програмістом (перехресний запит)
cur.execute("""
    SELECT p.last_name || ' ' || p.first_name as programmer_name, 
        COUNT(CASE WHEN e.error_severity = 'критична' THEN 1 ELSE NULL END) AS critical_errors,
        COUNT(CASE WHEN e.error_severity = 'важлива' THEN 1 ELSE NULL END) AS important_errors,
        COUNT(CASE WHEN e.error_severity = 'незначна' THEN 1 ELSE NULL END) AS minor_errors
    FROM error_fixes ef
    JOIN programmers p ON ef.programmer_code = p.programmer_code
    JOIN errors e ON ef.error_code = e.error_code
    GROUP BY programmer_name;
""")
programmer_error_counts = cur.fetchall()
print("\n6. Кількість критичних, важливих, незначних помилок, виправлених кожним програмістом:")
print(f"{'Програміст':<30} | {'Критичні помилки':<30} | {'Важливі помилки':<30} | {'Незначні помилки':<30}")
print("-" * 115)
for row in programmer_error_counts:
    print(f"{row[0]:<30} | {row[1]:<30} | {row[2]:<30} | {row[3]:<30}")

# Закриття підключення до бази даних
cur.close()
conn.close()
