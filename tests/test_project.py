import os
import joblib
import pandas as pd
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

FEATURES = [
    "CO",
    "NH3",
    "NO2",
    "OZONE",
    "PM10",
    "PM2.5",
    "SO2",
]

def test_required_model_files_exist():
    required_files = [
        "models/random_forest_classifier.joblib",
        "models/aqi_regression_model.joblib",
        "models/aqi_label_encoder.joblib",
        "models/aqi_features.joblib",
    ]
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing model file: {file_path}"

def test_feature_file_contains_expected_features():
    features = joblib.load("models/aqi_features.joblib")
    assert len(features) == len(FEATURES)
    for feature in FEATURES:
        assert feature in features

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text or "http_request_duration_seconds" in response.text or "process_cpu_seconds_total" in response.text

def test_prediction_endpoint():
    payload = {
        "CO": 1.2,
        "NH3": 20,
        "NO2": 40,
        "OZONE": 60,
        "PM10": 100,
        "PM2.5": 50,
        "SO2": 20,
    }
    response = client.post("/predict-aqi", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "predicted_aqi" in result
    assert "category" in result
    assert isinstance(result["predicted_aqi"], (int, float))
    assert isinstance(result["category"], str)
    assert 0 <= result["predicted_aqi"] <= 500
