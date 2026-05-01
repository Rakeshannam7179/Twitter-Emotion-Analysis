import uvicorn
import sys
from main import app

if __name__ == "__main__":
    with open("server_log.txt", "w") as f:
        sys.stderr = f
        sys.stdout = f
        uvicorn.run(app, host="127.0.0.1", port=8001)
