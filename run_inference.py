from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load model once
model_path = "trained_emotion_model"
try:
    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path).to("cuda" if torch.cuda.is_available() else "cpu")
    labels = ['anger', 'joy', 'optimism', 'sadness']
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

def predict_emotion(text):
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        logits = model(**inputs).logits
    
    predicted_class_id = logits.argmax().item()
    predicted_label = labels[predicted_class_id]
    
    print(f"\nText: '{text}'")
    print(f"Predicted Emotion: {predicted_label}")

if __name__ == "__main__":
    texts = [
        "I am so happy today!",
        "This makes me incredibly angry.",
        "I hope everything turns out okay.",
        "I feel a bit blue today."
    ]
    
    for t in texts:
        predict_emotion(t)

