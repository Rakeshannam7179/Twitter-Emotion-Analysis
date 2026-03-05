# from deepface import DeepFace
# from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image
import numpy as np

# Global variables for CLIP
processor = None
clip_model = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_clip():
    global processor, clip_model
    if processor is None:
        from transformers import CLIPProcessor, CLIPModel
        print("Loading CLIP model...")
        model_name = "openai/clip-vit-base-patch32"
        processor = CLIPProcessor.from_pretrained(model_name)
        clip_model = CLIPModel.from_pretrained(model_name)
        clip_model.to(device)

def analyze_face_emotion(img_path):
    """
    Detects emotion from the most prominent face in the image using DeepFace.
    Returns a dict of {emotion: score} or None if no face found.
    """
    try:
        from deepface import DeepFace
        # DeepFace.analyze returns a list of result objects
        results = DeepFace.analyze(
            img_path=str(img_path),
            actions=['emotion'],
            enforce_detection=True,
            detector_backend='opencv',
            align=True
        )
        if not results:
            return None
        
        # Take the first face
        emotion_scores = results[0]['emotion']
        # DeepFace returns percentages (0-100), normalize to 0-1
        normalized_scores = {k: float(v) / 100.0 for k, v in emotion_scores.items()}
        return normalized_scores 
    except Exception as e:
        print(f"Face detection failed or no face found: {e}")
        return None

def analyze_scene_emotion(img_path):
    """
    Classifies scene emotion using CLIP zero-shot classification.
    Returns a dict of {emotion: score}.
    """
    labels = ["joy", "anger", "sadness", "fear", "surprise", "love", "neutral"]
    
    try:
        load_clip()
        image = Image.open(img_path)
        inputs = processor(
            text=labels, images=image, return_tensors="pt", padding=True
        ).to(device)
        
        with torch.no_grad():
            outputs = clip_model(**inputs)
        
        # Softmax to get probabilities
        probs = outputs.logits_per_image.softmax(dim=1).cpu().numpy()[0]
        
        return {label: float(score) for label, score in zip(labels, probs)}
    except Exception as e:
        print(f"Scene analysis failed: {e}")
        # Return uniform distribution or neutral bias on failure
        return {label: 1.0/len(labels) for label in labels}

def fuse_emotions(text_scores, image_scores, w_text=0.6, w_img=0.4):
    """
    Fuses text and image emotion scores. 
    Handles cases where one modality is missing (empty dict).
    """
    if not text_scores and not image_scores:
        return {"final_label": "neutral", "fused_scores": {}}
    
    # If one is missing, give full weight to the other
    if not text_scores:
        w_text = 0.0
        w_img = 1.0
    elif not image_scores:
        w_text = 1.0
        w_img = 0.0
        
    # Ensure all keys exist
    all_emotions = set(text_scores.keys()) | set(image_scores.keys())
    
    fused_scores = {}
    for emotion in all_emotions:
        t_score = text_scores.get(emotion, 0.0)
        i_score = image_scores.get(emotion, 0.0)
        
        # Weighted average
        fused_scores[emotion] = float((t_score * w_text) + (i_score * w_img))
    
    # Normalize fused scores to sum to 1
    total_score = sum(fused_scores.values())
    if total_score > 0:
        fused_scores = {k: float(v / total_score) for k, v in fused_scores.items()}
    
    # Determine winner
    if fused_scores:
        final_label = max(fused_scores, key=fused_scores.get)
    else:
        final_label = "neutral"
    
    return {
        "final_label": final_label,
        "fused_scores": fused_scores
    }

def normalize_emotion_keys(scores):
    """
    Maps various emotion labels to a standard set:
    joy, anger, sadness, fear, surprise, love, neutral, optimism
    """
    # DeepFace: angry, disgust, fear, happy, sad, surprise, neutral
    # RoBERTa (tweet_eval): anger, joy, optimism, sadness
    # CLIP: joy, anger, sadness, fear, surprise, love, neutral
    
    mapping = {
        "happy": "joy",
        "angry": "anger",
        "sad": "sadness",
        "disgust": "anger", # Mapping disgust to anger for simplicity
    }
    
    new_scores = {}
    for k, v in scores.items():
        key = k.lower()
        if key in mapping:
            key = mapping[key]
        new_scores[key] = float(new_scores.get(key, 0.0) + v)
        
    return new_scores
