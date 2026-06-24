import sqlite3

conn = sqlite3.connect("talentvault.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    mobile TEXT,
    city TEXT,
    designation TEXT,
    experience INTEGER,
    qualification TEXT,
    position TEXT,
    skills TEXT,
    resume_path TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")