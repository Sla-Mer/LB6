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


# Виведення даних з таблиці "Помилки" з відповідними значеннями
cur.execute("""
    SELECT 
        e.error_code,
        e.error_description, 
        to_char(e.error_date, 'YYYY:MM:DD HH24:MI:SS') as formatted_error_date, 
        e.error_severity, 
        e.error_category, 
        e.error_source
    FROM errors e;
""")
error_data = cur.fetchall()
print("Дані з таблиці 'Помилки':")
# Додавання заголовків з роздільниками та вирівнюванням до 30 символів
print(f"{'Код':<30} | {'Назва Помилки':<30} | {'Дата Помилки':<30} | {'Рівень Помилки':<30} | {'Категорія Помилки':<30} | {'Джерело Помилки':<30}")
for row in error_data:
    formatted_row = [str(val).ljust(30) for val in row]
    print(" | ".join(formatted_row))

# Виведення даних з таблиці "Програмісти" з відповідними значеннями
cur.execute("""
    SELECT 
        p.programmer_code,
        p.last_name, 
        p.first_name, 
        p.phone_number
    FROM programmers p;
""")
programmer_data = cur.fetchall()
print("\nДані з таблиці 'Програмісти':")
# Додавання заголовків з роздільниками та вирівнюванням до 30 символів
print(f"{'Код':<30} | {'Прізвище програміста':<30} | {'Імя програміста':<30} | {'Телефон програміста':<30}")
for row in programmer_data:
    formatted_row = [str(val).ljust(30) for val in row]
    print(" | ".join(formatted_row))

# Виведення даних з таблиці "Виправлення помилок" з відповідними значеннями, включаючи інформацію про помилку та програміста
cur.execute("""
    SELECT 
        e.error_description, 
        p.last_name AS programmer_last_name, 
        p.first_name AS programmer_first_name, 
        to_char(ef.fix_start_date, 'YYYY:MM:DD HH24:MI:SS') as formatted_fix_start_date, 
        ef.fix_duration, 
        ef.work_cost
    FROM error_fixes ef
    JOIN errors e ON ef.error_code = e.error_code
    JOIN programmers p ON ef.programmer_code = p.programmer_code;
""")
error_fix_data = cur.fetchall()
print("\nДані з таблиці 'Виправлення помилок':")
# Додавання заголовків з роздільниками та вирівнюванням до 30 символів
print(f"{'Назва Помилки':<30} | {'Прізвище програміста':<30} | {'Імя програміста':<30} | {'Дата початку виправлення':<30} | {'Тривалість виправлення (дн)':<30} | {'Вартість роботи':<30}")
for row in error_fix_data:
    formatted_row = [str(val).ljust(30) for val in row]
    print(" | ".join(formatted_row))

# Закриття підключення до бази даних
cur.close()
conn.close()