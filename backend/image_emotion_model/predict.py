import torch
from PIL import Image
from torchvision import transforms
from .model import EmotionModel
import os

# Map prediction to emotion based on FER2013 standard labels if used
# Standard index: 0:angry, 1:disgust, 2:fear, 3:happy, 4:neutral, 5:sad, 6:surprise
EMOTION_MAP = {
    0: 'angry',
    1: 'disgust',
    2: 'fear',
    3: 'happy',
    4: 'neutral',
    5: 'sad',
    6: 'surprise'
}

_model = None
_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def load_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), "image_emotion_model.pth")
        _model = EmotionModel(num_classes=7)
        if os.path.exists(model_path):
            _model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
            print("Custom Image Emotion Model loaded.")
        else:
            print(f"Warning: Custom model weights not found at {model_path}. Using uninitialized model (not recommended).")
        _model.eval()
    return _model

def predict_custom_image_emotion(image_path):
    model = load_model()
    img = Image.open(image_path).convert('RGB')
    img_tensor = _transform(img).unsqueeze(0)
    
    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.softmax(output, dim=1)[0]
        prediction = output.argmax(1).item()
    
    emotion = EMOTION_MAP.get(prediction, "unknown")
    scores = {EMOTION_MAP[i]: float(probabilities[i]) for i in range(len(EMOTION_MAP))}
    
    return emotion, scores
