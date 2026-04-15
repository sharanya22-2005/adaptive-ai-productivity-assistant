# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.store import add_task, get_tasks
from backend.scheduler import generate_schedule
from ai_module.insights import generate_insights
from alarm_chatbot.chatbot import chatbot
from alarm_chatbot.alarm import start_alarm

app = FastAPI()

# ✅ Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running"}

# ➕ Add Task
@app.post("/add_task")
def add_task_api(task: dict):
    add_task(task)
    return {"message": "Task added"}

# 📋 Get Tasks
@app.get("/get_tasks")
def get_tasks_api():
    return get_tasks()

# 📅 Generate Schedule
@app.get("/schedule")
def schedule_api():
    tasks = get_tasks()
    return generate_schedule(tasks)

@app.get("/insights")
def insights_api():
    return generate_insights()

@app.get("/chat")
def chat_api(query: str):
    return {"response": chatbot(query)}

@app.get("/status")
def status():
    return {"status": "AI system active"}

@app.get("/alarm")
def alarm_api(time: str, task: str):
    start_alarm(time, task)
    return {"message": "Alarm set successfully"}