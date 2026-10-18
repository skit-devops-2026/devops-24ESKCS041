# AQI Category Prediction & DevOps Observability Pipeline

An end-to-end Machine Learning and DevOps project predicting **Air Quality Index (AQI)** and air quality categories using CPCB environmental pollutant data. This repository includes complete data preprocessing, ML model inference with FastAPI, automated CI/CD pipelines (GitHub Actions and Jenkins), Docker containerization, Kubernetes manifests, and full-stack observability with **Prometheus** and **Grafana**.

---

## 1. Project Overview & Architecture

### Machine Learning
- **Regressor:** Random Forest Regressor for continuous AQI numerical calculation
- **Classifier:** Random Forest Classifier for discrete AQI category prediction (`Good`, `Moderate`, `Satisfactory`, `Poor`, `Very Poor`, `Severe`)
- **Features Used:** `CO`, `NH3`, `NO2`, `OZONE`, `PM10`, `PM2.5`, `SO2`
- **Serialization:** Joblib serialized model artifacts in `models/`

### Backend API & Metrics
- **Framework:** FastAPI with Uvicorn ASGI server
- **Endpoints:**
  - `GET /`: Health check & feature list
  - `POST /predict-aqi`: Real-time AQI prediction & category classification
  - `GET /metrics`: Native Prometheus metrics endpoint exporting request counts, duration histograms, and process memory

### Monitoring Architecture
```
[ FastAPI / Express App ]  <--- Scrapes /metrics every 15s --- [ Prometheus (9090) ]
        |                                                              |
    Port 5000                                                   PromQL Queries
                                                                       |
                                                                       v
                                                             [ Grafana (3000) ]
```

---

## 2. Directory Structure

```text
milestone2/
├── app.py                      # FastAPI API server with Prometheus metrics
├── predict.py                  # CLI inference utility
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container build instructions
├── docker-compose.yml          # Multi-container orchestration (App, Prometheus, Grafana)
├── Jenkinsfile                 # Declarative Jenkins CI pipeline
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions automated test & build workflow
├── data/
│   └── cpcb_raw.csv            # CPCB pollutant dataset
├── models/                     # Saved trained models & encoders
├── tests/
│   └── test_project.py         # Pytest test suite for models and API
├── monitoring/
│   ├── prometheus.yml          # Prometheus scrape target configuration
│   ├── aqi-dashboard.json      # Grafana dashboard JSON model for AQI service
│   └── grafana_dashboard.jpg   # Exported dashboard screenshot
├── docs/
│   ├── MONITORING.md           # Observability reference & Golden Signals guide
│   └── grafana_dashboard.jpg   # Visual dashboard evidence
└── todo-practice/              # Complete beginner practice sheet application
    ├── server.js               # Node.js + Express app with prom-client
    ├── package.json
    ├── Dockerfile
    ├── docker-compose.yml      # Orchestrates Node App, MongoDB, Prometheus, Grafana
    ├── prometheus.yml          # Scrapes app:5000
    ├── utils.js & test.js      # Unit tests
    ├── k8s-practice/           # Kubernetes Deployments & Services
    └── monitoring/             # Exported Grafana dashboard JSON
```

---

## 3. Quickstart & Local Setup

### Running with Docker Compose (Recommended)
To launch the full observability stack with one command:
```bash
docker compose up -d --build
```
Access the services at:
- **Application API:** [http://localhost:5000](http://localhost:5000)
- **Metrics Endpoint:** [http://localhost:5000/metrics](http://localhost:5000/metrics)
- **Prometheus Dashboard:** [http://localhost:9090](http://localhost:9090)
- **Grafana Visualization:** [http://localhost:3000](http://localhost:3000) *(User: `admin`, Password: `admin`)*

---

## 4. API Usage Example

### Predict AQI (`POST /predict-aqi`)
```bash
curl -X POST "http://localhost:5000/predict-aqi"   -H "Content-Type: application/json"   -d '{
    "CO": 1.2,
    "NH3": 20.0,
    "NO2": 40.0,
    "OZONE": 60.0,
    "PM10": 100.0,
    "PM2.5": 50.0,
    "SO2": 20.0
  }'
```

**Response:**
```json
{
  "predicted_aqi": 112.45,
  "category": "Moderate"
}
```

---

## 5. Observability & Golden Signals (Self-Check Verified)

| Signal | Description | PromQL Query |
|---|---|---|
| **Latency** | 95th Percentile request duration | `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))` |
| **Traffic** | Requests per second | `sum(rate(http_requests_total[5m]))` |
| **Errors** | Failing HTTP status codes | `sum(rate(http_requests_total{status=~"5.."}[5m]))` |
| **Saturation** | Memory and CPU resource usage | `process_resident_memory_bytes` |

---

## 6. Testing & CI Pipeline

Run tests locally:
```bash
pytest -v tests/
```

Both **GitHub Actions** (`.github/workflows/ci.yml`) and **Jenkins** (`Jenkinsfile`) automate:
1. Environment initialization
2. Dependency installation
3. Model and API verification tests
4. Docker container build and image packaging
