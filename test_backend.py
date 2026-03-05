import requests
from PIL import Image
import io

def create_dummy_image():
    # Create a red 224x224 image
    img = Image.new('RGB', (224, 224), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    return buf

def test_api():
    url = "http://localhost:8000/analyze_multimodal"
    text = "I am delightful!"
    
    print(f"Testing API at {url}...")
    print(f"Text: {text}")
    print("Image: Dummy Red Image (simulating scene/face)")
    
    img_data = create_dummy_image()
    
    try:
        response = requests.post(
            url,
            data={"text": text},
            files={"image": ("dummy.jpg", img_data, "image/jpeg")}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            print(response.json())
        else:
            print("Error Response:")
            print(response.text)
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_api()
