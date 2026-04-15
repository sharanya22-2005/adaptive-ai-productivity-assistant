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


