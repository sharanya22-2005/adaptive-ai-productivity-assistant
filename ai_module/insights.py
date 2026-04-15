import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor

data_file = "productivity_data.csv"

# Load or create data
def load_data():
    try:
        return pd.read_csv(data_file)
    except:
        return pd.DataFrame(columns=[
            "task", "category", "start_time", "end_time",
            "duration", "delay", "hour"
        ])

# Save data
def save_data(df):
    df.to_csv(data_file, index=False)

# -----------------------------
# Log Task (API usable)
# -----------------------------
def log_task(task, category, start_time, end_time, delay):
    df = load_data()

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

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_data(df)

    return {"message": "Task logged successfully"}

# -----------------------------
# Insights (API usable)
# -----------------------------
def generate_insights():
    df = load_data()

    if len(df) < 5:
        return ["Not enough data yet"]

    insights = []

    peak_hour = df.groupby("hour")["duration"].mean().idxmax()
    insights.append(f"🔥 Peak productivity hour: {peak_hour}:00")

    avg_delay = df["delay"].mean()
    if avg_delay > 15:
        insights.append("⚠️ You tend to procrastinate before tasks")

    low_hour = df.groupby("hour")["duration"].mean().idxmin()
    insights.append(f"⚠️ Avoid heavy tasks at {low_hour}:00")

    return insights

# -----------------------------
# ML Prediction
# -----------------------------
def predict_duration(hour, delay):
    df = load_data()

    if len(df) < 5:
        return "Not enough data"

    X = df[["hour", "delay"]]
    y = df["duration"]

    model = RandomForestRegressor()
    model.fit(X, y)

    prediction = model.predict([[hour, delay]])
    return round(prediction[0], 2)