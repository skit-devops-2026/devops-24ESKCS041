# AirQualityPrediction

An end-to-end Machine Learning and DevOps project for predicting **Air Quality Index (AQI)** and its corresponding air-quality category using pollutant data collected from the **Central Pollution Control Board (CPCB)** through the Government of India's Open Government Data Platform.

The project combines:

- Data collection and preprocessing
- Machine Learning
- AQI regression and classification
- FastAPI REST API
- Web-based frontend dashboard
- Automated testing with Pytest
- GitHub Actions CI
- Jenkins CI pipeline
- Git and GitHub workflow

---

## 1. Project Overview

Air pollution is a major environmental and public-health concern. Monitoring pollutant concentrations and estimating the Air Quality Index can help users understand the current air-quality condition.

This project takes pollutant concentration values as input and uses trained Machine Learning models to predict:

1. Numerical AQI value
2. AQI category

### Pollutants Used

The prediction model uses the following pollutants:

| Pollutant | Description |
|---|---|
| CO | Carbon Monoxide |
| NH3 | Ammonia |
| NO2 | Nitrogen Dioxide |
| OZONE | Ozone |
| PM10 | Particulate Matter 10 |
| PM2.5 | Particulate Matter 2.5 |
| SO2 | Sulfur Dioxide |

---

## 2. Features

### Machine Learning

- Random Forest Regressor for numerical AQI prediction
- Random Forest Classifier for AQI category prediction
- Joblib-based model serialization
- Feature validation
- AQI range validation

### Backend

- FastAPI REST API
- `/` health/home endpoint
- `/predict-aqi` prediction endpoint
- Automatic API documentation through Swagger UI

### Frontend

- Web-based AQI dashboard
- Pollutant input fields
- AQI prediction display
- AQI category display
- API integration using JavaScript

### DevOps

- Git and GitHub version control
- Feature branches
- Pull Requests
- GitHub Actions CI
- Automated Pytest test suite
- Jenkins pipeline
- Automated dependency installation
- Automated project verification

---

## 3. System Architecture

```text
                    CPCB / data.gov.in
                            |
                            v
                    Data Collection
                            |
                            v
                   Data Preprocessing
                            |
                            v
                    Feature Preparation
                            |
                            v
                 Machine Learning Training
                     /              \
                    /                \
                   v                  v
          AQI Regression       AQI Classification
             Model                  Model
                \                    /
                 \                  /
                  v                v
                     FastAPI Backend
                            |
                    POST /predict-aqi
                            |
                            v
                    Web Dashboard
                            |
                            v
                  AQI + Category Result
