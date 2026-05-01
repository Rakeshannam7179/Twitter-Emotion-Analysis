import numpy as np

# We cannot easily preload at module level if it blocks the event loop
# We will init on first request or asynchronously

def predict_image_emotion(image_path):
    from deepface import DeepFace
    result = DeepFace.analyze(
        img_path=image_path,
        actions=["emotion"],
        enforce_detection=False,
        detector_backend='opencv'
    )
    emotion = result[0]["dominant_emotion"]
    scores = {k: float(v) for k, v in result[0]["emotion"].items()}
    return emotion, scores
