# main.py
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports
from store import add_task, get_tasks, delete_task_by_name, mark_task_complete
from scheduler import generate_schedule
from ai_module.insights import generate_insights
from alarm_chatbot.chatbot import chatbot

app = FastAPI()

# ✅ CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- ROOT --------------------
@app.get("/")
def home():
    return {"message": "Backend running"}

# -------------------- TASK APIs --------------------

# ➕ Add Task
@app.post("/add_task")
def add_task_api(task: dict):
    add_task(task)
    return {"message": "Task added", "task": task}

# 📋 Get Tasks
@app.get("/get_tasks")
def get_tasks_api():
    return get_tasks()

# ❌ Delete Task
@app.delete("/delete_task/{task_name}")
def delete_task_api(task_name: str):
    result = delete_task_by_name(task_name)
    if result:
        return {"message": f"{task_name} deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

# ✅ Complete Task
@app.post("/complete_task/{task_name}")
def complete_task_api(task_name: str):
    result = mark_task_complete(task_name)
    if result:
        return {"message": f"{task_name} completed, streak updated"}
    raise HTTPException(status_code=404, detail="Task not found")

# -------------------- AI SCHEDULING --------------------

@app.get("/schedule")
def schedule_api(ai_level: int = 50):
    """
    AI-based scheduling with sensitivity level
    """
    tasks = get_tasks()

    # 🔥 Add AI logic here
    for task in tasks:
        if ai_level > 70 and task.get("priority") == "Low":
            task["time"] += 1

        if ai_level > 80 and task.get("priority") == "High":
            task["time"] -= 1

    scheduled = sorted(tasks, key=lambda x: x["time"])
    return scheduled

# -------------------- AI INSIGHTS --------------------

@app.get("/insights")
def insights_api():
    return generate_insights()

# -------------------- CHAT ORCHESTRATOR --------------------

@app.get("/chat")
def chat_api(query: str):
    """
    Chatbot + system control
    """
    tasks = get_tasks()
    response = chatbot(query)

    # 🔥 ADD SYSTEM ACTIONS FROM CHAT
    query_lower = query.lower()

    if "reschedule" in query_lower and tasks:
        tasks[0]["time"] += 1
        return {
            "response": "Meeting rescheduled by 1 hour",
            "action": "rescheduled"
        }

    if "complete" in query_lower and tasks:
        mark_task_complete(tasks[0]["title"])
        return {
            "response": "Task marked as complete",
            "action": "completed"
        }

    return {"response": response}

# -------------------- STATUS --------------------

@app.get("/status")
def status():
    return {"status": "AI system active"}