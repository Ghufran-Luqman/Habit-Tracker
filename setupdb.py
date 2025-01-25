import sqlite3
conn = sqlite3.connect("tasks.db")
c = conn.cursor()
'''
c.execute("""CREATE TABLE tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL UNIQUE,
          state INTEGER DEFAULT 0
          )""")
'''

conn.commit()
conn.close()