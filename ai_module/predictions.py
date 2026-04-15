import json
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer

# ------------------------------
# Data Storage
# ------------------------------
DATA_FILE = "task_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return [], []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return data["tasks"], data["times"]

def save_data(tasks, times):
    with open(DATA_FILE, "w") as f:
        json.dump({"tasks": tasks, "times": times}, f)

# ------------------------------
# Feature Engineering
# ------------------------------
class FeatureExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, tasks):
        text_features = self.vectorizer.fit_transform(tasks).toarray()
        length_feature = np.array([len(t.split()) for t in tasks]).reshape(-1, 1)
        return np.hstack((text_features, length_feature))

    def transform(self, tasks):
        text_features = self.vectorizer.transform(tasks).toarray()
        length_feature = np.array([len(t.split()) for t in tasks]).reshape(-1, 1)
        return np.hstack((text_features, length_feature))

# ------------------------------
# AI Model
# ------------------------------
class TimePredictor:
    def __init__(self):
        self.tasks, self.times = load_data()
        self.extractor = FeatureExtractor()
        self.model = LinearRegression()

        if len(self.tasks) > 1:
            X = self.extractor.fit_transform(self.tasks)
            y = np.array(self.times)
            self.model.fit(X, y)

    def predict(self, task):
        if len(self.tasks) < 2:
            print("⚠️ Not enough data. Using default estimate (30 mins).")
            return 30

        X = self.extractor.transform([task])
        return round(self.model.predict(X)[0], 2)

    def update(self, task, actual_time):
        self.tasks.append(task)
        self.times.append(actual_time)
        save_data(self.tasks, self.times)

        # retrain model
        if len(self.tasks) > 1:
            X = self.extractor.fit_transform(self.tasks)
            y = np.array(self.times)
            self.model.fit(X, y)

# ------------------------------
# CLI Interface
# ------------------------------
def main():
    predictor = TimePredictor()

    while True:
        print("\n--- AI Time Manager ---")
        print("1. Predict Task Duration")
        print("2. Add Completed Task (Train AI)")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1":
            task = input("Enter task description: ")
            prediction = predictor.predict(task)
            print(f"⏱ Estimated Time: {prediction} minutes")

        elif choice == "2":
            task = input("Task description: ")
            actual = float(input("Actual time taken (minutes): "))
            predictor.update(task, actual)
            print("✅ Data added. AI improved.")

        elif choice == "3":
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()