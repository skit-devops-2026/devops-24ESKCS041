# Monitoring and Observability Setup (Prometheus & Grafana)

This guide documents the monitoring setup for both the practice To-Do application and the AQI Prediction service, matching all requirements from the Monitoring Practice Sheet and course milestones.

---

## 1. Observability Architecture
```
+--------------------+        Scrapes /metrics (every 15s)       +-----------------------+
|  Application API   | <---------------------------------------- |   Prometheus Server   |
| (FastAPI / Express)|                                           |     (Port 9090)       |
+--------------------+                                           +-----------+-----------+
                                                                             |
                                                                             | PromQL Queries
                                                                             v
                                                                 +-----------------------+
                                                                 |   Grafana Dashboard   |
                                                                 |     (Port 3000)       |
                                                                 +-----------------------+
```

---

## 2. Metric Types Covered

| Type | Can go down? | Typical Use | Example in To-Do App | Example in AQI App |
|---|---|---|---|---|
| **Counter** | No | Total counts, cumulative events | `todos_created_total` | `http_requests_total` |
| **Gauge** | Yes | Current snapshot levels | `todos_count` | Process memory (`process_resident_memory_bytes`) |
| **Histogram**| N/A (buckets)| Durations and distributions | `http_request_duration_seconds` | `http_request_duration_seconds` |

---

## 3. PromQL Queries & Answers

1. **Current Count (Gauge):**
   ```promql
   todos_count
   ```
   *Answers:* How many to-dos exist right now.

2. **Rate of Creation (Counter):**
   ```promql
   rate(todos_created_total[5m])
   ```
   *Answers:* How many items are being created per second averaged over 5 minutes.

3. **95th Percentile Latency (Histogram Quantile):**
   ```promql
   histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
   ```
   *Answers:* 95% of requests are processed faster than this time in seconds.

4. **Resource Saturation:**
   ```promql
   process_resident_memory_bytes
   ```
   *Answers:* Actual physical RAM consumed by the service process.

---

## 4. The Four Golden Signals
1. **Latency:** How long requests take (p95 / histogram).
2. **Traffic:** How much demand/load is on the system (`rate(http_requests_total[5m])`).
3. **Errors:** Rate of failing requests (`5xx` status codes).
4. **Saturation:** Resource utilization against limits (RAM, CPU, queue length).

---

## 5. Grafana Dashboard Setup
- Data Source: Prometheus at `http://prometheus:9090`
- Dashboards exported as JSON in `monitoring/` directory for both apps:
  - `todo-practice/monitoring/todo-app-dashboard.json`
  - `monitoring/aqi-dashboard.json`

---

## 6. How to Run & Verify

### Running the To-Do Practice Monitoring Stack:
```bash
cd todo-practice
docker compose up -d --build
```
- Web UI: http://localhost:5000
- Metrics: http://localhost:5000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin / admin)
