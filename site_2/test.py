# test.py
import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Проверим, есть ли таблица Tovar
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print("Существующие таблицы:", [t[0] for t in tables])

# Проверим структуру Tovar
print("\nСтруктура таблицы Tovar:")
cur.execute("PRAGMA table_info(Tovar)")
columns = cur.fetchall()
for col in columns:
    print(f"  {col[0]}: '{col[1]}' (тип: {col[2]})")

# Проверим, есть ли данные
cur.execute("SELECT COUNT(*) FROM Tovar")
count = cur.fetchone()[0]
print(f"\nКоличество записей в Tovar: {count}")

if count > 0:
    print("\nПервая запись:")
    cur.execute("SELECT * FROM Tovar LIMIT 1")
    row = cur.fetchone()
    for i, val in enumerate(row):
        print(f"  {columns[i][1]} = {val}")

conn.close()