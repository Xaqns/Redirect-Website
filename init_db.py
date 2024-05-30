import sqlite3

conn = sqlite3.connect('logs.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        ip TEXT,
        user_agent TEXT,
        timestamp TEXT
    )
''')
conn.commit()
conn.close()
