import os
import pandas as pd
import numpy as np
from keras.models import load_model
from datetime import datetime

# Constants
DATA_PATH = "solar_flare_cleaned.csv"  # 👈 Update this to your CSV filename
MODEL_PATH = "solarflare_model.h5"

# Load model
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
else:
    raise FileNotFoundError(f"[❌] Model file not found: {MODEL_PATH}")

# Load dataset and preprocess
df = pd.read_csv(DATA_PATH, parse_dates=["beginTime"])
df.rename(columns={"beginTime": "date"}, inplace=True)

def get_features_from_date(selected_date):
    """
    Extract features for a given date.
    :param selected_date: datetime.date
    :return: np.array of features or raise ValueError if date not found
    """
    selected_date = pd.to_datetime(selected_date)

    row = df[df["date"].dt.date == selected_date.date()]
    if row.empty:
        raise ValueError(f"No data available for date: {selected_date.date()}")

    # Drop the 'date' column and get features only
    features = row.drop(columns=["date", "EventOccurred"], errors="ignore").values
    return features

def predict_solar_flare(selected_date):
    """
    Predict solar flare for a given date.
    :param selected_date: datetime.date
    :return: prediction result
    """
    try:
        features = get_features_from_date(selected_date)
        prediction = model.predict(features)
        return prediction[0][0]  # Assuming output is a single probability value
    except Exception as e:
        return f"[❌] Prediction failed: {e}"
