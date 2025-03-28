# **Movie Recommender: Full-Stack ML-Powered App**

This project is a full-stack movie recommendation system designed to deliver personalized suggestions using a hybrid of machine learning and per-user feedback. It is implemented using:

- **Frontend**: Next.js + React  

- **Backend**: FastAPI + scikit-learn  

- **Modeling**: Logistic Regression on vectorized user-movie feature combinations  

- **Data**: MovieLens (for movie metadata), simulated or live feedback data  

## **Architecture Overview**

**Main components:**

1. Interactive quiz-based frontend to gather user intent  

2. Backend model scoring for recommendation ranking  

3. Real-time feedback collection and retraining  

4. Personalized re-ranking using per-user historical preferences  

5. Embedded UI dashboard for feedback stats and history  

## **Development Timeline & Decisions**

### **1\. Interactive Frontend for Cold-Start Recommendations**

We started by designing a question-based onboarding UI, where the user answers 5 questions (mood, content type, time, genre, intensity). Each answer is one-hot encoded into a user intent vector.

**Reasoning**:  
This approach mitigates cold-start issues by collecting structured, semantically relevant data without requiring historical behavior.

### **2\. Movie Vector Representation using MovieLens**

We extracted genres from MovieLens and transformed each movie into a genre-based binary vector.

**Reasoning**:  
Genre vectors are interpretable and align naturally with quiz answers. This keeps the system transparent and extensible.

### **3\. Initial Cosine Similarity-Based Matching**

The first working version used cosine similarity between the user vector and movie genre vectors to return the top recommendations.

**Reasoning**:  
Simple to implement and serves as a baseline to validate the quality of vectorization and quiz logic.

### **4\. Logging Feedback and Introducing ML Model**

We introduced a feedback mechanism where the user can like/dislike each recommended movie. This was logged to a feedback.jsonl file with full feature vectors.

We then trained a LogisticRegression model using:

ini

CopyEdit

input = \[user_vector + movie_vector\]

label = liked (0/1)

**Reasoning**:  
Using a learnable model allows the system to improve over time as more feedback is collected, and it generalizes patterns beyond just vector similarity.

### **5\. Automatic Retraining on Feedback Threshold**

We introduced logic to retrain the model every N feedback samples (e.g., 20), using stored feedback data.

**Reasoning**:  
This creates a continual learning loop without requiring explicit dev action. Keeps the model updated as user behavior changes.

### **6\. Per-User History and Hybrid Re-Ranking**

We began storing liked movies per user and used cosine similarity between a candidate movie and previously liked movies to generate a personalization score.

Final score:

ini

CopyEdit

score = 0.7 \* model prediction + 0.3 \* similarity to user history

**Reasoning**:  
This hybrid approach ensures global learning generalizes across users while enabling user-specific fine-tuning.

### **7\. Persistent Session Tracking (localStorage)**

We persisted user_id in localStorage to maintain a consistent identity across page refreshes and API calls.

**Reasoning**:  
Essential for tracking history, logging feedback, and delivering personalized results across sessions.

### **8\. Feedback Dashboard**

Added embedded UI to show:

- Movies liked by the current user  

- Global stats: number of feedback entries and users  

**Reasoning**:  
Increases transparency for the user and helps debug/validate the system’s behavior.

## **Current Features**

- Quiz-driven cold-start personalization  

- Genre-based movie representation  

- Feedback-driven logistic regression model  

- Continuous auto-retraining  

- Session-aware user tracking  

- Hybrid global + personalized scoring  

- Real-time feedback and analytics dashboard  

## **Future Work**

- Enhance movie vectors with textual embeddings or ratings  

- Integrate TMDB API for metadata and poster images  

- Session segmentation and behavior clustering  

- Visualization of feedback over time (e.g., favorite genres)

========

Setup instructions:

1. Run backend

```bash
uvicorn main:app --reload
```
Ensure you have fastapi, uvicorn, scikit-learn, numpy, and joblib installed.
Backend will run on http://localhost:8000.

2. Run frontend

```bash
cd movie-recommender
npm run dev
```

Frontend runs on http://localhost:3000.


ChatGPT has been a lot of help to accomplish all this in basically a few hours.