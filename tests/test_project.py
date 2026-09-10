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
    """Check that all trained ML model files are available."""

    required_files = [
        "models/random_forest_classifier.joblib",
        "models/aqi_regression_model.joblib",
        "models/aqi_label_encoder.joblib",
        "models/aqi_features.joblib",
    ]

    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing model file: {file_path}"


def test_feature_file_contains_expected_features():
    """Check that the saved feature list matches the API input."""

    features = joblib.load("models/aqi_features.joblib")

    assert len(features) == 999

    for feature in FEATURES:
        assert feature in features


def test_prediction_endpoint():
    """Check that the FastAPI prediction endpoint returns a valid response."""

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


def test_prediction_aqi_range():
    """Check that predicted AQI is within the expected AQI range."""

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

    assert 0 <= result["predicted_aqi"] <= 500


def test_home_endpoint():
    """Check that the API root endpoint is working."""

    response = client.get("/")

    assert response.status_code == 200