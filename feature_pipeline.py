import os
import pandas as pd


input_file = "data/raw_aqi_data.csv"
output_file = "data/features.csv"

df = pd.read_csv(input_file)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day
df["month"] = df["timestamp"].dt.month
df["day_of_week"] = df["timestamp"].dt.dayofweek

df["aqi_change_rate"] = df["aqi"].diff()

pollutant_cols = ["pm25", "pm10", "no2", "so2", "co", "o3"]
lag_cols = pollutant_cols + ["aqi"]

for col in lag_cols:
    df[f"{col}_lag1"] = df[col].shift(1)
    df[f"{col}_lag2"] = df[col].shift(2)
    df[f"{col}_lag3"] = df[col].shift(3)

df = df.dropna().reset_index(drop=True)

os.makedirs("data", exist_ok=True)
df.to_csv(output_file, index=False)

print("Feature engineering completed!")
print("Rows saved:", len(df))
print("Columns:", list(df.columns))
print(df.head())