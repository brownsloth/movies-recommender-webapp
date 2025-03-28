import json

def log_feedback(user_id, user_vector, movie_id, movie_vector, liked, path="feedback.jsonl"):
    feedback = {
        "user_id": user_id,
        "user_vector": user_vector,
        "movie_id": movie_id,
        "movie_vector": movie_vector,
        "liked": liked
    }
    with open(path, "a") as f:
        f.write(json.dumps(feedback) + "\n")
