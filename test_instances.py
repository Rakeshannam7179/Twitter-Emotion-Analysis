import requests
from ntscraper import Nitter

instances = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.cz",
    "https://nitter.unixfox.eu",
    "https://nitter.moomoo.me",
    "https://nitter.net"
]

def check_instances():
    working = []
    for inst in instances:
        try:
            r = requests.get(inst, timeout=5)
            if r.status_code == 200:
                print(f"[OK] {inst}")
                working.append(inst)
            else:
                print(f"[FAIL] {inst} - {r.status_code}")
        except Exception as e:
            print(f"[ERROR] {inst} - {e}")
            
    print(f"\nFound {len(working)} working instances.")
    if working:
        scraper = Nitter()
        try:
            # Try forcing an instance
            print(f"Trying ntscraper with instance: {working[0]}")
            data = scraper.get_tweets("python", mode="hashtag", number=2, instance=working[0])
            print(f"Success! Got {len(data.get('tweets', []))} tweets.")
        except Exception as e:
            print(f"ntscraper failed even with explicit instance: {e}")

if __name__ == "__main__":
    check_instances()
