import streamlit as st
import pandas as pd
import os
import joblib
import numpy as np
from keras.models import load_model
from db import get_flare_data_from_db
from datetime import datetime, timedelta

@st.cache_resource
def load_keras_model_and_scaler():
    model_path = os.path.join("models", "solarflare_model.h5")
    scaler_path = os.path.join("models", "scaler.pkl")

    if not os.path.exists(model_path):
        st.error(f"Keras model file not found at '{model_path}'.")
        return None, None
    if not os.path.exists(scaler_path):
        st.error(f"Scaler file not found at '{scaler_path}'.")
        return None, None

    try:
        model = load_model(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except Exception as e:
        st.error(f"Error loading model or scaler: {e}")
        return None, None

def prediction_page():
    st.title("☀️ Solar Flare Event Prediction")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Select start date", datetime.now() - timedelta(days=7))
    with col2:
        end_date = st.date_input("Select end date", datetime.now())

    if start_date > end_date:
        st.error("Start date must be before or equal to end date.")
        return

    model, scaler = load_keras_model_and_scaler()
    if model is None or scaler is None:
        return

    if st.button("🔮 Predict Solar Flares"):
        with st.spinner("Fetching data and making predictions..."):
            data_df = get_flare_data_from_db(start_date, end_date)

            if data_df.empty:
                st.warning("No data found for the selected period.")
                return

            try:
                # Example feature extraction - you must adjust this to your model input
                # For demonstration, let's say you use 'begin_time' to create a feature like days since start_date
                features = pd.DataFrame({
                    "days_since_start": (data_df['begin_time'] - pd.Timestamp(start_date)).dt.days
                })

                # Scale features before prediction
                X_scaled = scaler.transform(features)

                # Predict using keras model - assuming binary classification (output prob)
                preds_prob = model.predict(X_scaled)
                # Thresholding at 0.5 for Yes/No prediction
                preds = (preds_prob.flatten() >= 0.5)

                result_df = pd.DataFrame({
                    "Date": data_df['begin_time'].dt.date,
                    "Solar Flare Event": ["Yes" if pred else "No" for pred in preds]
                })

                st.success("Prediction completed!")
                st.dataframe(result_df)

            except Exception as e:
                st.error(f"Error during prediction: {e}")
