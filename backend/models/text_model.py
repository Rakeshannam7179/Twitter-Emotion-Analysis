from transformers import pipeline
import os

emotion_model = None

def get_emotion_model():
    global emotion_model
    if emotion_model is None:
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "fine_tuned_emotion", "final")
        if not os.path.exists(model_path):
            model_path = "j-hartmann/emotion-english-distilroberta-base"
        emotion_model = pipeline("text-classification", model=model_path)
    return emotion_model

def predict_text_emotion(text):
    model = get_emotion_model()
    # Request all scores from the model
    results = model(text, top_k=None)
    
    # Sort results to have the top one first
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    return {
        "label": sorted_results[0]["label"],
        "score": float(sorted_results[0]["score"]),
        "all_scores": {r["label"]: float(r["score"]) for r in sorted_results}
    }
