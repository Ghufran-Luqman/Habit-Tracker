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
c.execute("SELECT name FROM tasks ORDER BY id")
t = c.fetchall()
print(t)
conn.commit()
conn.close()