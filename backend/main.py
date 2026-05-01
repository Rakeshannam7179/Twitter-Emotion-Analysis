import sys
import importlib.machinery

# Monkey patch for Python 3.12+ compatibility for older packages like snscrape
if not hasattr(importlib.machinery.FileFinder, 'find_module'):
    def find_module(self, fullname, path=None):
        spec = self.find_spec(fullname, path)
        return spec.loader if spec else None
    importlib.machinery.FileFinder.find_module = find_module

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from services.scraper import fetch_tweets
from services.emotion_engine import analyze_tweets, calculate_percentages
from models.text_model import predict_text_emotion
from models.image_model import predict_image_emotion
import os
import shutil
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Pre-load DeepFace model to avoid delay on first request
    import numpy as np
    from deepface import DeepFace
    print("Pre-loading DeepFace emotion model...")
    try:
        # Use a dummy image to trigger model loading
        DeepFace.analyze(
            np.zeros((224, 224, 3), dtype=np.uint8), 
            actions=['emotion'], 
            enforce_detection=False,
            detector_backend='opencv'
        )
        print("DeepFace emotion model pre-loaded successfully.")
    except Exception as e:
        print(f"Failed to pre-load DeepFace model: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze_text")
def analyze_text(text: str = Form(...)):
    try:
        result = predict_text_emotion(text)
        return result
    except Exception as e:
        import traceback
        with open("route_error.txt", "w") as f:
            f.write(traceback.format_exc())
        return {"error": str(e)}

@app.post("/analyze_image")
async def analyze_image(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Run blocking huggingface/deepface code in a separate thread so it doesn't hang FastAPI
        emotion, scores = await asyncio.to_thread(predict_image_emotion, temp_file)
        return {"emotion": emotion, "scores": scores}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.get("/test_speed")
def test_speed():
    return {"status": "fast"}

@app.get("/analyze_hashtag")
def analyze_hashtag(hashtag: str, limit: int = 100):
    tweets = fetch_tweets(hashtag, limit)
    total = len(tweets)
    
    if total == 0:
        return {"message": "No tweets found"}
        
    emotion_counts = analyze_tweets(tweets)
    emotion_scores = calculate_percentages(emotion_counts, total)
    
    return {
        "hashtag": hashtag,
        "tweets_analyzed": total,
        "emotion_distribution": emotion_scores
    }

@app.post("/analyze_url")
def analyze_url(url: str):
    # validate url
    if "twitter.com" not in url and "x.com" not in url:
        return {"error": "This URL does not belong to Twitter"}
        
    import random
    
    # Enhanced mock data with better variety
    mock_data = {
        "positive": [
            "I just had the greatest day ever! 😊",
            "What a wonderful surprise! Love this.",
            "So proud of what we achieved today. Optimistic!",
            "This community is so supportive and kind."
        ],
        "negative": [
            "This is so incredibly sad and frustrating. 😢",
            "I am so angry about this news. Unacceptable!",
            "Really disappointed in the recent turn of events.",
            "This makes me so anxious and worried."
        ],
        "neutral": [
            "Just read the latest update on the project.",
            "Interesting perspective on the current situation.",
            "Looking forward to seeing how this develops.",
            "Checking out the new features of the platform."
        ]
    }
    
    # Simple logic: detect keywords in URL to "pretend" we scraped it
    url_lower = url.lower()
    if any(k in url_lower for k in ["happy", "good", "great", "win", "love", "best"]):
        pool = mock_data["positive"]
    elif any(k in url_lower for k in ["sad", "angry", "bad", "fail", "hate", "worst", "error"]):
        pool = mock_data["negative"]
    else:
        # Fallback to a random selection but balanced
        all_tweets = mock_data["positive"] + mock_data["negative"] + mock_data["neutral"]
        random.seed(url)
        pool = [random.choice(all_tweets)]
        random.seed()
    
    tweet_text = random.choice(pool)
    result = predict_text_emotion(tweet_text)
    
    return result
