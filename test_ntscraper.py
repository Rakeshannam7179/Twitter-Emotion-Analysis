from ntscraper import Nitter

def test_scraper():
    print("Testing ntscraper instances...")
    try:
        scraper = Nitter(log_level=1)
        instances = scraper.get_instances()
        print(f"Got {len(instances) if instances else 0} instances.")
        print("Instances:", instances)
        
        print("\nTesting hashtag search '#python'...")
        # Try to get tweets
        data = scraper.get_tweets("python", mode="hashtag", number=2)
        print("Scrape result keys:", data.keys() if data else data)
        print("Number of tweets:", len(data.get('tweets', [])) if data else 0)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_scraper()
