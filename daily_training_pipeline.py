import subprocess

print("Running daily training pipeline...")

subprocess.run(["python", "feature_pipeline.py"], check=True)
subprocess.run(["python", "training_pipeline.py"], check=True)
subprocess.run(["python", "predict_next_3_days.py"], check=True)

print("Daily training pipeline completed successfully!")