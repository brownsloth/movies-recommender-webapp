import json
from train_logistic_regression import train_model, save_model  # reuse from before
from train_logistic_regression import load_feedback

def should_retrain(path="feedback.jsonl", threshold=50):
    with open(path) as f:
        lines = f.readlines()
    return len(lines) % threshold == 0

def auto_retrain(path="feedback.jsonl"):
    X, y = load_feedback(path)
    if len(X) < 10:
        print("🚧 Not enough data to retrain yet.")
        return
    model = train_model(X, y)
    save_model(model, "rec_model.pkl")
    print("✅ Model retrained and updated.")
