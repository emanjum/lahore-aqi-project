import os
import joblib
import numpy as np
import pandas as pd

from mongodb_utils import read_collection_as_dataframe, save_dataframe_to_mongodb

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb


print("Reading features from MongoDB...")
df = read_collection_as_dataframe("features")

if df.empty:
    print("No features found in MongoDB.")
    exit()

df["timestamp"] = pd.to_datetime(df["timestamp"])

# Remove rows where future target is missing
df = df.dropna(subset=["target_aqi_next_24h"]).reset_index(drop=True)

target = "target_aqi_next_24h"
drop_cols = ["timestamp", "aqi", target]
feature_cols = [col for col in df.columns if col not in drop_cols]

X = df[feature_cols]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ),
    "XGBoost": xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=4,
        random_state=42
    )
}

results = []
best_model = None
best_model_name = None
best_mae = float("inf")

for name, model in models.items():
    print(f"Training {name}...")

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    results.append({
        "model_name": name,
        "mae": mae,
        "rmse": rmse,
        "r2_score": r2
    })

    if mae < best_mae:
        best_mae = mae
        best_model = model
        best_model_name = name

metrics_df = pd.DataFrame(results)

os.makedirs("models", exist_ok=True)

metrics_df.to_csv("models/model_metrics.csv", index=False)

joblib.dump(best_model, "models/best_model.pkl")

save_dataframe_to_mongodb(metrics_df, "model_metrics")

print("Model comparison completed!")
print(metrics_df)
print("Best model:", best_model_name)
print("Best MAE:", best_mae)
print("Best model saved to models/best_model.pkl")