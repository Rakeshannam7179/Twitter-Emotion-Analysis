from models.text_model import predict_text_emotion

def analyze_tweets(tweets):
    emotion_counts = {}
    for tweet in tweets:
        text = tweet["text"]
        result = predict_text_emotion(text)
        emotion = result["label"]
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    return emotion_counts

def calculate_percentages(counts, total):
    percentages = {}
    for emotion, count in counts.items():
        percentages[emotion] = round((count / total) * 100, 2)
    return percentages
