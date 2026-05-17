import hopsworks
import streamlit as st
import os

print("Connecting to Hopsworks...")
project = hopsworks.login(
    api_key_value=st.secrets["HOPSWORKS_API_KEY"]
)

mr = project.get_model_registry()

print("Creating model in registry...")
model = mr.python.create_model(
    name="lahore_aqi_model",
    metrics={
        "mae": 0.0056,
        "r2_score": 0.9978
    },
    description="XGBoost model for Lahore AQI 3-day forecasting"
)

print("Saving model to registry...")
model.save("models")

print("Model uploaded successfully!")