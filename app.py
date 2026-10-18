from fastapi import FastAPI
import joblib
import pandas as pd
import os
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

# ==========================================
# APP
# ==========================================

app = FastAPI(
    title="AQI Prediction API",
    description="API for AQI prediction using Machine Learning",
    version="1.0"
)

# Instrument FastAPI app with Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# ==========================================
# LOAD MODELS
# ==========================================

classifier = joblib.load(
    os.path.join(MODEL_DIR, "random_forest_classifier.joblib")
)

regressor = joblib.load(
    os.path.join(MODEL_DIR, "aqi_regression_model.joblib")
)

label_encoder = joblib.load(
    os.path.join(MODEL_DIR, "aqi_label_encoder.joblib")
)

features = joblib.load(
    os.path.join(MODEL_DIR, "aqi_features.joblib")
)

# ==========================================
# HOME ROUTE
# ==========================================

@app.get("/")
def home():
    return {
        "message": "AQI Prediction API is running!",
        "features": features,
        "status": "healthy"
    }

# ==========================================
# AQI PREDICTION
# ==========================================

@app.post("/predict-aqi")
def predict_aqi(data: dict):
    # Create input DataFrame
    input_data = pd.DataFrame(
        [[data[feature] for feature in features]],
        columns=features
    )

    # AQI prediction
    predicted_aqi = regressor.predict(input_data)[0]

    # Category prediction
    predicted_class = classifier.predict(input_data)[0]

    predicted_category = label_encoder.inverse_transform(
        [predicted_class]
    )[0]

    return {
        "predicted_aqi": round(float(predicted_aqi), 2),
        "category": predicted_category
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=False)
