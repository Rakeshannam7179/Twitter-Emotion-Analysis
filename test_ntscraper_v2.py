from ntscraper import Nitter
import json

def test_hashtag_scrape():
    # Attempt with specific instance if possible or manually provide a list
    # The default instance detection might be failing
    nitter = Nitter()
    print("Scraping hashtag: python")
    try:
        # Try a known instance if the auto-selection fails
        # common instances: nitter.net, nitter.cz, nitter.it, nitter.hirosi.me
        tweets = nitter.get_tweets("python", mode="hashtag", number=5, instance='https://nitter.net')
        print(json.dumps(tweets, indent=2))
        if tweets and 'tweets' in tweets and len(tweets['tweets']) > 0:
            print(f"Successfully scraped {len(tweets['tweets'])} tweets")
        else:
            print("No tweets found or scraping failed")
    except Exception as e:
        print(f"Error with nitter.net: {e}")
        try:
             print("Trying auto-selection again with more retries...")
             tweets = nitter.get_tweets("python", mode="hashtag", number=5)
             print(f"Successfully scraped {len(tweets['tweets'])} tweets")
        except Exception as e2:
             print(f"Auto-selection error: {e2}")

if __name__ == "__main__":
    test_hashtag_scrape()
