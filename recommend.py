from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

def load_movie_vectors(path="movie_vectors.json"):
    with open(path, "r") as f:
        movies = json.load(f)
    return movies

def recommend_movies(user_vector, movies, top_k=5):
    movie_vectors = [m['vector'] for m in movies]
    similarities = cosine_similarity([user_vector], movie_vectors)[0]
    ranked = sorted(zip(movies, similarities), key=lambda x: x[1], reverse=True)
    return [{"title": m["title"], "score": round(score, 3)} for m, score in ranked[:top_k]]
