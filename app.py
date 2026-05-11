from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import random
import time

app = Flask(__name__)

# -----------------------------
# Counter Metric (Traffic/Errors)
# -----------------------------
REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

# -----------------------------
# Histogram Metric (Latency)
# -----------------------------
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# -----------------------------
# Routes
# -----------------------------

@app.route('/')
def home():
    REQUEST_COUNTER.labels(
        method='GET',
        endpoint='/',
        status_code='200'
    ).inc()

    return "Home Page"


@app.route('/api/users')
def users():
    REQUEST_COUNTER.labels(
        method='GET',
        endpoint='/api/users',
        status_code='200'
    ).inc()

    return "User List"


@app.route('/api/orders')
def orders():
    start_time = time.time()

    # Simulate processing time
    processing_time = random.uniform(0.05, 2.0)
    time.sleep(processing_time)

    # Record latency
    REQUEST_DURATION.labels(
        method='GET',
        endpoint='/api/orders'
    ).observe(time.time() - start_time)

    # Simulate 20% error rate
    if random.random() < 0.2:
        REQUEST_COUNTER.labels(
            method='GET',
            endpoint='/api/orders',
            status_code='500'
        ).inc()

        return "Internal Server Error", 500

    REQUEST_COUNTER.labels(
        method='GET',
        endpoint='/api/orders',
        status_code='200'
    ).inc()

    return f"Order List (took {processing_time:.2f}s)"


@app.route('/api/data')
def data():
    start_time = time.time()

    # Simulate processing time
    processing_time = random.uniform(0.05, 3.0)
    time.sleep(processing_time)

    # Record latency
    REQUEST_DURATION.labels(
        method='GET',
        endpoint='/api/data'
    ).observe(time.time() - start_time)

    REQUEST_COUNTER.labels(
        method='GET',
        endpoint='/api/data',
        status_code='200'
    ).inc()

    return f"Data (took {processing_time:.2f}s)"


# Better latency tracking using decorator
@app.route('/api/process')
@REQUEST_DURATION.labels(
    method='GET',
    endpoint='/api/process'
).time()
def process():
    processing_time = random.uniform(0.1, 2.0)
    time.sleep(processing_time)

    REQUEST_COUNTER.labels(
        method='GET',
        endpoint='/api/process',
        status_code='200'
    ).inc()

    return f"Processed (took {processing_time:.2f}s)"


# -----------------------------
# Metrics Endpoint
# -----------------------------
@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {
        'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'
    }


# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
