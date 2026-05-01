import time
import requests
import json

st = time.time()
print('Start requesting:', st)

try:
    with open('dummy.jpg', 'rb') as f:
        print("Sending...")
        # Add timeout to see if it just hangs indefinitely
        r = requests.post('http://localhost:8000/analyze_image', files={'file': f}, timeout=15)
        print("Status Code:", r.status_code)
        
        try:
            print("Response:", r.json())
        except Exception as e:
            print("Failed to parse JSON, Response text:", r.text)

except Exception as e:
    print("Request Exception:", e)

print('Total time taken:', time.time() - st)
