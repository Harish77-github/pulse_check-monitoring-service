from flask import Flask
from datetime import datetime
import psutil
import time
import requests

app = Flask(__name__)

start_time = time.time()

@app.route('/health')
def health():
    return {
        "status": "healthy",
        "service": "PulseCheck",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.route('/metrics')
def metrics():
    uptime = time.time() - start_time

    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "uptime_seconds": round(uptime, 2)
    }

@app.route('/check/github')
def check_github():
    start = time.time()

    try:
        response = requests.get("https://api.github.com")

        response_time = round((time.time() - start) * 1000, 2)

        return {
            "service": "GitHub API",
            "status": "reachable",
            "status_code": response.status_code,
            "response_time_ms": response_time
        }

    except Exception as e:
        return {
            "service": "GitHub API",
            "status": "unreachable",
            "error": str(e)
        }, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)