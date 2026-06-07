import pandas as pd
from mongodb_utils import read_collection_as_dataframe, save_dataframe_to_mongodb


# Read raw AQI data from MongoDB
print("Reading raw AQI data from MongoDB...")
df = read_collection_as_dataframe("raw_aqi_data")

# Exit if no data exists
if df.empty:
    print("No raw data found in MongoDB.")
    exit()


# Convert timestamp column to datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort data chronologically
df = df.sort_values("timestamp").reset_index(drop=True)

# Remove duplicate timestamps
df = df.drop_duplicates(subset=["timestamp"]).reset_index(drop=True)


# Create time-based features
df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day
df["month"] = df["timestamp"].dt.month
df["day_of_week"] = df["timestamp"].dt.dayofweek


# Calculate AQI change rate
df["aqi_change_rate"] = df["aqi"].diff()


# Pollutant columns used for lag features
pollutant_cols = [
    "pm25",
    "pm10",
    "no2",
    "so2",
    "co",
    "o3"
]

# Include AQI in lag features
lag_cols = pollutant_cols + ["aqi"]


# Generate lag features
for col in lag_cols:
    df[f"{col}_lag1"] = df[col].shift(1)
    df[f"{col}_lag2"] = df[col].shift(2)
    df[f"{col}_lag3"] = df[col].shift(3)


# Create target column (AQI after 24 hours)
df["target_aqi_next_24h"] = df["aqi"].shift(-24)


# Remove rows containing NaN values
df = df.dropna().reset_index(drop=True)

# Final duplicate check
df = df.drop_duplicates().reset_index(drop=True)


# Save engineered features to MongoDB Atlas
save_dataframe_to_mongodb(df, "features")


# Display summary
print("Feature engineering completed!")
print("Rows saved:", len(df))
print("Columns:", list(df.columns))
print(df.head())