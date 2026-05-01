import requests
import traceback
try:
    res = requests.post("http://127.0.0.1:8000/analyze_text", data={"text": "im happy"})
    print("STATUS", res.status_code)
    print("CONTENT", res.text)
except Exception as e:
    traceback.print_exc()
