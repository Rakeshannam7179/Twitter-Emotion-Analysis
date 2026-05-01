from models.text_model import predict_text_emotion

test_sentences = [
    "I'm so angry at this bug!",
    "What a wonderful day for a walk.",
    "I'm scared of the dark.",
    "This smells like rotten eggs.",
    "I'm feeling a bit down today.",
    "I can't believe I won the lottery!",
    "The sky is blue and the grass is green."
]

print("Evaluating current model...")
for sentence in test_sentences:
    result = predict_text_emotion(sentence)
    print(f"Text: '{sentence}' -> Produced: {result['label']} (Score: {result['score']:.2f})")
