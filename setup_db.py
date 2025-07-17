import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS reservations (
    reservation_no TEXT,
    date TEXT,
    name TEXT,
    status TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS moved_reservations (
    reservation_no TEXT,
    date TEXT,
    name TEXT,
    status TEXT
)
''')

c.execute("INSERT INTO reservations VALUES ('R123', '2025-07-12', 'Alice', 'confirmed')")
c.execute("INSERT INTO reservations VALUES ('R124', '2025-07-12', 'Bob', 'pending')")

conn.commit()
conn.close()