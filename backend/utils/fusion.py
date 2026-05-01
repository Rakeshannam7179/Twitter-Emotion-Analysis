# Emotion Alignment Map
# Unifies labels from distilroberta (text) and FER2013/DeepFace (image)

ALIGNED_LABELS = {
    'anger': 'angry',
    'disgust': 'disgust',
    'fear': 'fear',
    'joy': 'happy',
    'neutral': 'neutral',
    'sadness': 'sad',
    'surprise': 'surprise'
}

def get_aligned_emotion(label):
    return ALIGNED_LABELS.get(label.lower(), label.lower())

def fuse_emotions(text_scores, image_scores, text_weight=0.6, image_weight=0.4):
    """
    Combines scores from text and image models.
    text_scores: dict {emotion: score}
    image_scores: dict {emotion: score}
    """
    fused_scores = {}
    
    # Iterate through all standard neutral labels
    all_emotions = set(ALIGNED_LABELS.values())
    
    for emotion in all_emotions:
        # Find corresponding text score
        t_score = 0
        for t_label, t_val in text_scores.items():
            if get_aligned_emotion(t_label) == emotion:
                t_score = t_val
                break
        
        # Find corresponding image score
        i_score = 0
        for i_label, i_val in image_scores.items():
            if get_aligned_emotion(i_label) == emotion:
                i_score = i_val
                break
                
        fused_scores[emotion] = (t_score * text_weight) + (i_score * image_weight)
        
    # Determine winner
    final_emotion = max(fused_scores, key=fused_scores.get)
    return final_emotion, fused_scores
