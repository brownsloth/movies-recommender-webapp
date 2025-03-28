from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import json
from recommend import load_movie_vectors, recommend_movies  # your function file
from fastapi.middleware.cors import CORSMiddleware


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

@app.post("/recommend")
def recommend(user: UserVector):
    results = recommend_movies(user.vector, movies)
    return {"recommendations": results}

##Run using uvicorn main:app --reload
#It will run on http://localhost:8000
