import joblib
import pandas as pd
from datetime import timedelta
from mongodb_utils import (
    read_collection_as_dataframe,
    save_dataframe_to_mongodb,
    clear_collection
)


# Load the best trained model
print("Loading best trained model...")
model = joblib.load("models/best_model.pkl")


# Read latest engineered features from MongoDB
print("Reading latest features from MongoDB...")
df = read_collection_as_dataframe("features")


# Stop if feature data is missing
if df.empty:
    print("No features found in MongoDB.")
    exit()


# Convert timestamp and sort data chronologically
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)


# Get the most recent feature row
last_row = df.iloc[-1].copy()


# Remove non-feature columns before prediction
drop_cols = ["timestamp", "aqi", "target_aqi_next_24h"]
feature_cols = [col for col in df.columns if col not in drop_cols]


# Store next 3 days predictions
predictions = []


# Use latest timestamp as forecast starting point
current_timestamp = pd.Timestamp.now().normalize()


# Generate AQI predictions for the next 3 days
for day in range(1, 4):
    X = pd.DataFrame([last_row[feature_cols]])

    pred = model.predict(X)[0]
    pred = round(float(pred), 2)

    forecast_date = current_timestamp + timedelta(days=day)

    predictions.append({
        "timestamp": forecast_date,
        "day": f"Day {day}",
        "predicted_aqi": pred
    })

    # Update AQI lag values for next forecast step
    last_row["aqi_lag3"] = last_row["aqi_lag2"]
    last_row["aqi_lag2"] = last_row["aqi_lag1"]
    last_row["aqi_lag1"] = pred


# Convert predictions list to DataFrame
result = pd.DataFrame(predictions)


# Clear old predictions before saving new forecast
clear_collection("predictions")


# Save latest predictions to MongoDB
save_dataframe_to_mongodb(result, "predictions")


# Display forecast results
print("Next 3 Days AQI Forecast:")
print(result)
print("Predictions saved to MongoDB collection: predictions")