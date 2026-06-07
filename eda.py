# Exploratory Data Analysis (EDA)
# Lahore AQI Prediction Project

import os
import pandas as pd
import matplotlib.pyplot as plt

from mongodb_utils import read_collection_as_dataframe


# Read AQI data from MongoDB

print("Reading raw AQI data from MongoDB...")

df = read_collection_as_dataframe("raw_aqi_data")

if df.empty:
    print("No AQI data found in MongoDB.")
    exit()


# Data preprocessing

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)


# Remove duplicate rows
df = df.drop_duplicates().reset_index(drop=True)


# Basic dataset information

print("Dataset Shape")
print(df.shape)

print("\nDataset Columns")
print(df.columns)

print("\nFirst 5 Rows")
print(df.head())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nStatistical Summary")
print(df.describe())


# Create output folder for plots

os.makedirs("eda_outputs", exist_ok=True)

