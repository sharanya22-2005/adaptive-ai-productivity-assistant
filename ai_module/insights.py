import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# -----------------------------
# Data Storage
# -----------------------------
data_file = "productivity_data.csv"

try:
    df = pd.read_csv(data_file)
except:
    df = pd.DataFrame(columns=[
        "task", "category", "start_time", "end_time",
        "duration", "delay", "hour"
    ])

# -----------------------------
# Task Logger
# -----------------------------
def log_task(task, category, start_time, end_time, delay):
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")

    duration = (end - start).seconds / 60
    hour = start.hour

    new_entry = {
        "task": task,
        "category": category,
        "start_time": start_time,
        "end_time": end_time,
        "duration": duration,
        "delay": delay,
        "hour": hour
    }

    global df
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(data_file, index=False)

    print("✅ Task logged successfully!")

# -----------------------------
# Productivity Analysis
# -----------------------------
def analyze_productivity():
    if len(df) < 5:
        print("⚠️ Not enough data yet.")
        return

    print("\n📊 Productivity Insights:\n")

    # Peak hours
    peak_hour = df.groupby("hour")["duration"].mean().idxmax()
    print(f"🔥 Peak productivity hour: {peak_hour}:00")

    # Procrastination detection
    avg_delay = df["delay"].mean()
    print(f"⏳ Average delay before starting tasks: {avg_delay:.2f} mins")

    if avg_delay > 15:
        print("⚠️ You tend to procrastinate before tasks.")

    # Category performance
    category_perf = df.groupby("category")["duration"].mean()
    print("\n📂 Productivity by Category:")
    print(category_perf)

# -----------------------------
# ML Prediction Model
# -----------------------------
def train_model():
    if len(df) < 10:
        print("⚠️ Not enough data to train model.")
        return None

    X = df[["hour", "delay"]]
    y = df["duration"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    print("🤖 Model trained successfully!")
    return model

# -----------------------------
# Predict Task Efficiency
# -----------------------------
def predict_duration(model, hour, delay):
    prediction = model.predict([[hour, delay]])
    print(f"⏱️ Predicted task duration: {prediction[0]:.2f} minutes")

# -----------------------------
# Procrastination Detector
# -----------------------------
def detect_procrastination():
    procrastinated = df[df["delay"] > 20]

    if len(procrastinated) > len(df) * 0.4:
        print("🚨 High procrastination pattern detected!")
    else:
        print("✅ Procrastination under control.")

# -----------------------------
# Smart Recommendations
# -----------------------------
def generate_insights():
    print("\n🧠 Smart Insights:\n")

    peak_hour = df.groupby("hour")["duration"].mean().idxmax()

    print(f"👉 Schedule important tasks around {peak_hour}:00")

    if df["delay"].mean() > 15:
        print("👉 Use 5-minute rule to overcome procrastination")

    low_perf_hour = df.groupby("hour")["duration"].mean().idxmin()
    print(f"👉 Avoid heavy tasks at {low_perf_hour}:00")

# -----------------------------
# CLI Interface
# -----------------------------
def menu():
    while True:
        print("\n=== AI Time Manager ===")
        print("1. Log Task")
        print("2. Analyze Productivity")
        print("3. Train AI Model")
        print("4. Predict Task Duration")
        print("5. Detect Procrastination")
        print("6. Generate Insights")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == "1":
            task = input("Task: ")
            category = input("Category: ")
            start = input("Start time (HH:MM): ")
            end = input("End time (HH:MM): ")
            delay = float(input("Delay before starting (mins): "))
            log_task(task, category, start, end, delay)

        elif choice == "2":
            analyze_productivity()

        elif choice == "3":
            global model
            model = train_model()

        elif choice == "4":
            hour = int(input("Hour of task: "))
            delay = float(input("Expected delay: "))
            predict_duration(model, hour, delay)

        elif choice == "5":
            detect_procrastination()

        elif choice == "6":
            generate_insights()

        elif choice == "7":
            break

        else:
            print("Invalid choice")

# Run system
menu()