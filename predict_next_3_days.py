import pandas as pd
import xgboost as xgb


model = xgb.XGBRegressor()
model.load_model("models/xgb_model.json")

df = pd.read_csv("data/features.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

last_row = df.sort_values("timestamp").iloc[-1].copy()

feature_cols = [
    col for col in df.columns
    if col not in ["timestamp", "aqi"]
]

predictions = []

for day in range(1, 4):
    X = pd.DataFrame([last_row[feature_cols]])

    pred = model.predict(X)[0]
    pred = round(float(pred), 2)

    predictions.append({
        "day": f"Day {day}",
        "predicted_aqi": pred
    })

    last_row["aqi_lag3"] = last_row["aqi_lag2"]
    last_row["aqi_lag2"] = last_row["aqi_lag1"]
    last_row["aqi_lag1"] = pred

result = pd.DataFrame(predictions)

print("Next 3 Days AQI Forecast:")
print(result)