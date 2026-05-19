import os
import pandas as pd
from mongodb_utils import read_collection_as_dataframe, save_dataframe_to_mongodb


output_file = "data/features.csv"

print("Reading raw AQI data from MongoDB...")
df = read_collection_as_dataframe("raw_aqi_data")

if df.empty:
    print("No raw data found in MongoDB.")
    exit()

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

# Time-based features
df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day
df["month"] = df["timestamp"].dt.month
df["day_of_week"] = df["timestamp"].dt.dayofweek

# Change-rate feature
df["aqi_change_rate"] = df["aqi"].diff()

# Lag features
pollutant_cols = ["pm25", "pm10", "no2", "so2", "co", "o3"]
lag_cols = pollutant_cols + ["aqi"]

for col in lag_cols:
    df[f"{col}_lag1"] = df[col].shift(1)
    df[f"{col}_lag2"] = df[col].shift(2)
    df[f"{col}_lag3"] = df[col].shift(3)

# Target column: AQI 24 hours in the future
df["target_aqi_next_24h"] = df["aqi"].shift(-24)

# Remove rows with missing lag/target values
df = df.dropna().reset_index(drop=True)

os.makedirs("data", exist_ok=True)
df.to_csv(output_file, index=False)

save_dataframe_to_mongodb(df, "features")

print("Feature engineering completed!")
print("Rows saved:", len(df))
print("Columns:", list(df.columns))
print(df.head())