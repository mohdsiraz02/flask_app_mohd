import sqlite3

# 🔹 Connect to SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# 🔹 Create reservations table if not exists
c.execute('''
CREATE TABLE IF NOT EXISTS reservations (
    reservation_no TEXT PRIMARY KEY,
    date TEXT,
    name TEXT,
    status TEXT
)
''')

# 🔹 Create moved_reservations table if not exists
c.execute('''
CREATE TABLE IF NOT EXISTS moved_reservations (
    reservation_no TEXT PRIMARY KEY,
    date TEXT,
    name TEXT,
    status TEXT
)
''')

# 🔹 Insert initial reservation data
sample_reservations = [
    ('R123', '2025-07-12', 'Alice', 'confirmed'),
    ('R124', '2025-07-12', 'Bob', 'pending')
]

# ❗ Use INSERT OR IGNORE to prevent duplicates if re-run
c.executemany("INSERT OR IGNORE INTO reservations VALUES (?, ?, ?, ?)", sample_reservations)

# 🔹 Commit & close connection
conn.commit()
conn.close()