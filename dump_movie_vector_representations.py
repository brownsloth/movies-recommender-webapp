import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import json

# Load movie data
movies = pd.read_csv("./ml-latest-small/movies.csv")

# Genre Encoding
movies['genres'] = movies['genres'].apply(lambda x: x.split('|') if isinstance(x, str) else [])
mlb = MultiLabelBinarizer()
genre_features = mlb.fit_transform(movies['genres'])
genre_names = mlb.classes_.tolist()

# Define mappings
mood_map = {
    'Comedy': 'Happy',
    'Drama': 'Sad',
    'Action': 'Excited',
    'Fantasy': 'Relaxed',
    'Romance': 'Happy',
    'Thriller': 'Excited',
    'Horror': 'Sad'
}
intensity_map = {
    'Comedy': 'Light',
    'Drama': 'Deep/Intense',
    'Thriller': 'Deep/Intense',
    'Horror': 'Deep/Intense',
    'Romance': 'Light'
}

def build_full_vector(genres):
    # Mood
    moods = ['Happy', 'Sad', 'Excited', 'Relaxed']
    mood = [1 if any(mood_map.get(g) == m for g in genres) else 0 for m in moods]

    # Type (assume all are movies in MovieLens)
    type_vec = [1, 0]  # Movies, TV Shows

    # Time bucket (placeholder — all mid-range for now)
    time_vec = [0, 1, 0]  # <30, 1h, 2h+

    # Genre (already encoded)
    genre_vec = [1 if g in genres else 0 for g in genre_names]

    # Intensity
    intensities = ['Light', 'Deep/Intense']
    intensity = [1 if any(intensity_map.get(g) == i for g in genres) else 0 for i in intensities]

    return mood + type_vec + time_vec + genre_vec + intensity

# Build final vector
movie_vectors = []
for i, row in movies.iterrows():
    full_vec = build_full_vector(row['genres'])
    movie_vectors.append({
        "movieId": int(row['movieId']),
        "title": row['title'],
        "genres": row['genres'],
        "vector": full_vec
    })

# Save
json_path = "./ml-latest-small/movie_vectors_full.json"
with open(json_path, "w") as f:
    json.dump(movie_vectors, f, indent=2)

print("✅ Movie vectors stored at:", json_path)
