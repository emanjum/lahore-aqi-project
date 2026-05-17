import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


df = pd.read_csv("data/features.csv")

target = "aqi"

drop_cols = ["timestamp", target]
feature_cols = [col for col in df.columns if col not in drop_cols]

X = df[feature_cols]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model training completed!")
print("MAE:", mae)
print("MSE:", mse)
print("R2 Score:", r2)

os.makedirs("models", exist_ok=True)

model.save_model("models/xgb_model.json")

print("Model saved to models/xgb_model.json")