import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.models.text_model import predict_text_emotion

test_texts = [
    "I am so happy!",
    "I am very angry.",
    "I feel so sad.",
    "I am afraid.",
    "I am surprised!",
    "I feel neutral."
]

for text in test_texts:
    result = predict_text_emotion(text)
    print(f"Text: '{text}' -> Label: {result['label']}, Score: {result['score']:.4f}")
