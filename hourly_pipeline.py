import subprocess

print("Running hourly AQI pipeline...")

subprocess.run(["python", "fetch_data.py"], check=True)
subprocess.run(["python", "feature_pipeline.py"], check=True)

print("Hourly pipeline completed successfully!")