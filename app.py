from flask import Flask, jsonify, render_template_string
import psutil
import random
import time
import requests

app = Flask(__name__)

start_time = time.time()

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "PulseCheck Monitoring Service",
        "uptime_seconds": round(time.time() - start_time, 2)
    })

@app.route('/metrics')
def metrics():
    return jsonify({
        "cpu_usage_percent": round(psutil.cpu_percent(interval=1), 2),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "active_requests": random.randint(10, 100),
        "uptime_seconds": round(time.time() - start_time, 2)
    })
@app.route('/github')
def github_health():

    try:
        response = requests.get("https://api.github.com")

        github_status = "Reachable" if response.status_code == 200 else "Unreachable"

        return jsonify({
            "github_server_status": github_status,
            "status_code": response.status_code,
            "api_url": "https://api.github.com",
            "message": "GitHub API connectivity successful"
        })

    except Exception as e:

        return jsonify({
            "github_server_status": "Down",
            "error": str(e)
        }), 500

@app.route('/')
def dashboard():

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    requests = random.randint(10, 20)

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>PulseCheck Dashboard</title>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {{
                font-family: Arial;
                background-color: #0f172a;
                color: white;
                padding: 30px;
            }}

            .container {{
                max-width: 1000px;
                margin: auto;
            }}

            .cards {{
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
            }}

            .card {{
                background: #1e293b;
                padding: 20px;
                border-radius: 12px;
                flex: 1;
                text-align: center;
            }}

            canvas {{
                background: white;
                border-radius: 10px;
                padding: 10px;
            }}

            h1 {{
                text-align: center;
                margin-bottom: 30px;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <h1>🚀 PulseCheck Monitoring Dashboard</h1>

            <div class="cards">
                <div class="card">
                    <h2>CPU Usage</h2>
                    <h1>{cpu}%</h1>
                </div>

                <div class="card">
                    <h2>Memory Usage</h2>
                    <h1>{memory}%</h1>
                </div>

                <div class="card">
                    <h2>Active Requests</h2>
                    <h1>{requests}</h1>
                </div>
            </div>

            <canvas id="metricsChart"></canvas>

        </div>

        <script>

            const ctx = document.getElementById('metricsChart');

            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['CPU', 'Memory', 'Requests'],
                    datasets: [{{
                        label: 'System Metrics',
                        data: [{cpu}, {memory}, {requests}],
                    }}]
                }}
            }});

        </script>

    </body>
    </html>
    '''

    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)