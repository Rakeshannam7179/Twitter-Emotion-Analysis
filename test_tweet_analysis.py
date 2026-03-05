import requests
import time

def test_tweet_analysis():
    url = "http://localhost:8000/analyze_multimodal"
    
    # Jack's first tweet (text only, basically)
    # But fxtwitter might return profile image as OG image
    tweet_url = "https://x.com/jack/status/20"
    
    print(f"Testing Tweet Analysis: {tweet_url}")
    try:
        response = requests.post(url, data={"tweet_url": tweet_url})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success!")
            print(f"Emotion: {result.get('final_emotion')}")
            print(f"Source: {result.get('meta', {}).get('emotion_source')}")
            print(f"Tweet Extracted: {result.get('meta', {}).get('tweet_extracted')}")
            
            # Additional checks
            text_scores = result.get('text_scores', {})
            image_scores = result.get('image_scores', {})
            
            if text_scores:
                print("Text scores present (Good)")
            if image_scores:
                print("Image scores present (Good - likely profile pic)")
                
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    # Wait a bit for server to start if running immediately after restart
    time.sleep(2)
    test_tweet_analysis()
