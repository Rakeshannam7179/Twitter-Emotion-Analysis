import requests

def test_url_analysis(url):
    response = requests.post(f"http://localhost:8000/analyze_url?url={url}")
    print(f"URL: {url} -> Result: {response.json()}")

urls = [
    "https://twitter.com/test/status/1",
    "https://twitter.com/test/status/2",
    "https://twitter.com/test/status/3",
    "https://twitter.com/test/status/4",
    "https://twitter.com/test/status/5",
    "https://twitter.com/test/status/6"
]

for u in urls:
    test_url_analysis(u)
