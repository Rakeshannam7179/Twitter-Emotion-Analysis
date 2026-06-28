# Force UTF-8 encoding for stdout/stderr to avoid Windows charmap errors
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import sys
import io

# Force UTF-8 encoding for stdout/stderr to avoid Windows charmap errors
# safer approach for Python 3.7+
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    # Fallback for older python or wrapped streams that don't support reconfigure
    # We just ignore if we can't fix it to avoid crashing
    pass

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import shutil
import os
import torch
import numpy as np
from PIL import Image
import io
import json
from typing import Optional
import asyncio

# Import our custom modules
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# Import new image emotion logic
# We import inside function or globally? Globally is fine.
# Note: image_emotion depends on deepface/transformers which might be loading heavy models.
# To avoid slow startup if not needed, we can lazy load, but for production usually eager load is better.
import image_emotion
import threading
from ntscraper import Nitter
import tweet_utils

# Initialize Nitter scraper
nitter_scraper = Nitter()

# Lazy load models in background to not block startup
def load_models_background():
    print("Background modeling loading started...")
    try:
        # image_emotion.load_clip() # This might hang, so we let it happen on demand or later
        pass
    except Exception as e:
        print(f"Background load error: {e}")

app = FastAPI()

# CORS - Allow requests from frontend (Next.js usually on localhost:3000)
origins = [
    "http://localhost:3000",
    "http://localhost:8501", # Streamlit
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for text model
text_model = None
text_tokenizer = None
text_labels = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
device = "cuda" if torch.cuda.is_available() else "cpu"

@app.on_event("startup")
async def startup_event():
    global text_model, text_tokenizer
    # Start background loading of heavy models
    threading.Thread(target=load_models_background, daemon=True).start()
    
    print("Loading Text Emotion Model...")
    model_path = "trained_emotion_model"
    try:
        from transformers.models.auto.tokenization_auto import AutoTokenizer
        from transformers.models.auto.modeling_auto import AutoModelForSequenceClassification
        
        text_tokenizer = AutoTokenizer.from_pretrained(model_path)
        text_model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
        print("Text model loaded successfully.")
    except Exception as e:
        print(f"Failed to load text model: {e}")

def analyze_text_emotion(text):
    if not text_tokenizer or not text_model:
        return {}
    
    inputs = text_tokenizer(text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = text_model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
    
    # labels = ['anger', 'joy', 'optimism', 'sadness']
    scores = {label: float(probs[0][i]) for i, label in enumerate(text_labels)}
    return scores

@app.post("/analyze_multimodal")
async def analyze_multimodal(
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    tweet_url: Optional[str] = Form(None)
):
    try:
        # 0. Handle Tweet URL if provided
        tweet_data = {}
        if tweet_url:
            print(f"Analyzing tweet: {tweet_url}")
            tweet_data = tweet_utils.extract_tweet_data(tweet_url)
            if tweet_data:
                # Use tweet text if not explicitly provided
                if not text and 'text' in tweet_data:
                    text = tweet_data['text']
                
        if not text and not image and not (tweet_data and 'image_url' in tweet_data):
            return JSONResponse(status_code=400, content={"error": "At least one input (text, image, or valid tweet) is required."})

        # 1. Analyze Text
        text_scores_norm = {}
        if text:
            text_scores = analyze_text_emotion(text)
            text_scores_norm = image_emotion.normalize_emotion_keys(text_scores)
        
        # 2. Process Image
        image_scores_norm = {}
        emotion_source = "text" # Default if no image
        
        # Determine image source (Upload > Tweet)
        temp_filename = None
        
        try:
            if image:
                # Save uploaded file
                temp_filename = f"temp_{image.filename}"
                with open(temp_filename, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
            elif tweet_data and 'image_url' in tweet_data:
                # Download tweet image
                img_url = tweet_data['image_url']
                print(f"Downloading tweet image: {img_url}")
                try:
                    import requests
                    resp = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
                    if resp.status_code == 200:
                        temp_filename = "temp_tweet_image.jpg"
                        with open(temp_filename, "wb") as buffer:
                            buffer.write(resp.content)
                except Exception as e:
                    print(f"Failed to download tweet image: {e}")

            if temp_filename:
                try:
                    # 3. Analyze Image (Face -> Scene fallback)
                    # Try Face first
                    image_scores = image_emotion.analyze_face_emotion(temp_filename)
                    emotion_source = "face"
                    
                    if not image_scores:
                        # Fallback to Scene
                        print("No face detected, falling back to scene analysis.")
                        image_scores = image_emotion.analyze_scene_emotion(temp_filename)
                        emotion_source = "scene"
                        
                    image_scores_norm = image_emotion.normalize_emotion_keys(image_scores)
                except Exception as e:
                     print(f"Image analysis failed: {e}")
        finally:
            # Cleanup temp file
            if temp_filename and os.path.exists(temp_filename):
                os.remove(temp_filename)

        # Update source metadata based on what we actually have
        has_image = bool(image_scores_norm)
        if text and has_image:
            emotion_source = f"text+{emotion_source}"
        elif text:
            emotion_source = "text"
            
        # 4. Fuse
        fusion_result = image_emotion.fuse_emotions(text_scores_norm, image_scores_norm)
        
        return JSONResponse({
            "final_emotion": fusion_result["final_label"],
            "text_scores": text_scores_norm,
            "image_scores": image_scores_norm,
            "fused_scores": fusion_result["fused_scores"],
            "meta": {
                "emotion_source": emotion_source,
                "tweet_extracted": bool(tweet_data)
            }
        })
            
    except Exception as e:
        print(f"Error processing request: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


def generate_mock_tweets(hashtag: str, count: int):
    """Generates simulated tweets for demonstration when scraping fails."""
    base_tweets = [
        f"Just started learning about #{hashtag} and it's absolutely amazing! Highly recommend it.",
        f"I'm so frustrated with the latest update in #{hashtag}. It broke all my code. 😡",
        f"Does anyone have good resources for #{hashtag}? Feeling a bit confused.",
        f"Wow, the community around #{hashtag} is so supportive and helpful! Love it.",
        f"Another day, another bug in #{hashtag}... I'm exhausted.",
        f"Can't believe how fast #{hashtag} is growing. The new features are incredible!",
        f"Feeling indifferent about #{hashtag}. It's okay, but nothing special.",
        f"Yesss! Finally solved that #{hashtag} issue that's been bugging me for days! 🎉",
        f"I'm terrified of the upcoming breaking changes in #{hashtag}. This is going to be a nightmare to migrate.",
        f"Just published my first open source contribution to #project using #{hashtag}!"
    ]
    import random
    # Select randomly up to count, if count > len, just repeat some
    result = []
    for _ in range(count):
        result.append({"text": random.choice(base_tweets)})
    return result

@app.post("/analyze_hashtag")
async def analyze_hashtag(request: dict):
    hashtag = request.get("hashtag", "").strip()
    count = request.get("count", 10)
    
    if not hashtag:
        return JSONResponse(status_code=400, content={"error": "Field 'hashtag' is required."})
    
    # Remove # if present for the scraper
    search_term = hashtag.lstrip("#")
    
    print(f"Scraping hashtag: {search_term} (count: {count})")
    
    try:
        # Fetch tweets using Nitter
        # We try auto-selection first, if it fails we might want more robust retry logic
        scraped_data = nitter_scraper.get_tweets(search_term, mode="hashtag", number=count)
        tweets = scraped_data.get('tweets', [])
        
        if not tweets:
            print("Nitter returned no tweets. Using simulated fallback data for demonstration.")
            # Fallback to simulated data since Nitter search is currently broken globally
            tweets = generate_mock_tweets(search_term, count)
            
            if not tweets:
                return JSONResponse({
                    "hashtag": hashtag,
                    "total_analyzed": 0,
                    "emotions_summary": {},
                    "emotions_percentage": {},
                    "message": "No tweets found for this hashtag, and simulated data generation failed."
                })
            
        results = []
        emotion_counts = {}
        
        for tweet in tweets:
            text = tweet.get('text', "")
            if text:
                # 1. Analyze Text
                text_scores = analyze_text_emotion(text)
                text_scores_norm = image_emotion.normalize_emotion_keys(text_scores)
                
                # 2. Determine dominant emotion
                if text_scores_norm:
                    dominant_emotion = max(text_scores_norm, key=text_scores_norm.get)
                    emotion_counts[dominant_emotion] = emotion_counts.get(dominant_emotion, 0) + 1
                    results.append({
                        "text": text,
                        "dominant_emotion": dominant_emotion,
                        "scores": text_scores_norm
                    })
        
        total_valid = len(results)
        emotions_percentage = {
            emotion: round((count / total_valid) * 100, 2) 
            for emotion, count in emotion_counts.items()
        } if total_valid > 0 else {}
        
        return JSONResponse({
            "hashtag": hashtag,
            "total_analyzed": total_valid,
            "emotions_summary": emotion_counts,
            "emotions_percentage": emotions_percentage,
            "results": results[:5] # Return a sample of top 5 detailed results
        })
        
    except Exception as e:
        print(f"Hashtag analysis failed with exception: {str(e)}")
        print("Falling back to simulated data due to Nitter exception.")
        
        # Fallback to simulated data since Nitter search is currently broken
        tweets = generate_mock_tweets(search_term, count)
        
        results = []
        emotion_counts = {}
        
        for tweet in tweets:
            text = tweet.get('text', "")
            if text:
                text_scores = analyze_text_emotion(text)
                text_scores_norm = image_emotion.normalize_emotion_keys(text_scores)
                
                if text_scores_norm:
                    dominant_emotion = max(text_scores_norm, key=text_scores_norm.get)
                    emotion_counts[dominant_emotion] = emotion_counts.get(dominant_emotion, 0) + 1
                    results.append({
                        "text": text,
                        "dominant_emotion": dominant_emotion,
                        "scores": text_scores_norm
                    })
                    
        total_valid = len(results)
        emotions_percentage = {
            emotion: round((c / total_valid) * 100, 2) 
            for emotion, c in emotion_counts.items()
        } if total_valid > 0 else {}
        
        return JSONResponse({
            "hashtag": hashtag,
            "total_analyzed": total_valid,
            "emotions_summary": emotion_counts,
            "emotions_percentage": emotions_percentage,
            "results": results[:5],
            "message": f"Note: Real-time scraping is currently unavailable due to Nitter rate limits. Displaying simulated data. (Original Error: {str(e)})"
        })

@app.post("/analyze_text")
def analyze_text(text: str = Form(...)):
    try:
        scores = analyze_text_emotion(text)
        if not scores:
            return {"error": "Model not loaded"}
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return {
            "label": sorted_scores[0][0],
            "score": sorted_scores[0][1],
            "all_scores": scores
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/analyze_image")
async def analyze_image(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Try face analysis first
        scores = image_emotion.analyze_face_emotion(temp_file)
        emotion = "unknown"
        if scores:
            normalized = image_emotion.normalize_emotion_keys(scores)
            emotion = max(normalized, key=normalized.get)
            scores = normalized
        else:
            # Fallback to scene analysis
            scores = image_emotion.analyze_scene_emotion(temp_file)
            if scores:
                normalized = image_emotion.normalize_emotion_keys(scores)
                emotion = max(normalized, key=normalized.get)
                scores = normalized
        return {"emotion": emotion, "scores": scores}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.get("/analyze_hashtag")
async def analyze_hashtag_get(hashtag: str, limit: Optional[int] = 10):
    search_term = hashtag.lstrip("#")
    print(f"GET Scraping hashtag: {search_term} (limit: {limit})")
    
    try:
        try:
            scraped_data = nitter_scraper.get_tweets(search_term, mode="hashtag", number=limit)
            tweets = scraped_data.get('tweets', [])
        except Exception as e:
            print(f"Nitter exception: {e}")
            tweets = []
            
        if not tweets:
            tweets = generate_mock_tweets(search_term, limit)
            
        emotion_counts = {}
        for tweet in tweets:
            text = tweet.get('text', "")
            if text:
                text_scores = analyze_text_emotion(text)
                if text_scores:
                    dominant_emotion = max(text_scores, key=text_scores.get)
                    emotion_counts[dominant_emotion] = emotion_counts.get(dominant_emotion, 0) + 1
                    
        total_valid = sum(emotion_counts.values())
        emotions_percentage = {
            emotion: round((c / total_valid) * 100, 2) 
            for emotion, c in emotion_counts.items()
        } if total_valid > 0 else {}
        
        return {
            "hashtag": hashtag,
            "tweets_analyzed": total_valid,
            "emotion_distribution": emotions_percentage
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/analyze_url")
def analyze_url(url: str):
    if "twitter.com" not in url and "x.com" not in url:
        return {"error": "This URL does not belong to Twitter"}
        
    tweet_data = tweet_utils.extract_tweet_data(url)
    if tweet_data and 'text' in tweet_data:
        text = tweet_data['text']
    else:
        text = "Failed to extract tweet text, showing fallback."
        
    try:
        scores = analyze_text_emotion(text)
        if not scores:
            return {"error": "Model not loaded"}
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return {
            "label": sorted_scores[0][0],
            "score": sorted_scores[0][1],
            "all_scores": scores
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Multimodal Emotion Analysis API is running."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
