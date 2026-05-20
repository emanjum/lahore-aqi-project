import os
import pandas as pd
import streamlit as st
import certifi
from pymongo import MongoClient, UpdateOne


def get_mongo_client():
    # GitHub Actions / local terminal uses environment variable
    uri = os.getenv("MONGODB_URI")

    # Streamlit Cloud uses st.secrets
    if not uri:
        uri = st.secrets["MONGODB_URI"]

    client = MongoClient(uri, tlsCAFile=certifi.where())
    return client


def get_database():
    client = get_mongo_client()
    return client["aqi_project"]


def save_dataframe_to_mongodb(df, collection_name):
    db = get_database()
    collection = db[collection_name]

    records = df.to_dict("records")

    operations = []

    for i, record in enumerate(records):
        if "timestamp" in record:
            filter_query = {"timestamp": str(record["timestamp"])}
            record["timestamp"] = str(record["timestamp"])

        elif "model_name" in record:
            filter_query = {"model_name": record["model_name"]}

        else:
            filter_query = {"row_id": i}

        operations.append(
            UpdateOne(
                filter_query,
                {"$set": record},
                upsert=True
            )
        )

    if operations:
        collection.bulk_write(operations)

    print(f"Saved {len(records)} records to MongoDB collection: {collection_name}")


def read_collection_as_dataframe(collection_name):
    db = get_database()
    collection = db[collection_name]

    records = list(collection.find({}, {"_id": 0}))

    if not records:
        return pd.DataFrame()

    return pd.DataFrame(records)