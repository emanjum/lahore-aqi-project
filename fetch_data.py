import os
import time
import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from mongodb_utils import save_dataframe_to_mongodb


LAT = 31.5204
LON = 74.3587
API_KEY = st.secrets["OPENWEATHERMAP_API_KEY"]

end_date = datetime.now()
start_date = end_date - timedelta(days=180)

start_unix = int(start_date.timestamp())
end_unix = int(end_date.timestamp())

url = (
    "http://api.openweathermap.org/data/2.5/air_pollution/history"
    f"?lat={LAT}&lon={LON}&start={start_unix}&end={end_unix}&appid={API_KEY}"
)

response = requests.get(url)
print("Status Code:", response.status_code)

data = response.json()

if response.status_code != 200:
    print("Error response:")
    print(data)
    exit()

rows = []

for item in data["list"]:
    components = item["components"]

    row = {
        "timestamp": datetime.fromtimestamp(item["dt"]),
        "aqi": item["main"]["aqi"],
        "pm25": components.get("pm2_5"),
        "pm10": components.get("pm10"),
        "no2": components.get("no2"),
        "so2": components.get("so2"),
        "co": components.get("co"),
        "o3": components.get("o3"),
    }

    rows.append(row)

df = pd.DataFrame(rows)

os.makedirs("data", exist_ok=True)

file_path = "data/raw_aqi_data.csv"
df.to_csv(file_path, index=False)

print("Historical data saved successfully!")
print("Rows saved:", len(df))
print(df.head())
df.to_csv(file_path, index=False)
save_dataframe_to_mongodb(df, "raw_aqi_data")
print("Historical data saved successfully!")
print("Rows saved:", len(df))
print(df.head())