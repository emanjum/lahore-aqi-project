import pandas as pd
import hopsworks
import streamlit as st

print("Loading features...")
df = pd.read_csv("data/features.csv")

print("Connecting to Hopsworks...")
project = hopsworks.login(
    api_key_value=st.secrets["HOPSWORKS_API_KEY"]
)

fs = project.get_feature_store()

print("Creating or getting feature group...")
fg = fs.get_or_create_feature_group(
    name="lahore_air_quality_features",
    version=1,
    primary_key=["timestamp"],
    description="Lahore AQI engineered features with lag variables"
)

print("Uploading features...")
fg.insert(df)

print("Features uploaded successfully!")
print("Rows uploaded:", len(df))