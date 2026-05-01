import sys
sys.path.append(".")
from models.text_model import predict_text_emotion
try:
    print(predict_text_emotion("I am very happy today!"))
except Exception as e:
    import traceback
    traceback.print_exc()
