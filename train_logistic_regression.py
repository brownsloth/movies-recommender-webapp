import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# === 1. Load Feedback ===

def load_feedback(path="feedback.jsonl"):
    X, y = []
    expected_len = 51  # adjust if needed
    with open(path, "r") as f:
        for line in f:
            entry = json.loads(line)
            user_vec = entry["user_vector"]
            movie_vec = entry["movie_vector"]
            label = entry["liked"]

            combined = user_vec + movie_vec

            if len(combined) != expected_len:
                print(f"⚠️ Skipping invalid entry (len={len(combined)}): {entry}")
                continue

            X.append(combined)
            y.append(label)

    return np.array(X), np.array(y)

# === 2. Train Model ===

def train_model(X, y):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_val)
    y_prob = clf.predict_proba(X_val)[:, 1]

    print("📊 Classification Report:\n", classification_report(y_val, y_pred))
    print("💯 AUC Score:", roc_auc_score(y_val, y_prob))

    return clf

# === 3. Save Model ===

def save_model(model, path="rec_model.pkl"):
    joblib.dump(model, path)
    print(f"✅ Model saved to: {path}")

# === MAIN ===

if __name__ == "__main__":
    X, y = load_feedback()
    print(f"🧠 Loaded {len(X)} feedback samples")
    model = train_model(X, y)
    save_model(model)
