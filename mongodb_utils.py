import os
import pandas as pd
import streamlit as st
import certifi
from pymongo import MongoClient, UpdateOne


# Connect to MongoDB using environment variable or Streamlit secrets
def get_mongo_client():
    uri = os.getenv("MONGODB_URI")

    if not uri:
        uri = st.secrets["MONGODB_URI"]

    client = MongoClient(uri, tlsCAFile=certifi.where())
    return client


# Return the project database
def get_database():
    client = get_mongo_client()
    return client["aqi_project"]


# Save a DataFrame into MongoDB without creating duplicate records
def save_dataframe_to_mongodb(df, collection_name):
    db = get_database()
    collection = db[collection_name]

    records = df.to_dict("records")
    operations = []

    for i, record in enumerate(records):

        # Use timestamp as the unique key for AQI data
        if "timestamp" in record:
            record["timestamp"] = pd.to_datetime(
                record["timestamp"]
            ).strftime("%Y-%m-%d %H:%M:%S")

            filter_query = {"timestamp": record["timestamp"]}

        # Use model name as the unique key for model records
        elif "model_name" in record:
            filter_query = {"model_name": record["model_name"]}

        # Use row index for any other collection
        else:
            filter_query = {"row_id": i}

        operations.append(
            UpdateOne(
                filter_query,
                {"$set": record},
                upsert=True
            )
        )

    # Write all operations to MongoDB
    if operations:
        collection.bulk_write(operations)

    print(f"Saved {len(records)} records to MongoDB collection: {collection_name}")


# Read a MongoDB collection into a pandas DataFrame
def read_collection_as_dataframe(collection_name):
    db = get_database()
    collection = db[collection_name]

    records = list(collection.find({}, {"_id": 0}))

    # Return an empty DataFrame if no records exist
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Convert timestamp column to datetime and sort chronologically
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp").reset_index(drop=True)

    return df