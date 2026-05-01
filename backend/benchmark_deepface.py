import time
import numpy as np
from deepface import DeepFace

# Create a dummy image (100x100 RGB)
img = np.zeros((224, 224, 3), dtype=np.uint8)

print("Starting benchmark...")

# Warmup / Initial load
start_warmup = time.time()
DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
print(f"Warmup/Initial load took: {time.time() - start_warmup:.2f}s")

# Subsequent runs
durations = []
for i in range(5):
    start = time.time()
    DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
    durations.append(time.time() - start)
    print(f"Run {i+1} took: {durations[-1]:.2f}s")

print(f"Average subsequent run time: {sum(durations)/len(durations):.2f}s")

# Benchmark with detector_backend='skip'
print("\nBenchmarking with detector_backend='skip'...")
durations_skip = []
for i in range(5):
    start = time.time()
    DeepFace.analyze(img, actions=['emotion'], enforce_detection=False, detector_backend='skip')
    durations_skip.append(time.time() - start)
    print(f"Run {i+1} (skip) took: {durations_skip[-1]:.2f}s")

print(f"Average subsequent run time (skip): {sum(durations_skip)/len(durations_skip):.2f}s")
