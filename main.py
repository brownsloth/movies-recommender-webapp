from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import joblib
import json
import numpy as np
from recommend import load_movie_vectors
from feedback_tracker import should_retrain, auto_retrain
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()
#Accept requests from any frontend origin (you can restrict this later)
#Allow POST, OPTIONS, etc.
#Handle preflight requests without error
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for stricter setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = joblib.load("rec_model.pkl")
movies = load_movie_vectors("movie_vectors_full.json")
# main.py
genre_schema = ["Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", 
                "Drama", "Fantasy", "Film-Noir", "Horror", "IMAX", "Musical", "Mystery", 
                "Romance", "Sci-Fi", "Thriller", "War", "Western", "(no genres listed)"]
# print(movies[0])
# genre_schema = [genre for genre in movies[0]["vector"].keys()] if isinstance(movies[0]["vector"], dict) else [genre for genre in movies[0]["vector"]]


class UserVector(BaseModel):
    vector: List[int]

@app.get("/genres")
def get_genre_schema():
    print({"genres": genre_schema})
    return {"genres": genre_schema}

class FeedbackPayload(BaseModel):
    user_id: str
    user_vector: List[int]
    movie_id: int
    movie_vector: List[int]
    liked: int  # 1 or 0

@app.post("/feedback")
def log_feedback(payload: FeedbackPayload):
    # Log raw feedback
    with open("feedback.jsonl", "a") as f:
        f.write(json.dumps(payload.dict()) + "\n")

    # Log liked movies to per-user memory
    if payload.liked == 1:
        with open("user_memory.jsonl", "a") as f:
            f.write(json.dumps({
                "user_id": payload.user_id,
                "movie_id": payload.movie_id,
                "movie_vector": payload.movie_vector
            }) + "\n")

    # Auto retrain if enough data
    if should_retrain("feedback.jsonl", threshold=20):
        auto_retrain("feedback.jsonl")

    return {"status": "success"}

## COSINE SIMILARITY
# @app.post("/recommend")
# def recommend(user: UserVector):
#     results = recommend_movies(user.vector, movies)
#     return {"recommendations": results}

class RecommendPayload(BaseModel):
    user_id: str
    vector: List[int]

def get_user_liked_movies(user_id):
    liked = []
    try:
        with open("user_memory.jsonl", "r") as f:
            for line in f:
                entry = json.loads(line)
                if entry["user_id"] == user_id:
                    liked.append(entry["movie_vector"])
    except FileNotFoundError:
        pass
    return liked

@app.post("/recommend")
def recommend(payload: RecommendPayload, top_k: int = 5):
    user_vec = payload.vector
    user_id = payload.user_id

    liked_movies = get_user_liked_movies(user_id)

    scored = []
    for movie in movies:
        x = np.array(user_vec + movie["vector"]).reshape(1, -1)
        prob = model.predict_proba(x)[0][1]

        # Compute personalization score (average similarity to liked)
        personal_score = 0
        if liked_movies:
            sims = cosine_similarity([movie["vector"]], liked_movies)[0]
            personal_score = float(np.mean(sims))

        final_score = 0.7 * prob + 0.3 * personal_score

        scored.append({
            "title": movie["title"],
            "score": round(final_score, 3),
            "movie_id": movie["movieId"],
            "movie_vector": movie["vector"]
        })

    top = sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]
    return {"recommendations": top}

@app.get("/history/{user_id}")
def get_user_history(user_id: str):
    liked = []
    try:
        with open("user_memory.jsonl", "r") as f:
            for line in f:
                entry = json.loads(line)
                if entry["user_id"] == user_id:
                    liked.append({
                        "movie_id": entry["movie_id"],
                        "vector": entry["movie_vector"]
                    })
    except FileNotFoundError:
        pass
    return {"liked_movies": liked}

@app.get("/stats")
def get_stats():
    feedback_count = 0
    users = set()

    try:
        with open("feedback.jsonl", "r") as f:
            for line in f:
                feedback_count += 1
                entry = json.loads(line)
                users.add(entry["user_id"])
    except FileNotFoundError:
        pass

    return {
        "feedback_count": feedback_count,
        "user_count": len(users),
    }

@app.get("/movie_titles")
def get_movie_titles():
    id_to_title = {m["movieId"]: m["title"] for m in movies}
    return {"titles": id_to_title}


##Run using uvicorn main:app --reload
#It will run on http://localhost:8000
