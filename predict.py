import joblib
import numpy as np
import pandas as pd
import os

# ==============================
# LOAD MODELS
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

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

# ==============================
# DISPLAY LOADED INFORMATION
# ==============================

print("Models loaded successfully!")

print("\nClassifier:")
print(classifier)

print("\nRegressor:")
print(regressor)

print("\nClasses:")
print(label_encoder.classes_)

print("\nFeatures:")
print(features)

# ==============================
# TAKE INPUT
# ==============================

print("\nEnter pollutant values:")

input_data = []

for feature in features:
    value = float(input(f"Enter {feature}: "))
    input_data.append(value)

# Convert input to 2D array
input_array = pd.DataFrame(
    [input_data],
    columns=features
)

# ==============================
# PREDICT AQI
# ==============================

predicted_aqi = regressor.predict(input_array)[0]

# ==============================
# PREDICT AQI CATEGORY
# ==============================

predicted_class = classifier.predict(input_array)[0]

predicted_category = label_encoder.inverse_transform(
    [predicted_class]
)[0]

# ==============================
# DISPLAY RESULT
# ==============================

print("\n" + "=" * 40)
print("AQI PREDICTION RESULT")
print("=" * 40)

print("Predicted AQI:", round(predicted_aqi, 2))
print("Predicted Category:", predicted_category)

print("=" * 40)