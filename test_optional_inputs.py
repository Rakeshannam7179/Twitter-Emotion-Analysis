import requests
from PIL import Image
import io
import json

def create_dummy_image():
    # Create a red 224x224 image
    img = Image.new('RGB', (224, 224), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    return buf

def test_api():
    url = "http://localhost:8000/analyze_multimodal"
    print(f"Testing API at {url}...\n")
    
    # Test 1: Text Only
    print("--- Test 1: Text Only ---")
    try:
        response = requests.post(url, data={"text": "I am delightful!"})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Emotion: {response.json().get('final_emotion')}")
            print(f"Source: {response.json().get('meta', {}).get('emotion_source')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")

    # Test 2: Image Only
    print("\n--- Test 2: Image Only ---")
    try:
        img_data = create_dummy_image()
        response = requests.post(
            url,
            files={"image": ("dummy.jpg", img_data, "image/jpeg")}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Emotion: {response.json().get('final_emotion')}")
            print(f"Source: {response.json().get('meta', {}).get('emotion_source')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")

    # Test 3: Both
    print("\n--- Test 3: Both ---")
    try:
        img_data = create_dummy_image()
        response = requests.post(
            url,
            data={"text": "I am delightful!"},
            files={"image": ("dummy.jpg", img_data, "image/jpeg")}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Emotion: {response.json().get('final_emotion')}")
            print(f"Source: {response.json().get('meta', {}).get('emotion_source')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")
        
    # Test 4: None (Should fail)
    print("\n--- Test 4: None ---")
    try:
        response = requests.post(url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_api()
