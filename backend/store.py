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
tasks = []

def add_task(task):
    tasks.append(task)

def get_tasks():
    return tasks

# ✅ DELETE TASK
def delete_task_by_name(name):
    global tasks
    for t in tasks:
        if t["title"].lower() == name.lower():
            tasks.remove(t)
            return True
    return False

# ✅ COMPLETE TASK
def mark_task_complete(name):
    for t in tasks:
        if t["title"].lower() == name.lower():
            t["status"] = "completed"
            return True
    return False