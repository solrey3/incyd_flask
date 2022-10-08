import sqlite3

connection = sqlite3.connect('test.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, email) VALUES ('Solito', 'chaoticgood@duck.com'), ('Johnny', 'johnny@example.com')")

# cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
#             ('Second Post', 'Content for the second post')
#             )

connection.commit()
connection.close()