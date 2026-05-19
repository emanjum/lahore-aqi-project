import joblib
import pandas as pd
from datetime import timedelta
from mongodb_utils import read_collection_as_dataframe, save_dataframe_to_mongodb


print("Loading best trained model...")
model = joblib.load("models/best_model.pkl")

print("Reading latest features from MongoDB...")
df = read_collection_as_dataframe("features")

if df.empty:
    print("No features found in MongoDB.")
    exit()

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)

last_row = df.iloc[-1].copy()

drop_cols = ["timestamp", "aqi", "target_aqi_next_24h"]
feature_cols = [col for col in df.columns if col not in drop_cols]

predictions = []

current_timestamp = last_row["timestamp"]

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

result = pd.DataFrame(predictions)

save_dataframe_to_mongodb(result, "predictions")

print("Next 3 Days AQI Forecast:")
print(result)
print("Predictions saved to MongoDB collection: predictions")