Use these Prometheus queries in the Prometheus UI (http://localhost:9090) to verify both the Counter and Histogram metrics are working.

Counter Queries
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
Histogram Queries
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
Generate Traffic

Run these commands in another terminal:

while true; do
  curl http://localhost:5000/
  curl http://localhost:5000/api/users
  curl http://localhost:5000/api/orders
  curl http://localhost:5000/api/data
  curl http://localhost:5000/api/process
done

Then open Prometheus → Graph tab and execute the queries above

# SCREENSHOTS

Take these screenshots to clearly demonstrate both the Counter and Histogram metrics setup and results.

1. Docker Containers Running

Command:

docker ps

Screenshot should show:

prometheus
flask-app
Ports 9090 and 5000
2. Flask Metrics Endpoint

Open:

http://localhost:5000/metrics

Screenshot should include:

http_requests_total
http_request_duration_seconds_bucket
_sum
_count

This proves metrics are exposed correctly.

3. Prometheus Targets Page

Open:

http://localhost:9090/targets

Screenshot should show:

flask-app
State = UP

This proves Prometheus is scraping the Flask app.

4. Counter Metric Query

In Prometheus Graph tab, run:

http_requests_total

Screenshot should show:

Different endpoints
Status codes
Increasing values

This demonstrates traffic/error counting.

5. Error Counter Query

Run:

http_requests_total{status_code="500"}

Screenshot should show:

Error count for /api/orders

This demonstrates error monitoring.

6. Histogram Bucket Query

Run:

http_request_duration_seconds_bucket

Screenshot should show:

Different le bucket values
Endpoint labels

This proves histogram buckets are working.

7. Average Latency Query

Run:

rate(http_request_duration_seconds_sum[1m])
/
rate(http_request_duration_seconds_count[1m])

Use Graph mode.

Screenshot should show:

Latency graph changing over time
8. 95th Percentile Latency

Run:

histogram_quantile(
  0.95,
  rate(http_request_duration_seconds_bucket[1m])
)

Screenshot should show:

p95 latency graph/value

This is the strongest proof of histogram usage.

9. Traffic Generation Terminal

Terminal running:

while true; do
  curl http://localhost:5000/api/orders
done

This demonstrates live traffic generation.

Best Final Report Order
Architecture / docker-compose
Running containers
Metrics endpoint
Prometheus target UP
Counter query
Error query
Histogram bucket query
Latency graph
p95 graph

That sequence tells the full observability story cleanly..
