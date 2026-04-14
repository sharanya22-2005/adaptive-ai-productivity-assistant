import sqlite3

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    priority TEXT,
    duration INTEGER
)
""")

conn.commit()


# ✅ THIS FUNCTION MUST EXIST
def add_task(task):
    cursor.execute(
        "INSERT INTO tasks (name, priority, duration) VALUES (?, ?, ?)",
        (task["name"], task["priority"], task["duration"])
    )
    conn.commit()


# ✅ THIS FUNCTION MUST EXIST
def get_tasks():
    cursor.execute("SELECT name, priority, duration FROM tasks")
    rows = cursor.fetchall()

    return [
        {"name": r[0], "priority": r[1], "duration": r[2]}
        for r in rows
    ]