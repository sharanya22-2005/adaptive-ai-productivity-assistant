# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.store import add_task, get_tasks
from backend.scheduler import generate_schedule
from ai_module.insights import generate_insights
from alarm_chatbot.chatbot import chatbot
from alarm_chatbot.alarm import start_alarm
from ai_module.insights import generate_insights
from ai_module.predictions import TimePredictor
from ai_module.recommendations import AITimeManager


app = FastAPI()
predictor = TimePredictor()
ai_manager = AITimeManager()
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

@app.get("/insights")
def insights_api():
    return generate_insights()

@app.get("/train")
def train_api(task: str, time: float):
    predictor.update(task, time)
    return {"message": "Model updated successfully"}

@app.get("/log-task")
def log_task(task: str, start: str, end: str, planned: float):
    ai_manager.log_task(task, start, end, planned)
    return {"message": "Task logged"}

@app.get("/recommend-ai")
def recommend_ai():
    return ai_manager.generate_recommendations()

@app.get("/procrastination")
def procrastination():
    return {"status": ai_manager.detect_procrastination()}