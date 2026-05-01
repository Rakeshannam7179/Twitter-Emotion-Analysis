import time
import traceback
from deepface import DeepFace

print("Building model...")
st = time.time()
try:
    # According to DeepFace architecture, it caches models when building them.
    # However, 'Emotion' might not be the correct exact key, or we need to access it differently.
    model = DeepFace.build_model('Emotion')
    print("Model built in", time.time() - st)
except Exception as e:
    print("Error building model directly:")
    traceback.print_exc()

print("Running analyze to see if it implicitly builds and caches...")
import numpy as np
try:
    DeepFace.analyze(np.zeros((100, 100, 3), dtype=np.uint8), actions=['emotion'], enforce_detection=False)
    print("Analyze finished.")
except Exception as e:
    traceback.print_exc()
