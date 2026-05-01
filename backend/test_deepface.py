import cv2
import numpy as np
from deepface import DeepFace
import traceback

print('Running DeepFace')
try:
    result = DeepFace.analyze(img_path=np.zeros((100, 100, 3), dtype=np.uint8), actions=['emotion'], enforce_detection=False)
    print(result)
except Exception as e:
    traceback.print_exc()
