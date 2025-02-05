import sqlite3

# создаем базу данных по выписке из банка
def create_database():
    conn = sqlite3.connect('transactions.db')
    # создаем курсор для запросов
    c = conn.cursor()
    # создаем саму таблицу с проверкой и указанием формата для каждой величины
    c.execute('''CREATE DATABASE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, category TEXT, amount REAL, description TEXT)''')
    # сохраняем изменения
    conn.commit()
    # закрываем соединение, чтобы не было утечек
    conn.close()


# ОСНОВНОЙ КОД
print('start')
create_database()
print('finish')