import json
import random
from itertools import product

# Load full movie vectors
with open("movie_vectors_full.json", "r") as f:
    movies = json.load(f)

# Config
mood_index = {"Happy": 0, "Sad": 1, "Excited": 2, "Relaxed": 3}
type_index = {"Movies": 0, "TV Shows": 1}
intensity_index = {"Light": 0, "Deep/Intense": 1}

def generate_user_vector(mood, content_type, time, genre, intensity, genre_schema_len):
    vec = []
    vec += [1 if mood_index[mood] == i else 0 for i in range(4)]
    vec += [1 if type_index[content_type] == i else 0 for i in range(2)]
    vec += [1 if time == i else 0 for i in range(3)]
    vec += [1 if i == genre else 0 for i in range(genre_schema_len)]
    vec += [1 if intensity_index[intensity] == i else 0 for i in range(2)]
    return vec

# Create a small genre lookup for simplicity
genre_lookup = {i: g for i, g in enumerate([
    "Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary",
    "Drama", "Fantasy", "Film-Noir", "Horror", "IMAX", "Musical", "Mystery",
    "Romance", "Sci-Fi", "Thriller", "War", "Western", "(no genres listed)"
])}

feedback_data = []

# Generate fake sessions
for _ in range(100):
    genre_idx = random.randint(0, 19)
    genre = genre_lookup[genre_idx]
    mood = random.choice(list(mood_index.keys()))
    intensity = "Light" if genre in ["Comedy", "Romance"] else "Deep/Intense"
    content_type = random.choice(["Movies", "TV Shows"])
    time_bucket = random.randint(0, 2)

    user_vec = generate_user_vector(
        mood=mood,
        content_type=content_type,
        time=time_bucket,
        genre=genre_idx,
        intensity=intensity,
        genre_schema_len=20
    )

    movie = random.choice(movies)
    movie_vec = movie["vector"]

    # Logical rule-based feedback
    liked = 0

    if "Comedy" in movie["genres"] and mood == "Happy":
        liked = 1
    elif "Romance" in movie["genres"] and mood in ["Happy", "Relaxed"]:
        liked = 1
    elif "Horror" in movie["genres"] and intensity == "Light":
        liked = 0
    else:
        liked = random.choice([0, 1])  # fallback

    feedback_data.append({
        "user_id": f"user_{random.randint(1, 10)}",
        "user_vector": user_vec,
        "movie_id": movie["movieId"],
        "movie_vector": movie_vec,
        "liked": liked
    })

# Save synthetic feedback
with open("feedback.jsonl", "w") as f:
    for row in feedback_data:
        f.write(json.dumps(row) + "\n")

print("✅ Generated 100 semi-smart synthetic feedback rows.")
