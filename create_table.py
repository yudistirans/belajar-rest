import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS products (product_id INTEGER PRIMARY KEY, product_name TEXT, product_description TEXT, product_price INTEGER)"
cursor.execute(create_table)

products = [
    (1, 'Ayam', 'Ayam adalah', 30000),
    (2, 'Telor', 'Telor adalah', 20000),
    (3, 'Sosis', 'Sosis adalah', 25000)
]
insert_query = "INSERT INTO products VALUES (?, ?, ?, ?)"
cursor.executemany(insert_query, products)

connection.commit()

connection.close()