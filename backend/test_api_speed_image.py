import requests
import time
import os

url = "http://127.0.0.1:8000/analyze_image"
image_path = "dummy.jpg"

if not os.path.exists(image_path):
    import numpy as np
    from PIL import Image
    # Create a dummy image if it doesn't exist
    arr = np.zeros((224, 224, 3), dtype=np.uint8)
    Image.fromarray(arr).save(image_path)

print(f"Testing {url} with {image_path}...")

# First request (should be fast if pre-loaded)
start = time.time()
with open(image_path, "rb") as f:
    response = requests.post(url, files={"file": f})
print(f"First request took: {time.time() - start:.2f}s")
print(f"Response: {response.json()}")

# Second request
start = time.time()
with open(image_path, "rb") as f:
    response = requests.post(url, files={"file": f})
print(f"Second request took: {time.time() - start:.2f}s")
