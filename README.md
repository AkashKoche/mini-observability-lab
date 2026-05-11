Use these Prometheus queries in the Prometheus UI (http://localhost:9090) to verify both the Counter and Histogram metrics are working.

# Generate Traffic

Run these commands in another terminal:

    while true; do
    curl http://localhost:5000/
    curl http://localhost:5000/api/users
    curl http://localhost:5000/api/orders
    curl http://localhost:5000/api/data
    curl http://localhost:5000/api/process
    done

# Counter Queries

Total HTTP Requests

    http_requests_total

Requests Per Second

    rate(http_requests_total[1m])

Requests Grouped by Endpoint

    sum by (endpoint) (
    rate(http_requests_total[1m])
    )

Error Requests (500)

    http_requests_total{status_code="500"}

Error Rate

    rate(http_requests_total{status_code="500"}[1m])

# Histogram Queries

Total Request Duration Count

    http_request_duration_seconds_count

Average Request Latency

    rate(http_request_duration_seconds_sum[1m])
    /
    rate(http_request_duration_seconds_count[1m])

95th Percentile Latency

    histogram_quantile(
    0.95,
    rate(http_request_duration_seconds_bucket[1m])
    )

Latency by Endpoint

    histogram_quantile(
    0.95,
    sum by (le, endpoint) (
    rate(http_request_duration_seconds_bucket[1m])
    )
    )



Then open Prometheus → Graph tab and execute the queries above
