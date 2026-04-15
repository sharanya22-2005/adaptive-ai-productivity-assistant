import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.cluster import KMeans

class AITimeManager:
    def __init__(self):
        self.data = pd.DataFrame(columns=[
            "task", "start_time", "end_time", "duration",
            "planned_duration", "completed", "timestamp"
        ])

    # -------------------------------
    # 1. Add Task Data
    # -------------------------------
    def log_task(self, task, start_time, end_time, planned_duration, completed=True):
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")

        duration = (end - start).seconds / 60  # in minutes

        entry = {
            "task": task,
            "start_time": start.hour,
            "end_time": end.hour,
            "duration": duration,
            "planned_duration": planned_duration,
            "completed": int(completed),
            "timestamp": datetime.now()
        }

        self.data = pd.concat([self.data, pd.DataFrame([entry])], ignore_index=True)

    # -------------------------------
    # 2. Detect Productivity Patterns
    # -------------------------------
    def analyze_productivity(self):
        if len(self.data) < 5:
            print("Not enough data yet.")
            return None

        df = self.data.copy()

        # Efficiency score
        df["efficiency"] = df["planned_duration"] / df["duration"]
        df["efficiency"] = df["efficiency"].clip(upper=2)

        # Use clustering to detect patterns
        X = df[["start_time", "efficiency"]]

        kmeans = KMeans(n_clusters=3, random_state=42)
        df["cluster"] = kmeans.fit_predict(X)

        return df

    # -------------------------------
    # 3. Detect Procrastination
    # -------------------------------
    def detect_procrastination(self):
        if len(self.data) == 0:
            return "No data yet"

        df = self.data.copy()
        df["delay"] = df["duration"] - df["planned_duration"]

        score = df["delay"].mean()

        if score > 10:
            return "High procrastination detected 🚨"
        elif score > 0:
            return "Moderate procrastination ⚠️"
        else:
            return "Good time discipline ✅"
       

    # -------------------------------
    # 4. Generate Smart Recommendations
    # -------------------------------
    def generate_recommendations(self):
        df = self.analyze_productivity()

        if df is None:
            return "Add more task data first."

        recommendations = []

        # Best productivity hours
        best_hours = df.groupby("start_time")["efficiency"].mean().idxmax()
        recommendations.append(f"🔥 Your most productive hour is around {best_hours}:00")

        # Worst hours
        worst_hours = df.groupby("start_time")["efficiency"].mean().idxmin()
        recommendations.append(f"⚠️ Avoid heavy tasks around {worst_hours}:00")

        # Procrastination insight
        procrastination = self.detect_procrastination()
        recommendations.append(f"🧠 {procrastination}")

        # Task duration correction
        avg_delay = (df["duration"] - df["planned_duration"]).mean()

        if avg_delay > 5:
            recommendations.append("⏳ You underestimate tasks. Add buffer time (+10-20%).")
        elif avg_delay < -5:
            recommendations.append("⚡ You overestimate tasks. Tighten schedules.")

        # Focus suggestion
        avg_duration = df["duration"].mean()
        if avg_duration > 90:
            recommendations.append("🧘 Take breaks every 60-90 mins for better focus.")
        else:
            recommendations.append("🚀 Good short focus cycles. Maintain it.")

        return "\n".join(recommendations)

