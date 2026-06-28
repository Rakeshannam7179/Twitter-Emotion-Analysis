import requests
import re

def extract_tweet_data(tweet_url: str):
    """
    Extracts the text and media image URL from a Twitter/X tweet URL
    using the vxtwitter API.
    """
    try:
        # Convert twitter.com or x.com URL to api.vxtwitter.com URL
        # Format: https://x.com/username/status/12345 -> https://api.vxtwitter.com/username/status/12345
        api_url = tweet_url
        api_url = re.sub(r'https?://(www\.)?(twitter|x)\.com', 'https://api.vxtwitter.com', api_url)
        
        print(f"Fetching tweet data from API: {api_url}")
        resp = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            tweet_data = {}
            
            # Extract text
            if 'text' in data:
                tweet_data['text'] = data['text']
                
            # Extract image URL (either tweet media or fallback to user profile image)
            if 'mediaURLs' in data and len(data['mediaURLs']) > 0:
                # Find first image URL
                # vxtwitter returns all media URLs in mediaURLs
                for url in data['mediaURLs']:
                    if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        tweet_data['image_url'] = url
                        break
            
            # Fallback to user profile image if no media images
            if 'image_url' not in tweet_data and 'user_profile_image_url' in data:
                tweet_data['image_url'] = data['user_profile_image_url']
                
            return tweet_data
        else:
            print(f"Failed to fetch tweet details from API: HTTP {resp.status_code}")
            return {}
    except Exception as e:
        print(f"Error extracting tweet data: {e}")
        return {}
