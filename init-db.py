import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO data (rate, currentbal) VALUES (?, ?)", ('1500', '1500'))
cur.execute("INSERT INTO transactions (detail, amount) VALUES (?, ?)", ('Tacos 🌮', "500"))

connection.commit()
connection.close()