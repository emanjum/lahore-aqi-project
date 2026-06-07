# PROJECT CHALLENGES AND SOLUTIONS

## 1. Collecting Reliable AQI Data

### Challenge

The first challenge was collecting air quality data continuously from the OpenWeather Air Pollution API. Since the project depended on real-time data, it was important to ensure that the hourly pipeline stored the latest information correctly without losing previous records.

### Solution

The hourly pipeline was designed to fetch AQI data automatically and store it in MongoDB Atlas. The pipeline was tested multiple times to verify that new data was being added correctly.

---

## 2. Duplicate Data in MongoDB

### Challenge

During development, the MongoDB database started storing duplicate AQI records. This caused the dataset size to increase unnecessarily and affected feature engineering and model training.

### Solution

The database saving logic was updated to use the timestamp as a unique identifier with MongoDB's `upsert` functionality. An EDA script was also created to identify and verify duplicate records before model training.

---

## 3. Feature Engineering Problems

### Challenge

Because duplicate timestamps existed in the dataset, the generated lag features also contained repeated values, resulting in incorrect training samples.

### Solution

The feature engineering pipeline was modified to sort the data chronologically and remove duplicate timestamps before generating lag features. This ensured that each feature vector represented a unique observation.

---

## 4. Model Selection

### Challenge

Different machine learning models produced different prediction accuracies, making it difficult to decide which model should be used for forecasting.

### Solution

Linear Regression, Random Forest, and XGBoost models were trained and compared using MAE, RMSE, and R² Score. Random Forest achieved the best performance and was selected as the final model for deployment.

---

## 5. Three-Day Prediction Storage

### Challenge

The prediction collection in MongoDB sometimes contained old forecast records together with new ones, causing repeated forecast dates and incorrect dashboard output.

### Solution

The prediction pipeline was updated to remove old prediction records before saving the latest three-day forecast. This ensured that the dashboard always displayed the newest predictions only.

---

## 6. Forecast Date Display

### Challenge

The dashboard initially displayed incorrect forecast dates because the prediction dates were generated using the last available data timestamp instead of the current date.

### Solution

The prediction logic was modified so that forecasts always start from the current day and correctly display Day 1, Day 2, and Day 3.

---

## 7. Moving to a Fully Cloud-Based Architecture

### Challenge

The initial implementation relied on local CSV files for storing engineered features, which was not suitable for a cloud-based system.

### Solution

The project was redesigned to use MongoDB Atlas as the primary storage for raw data, engineered features, model metrics, and predictions. Local CSV files were removed from the workflow, making the system fully cloud-based.

---

## 8. Streamlit Dashboard Deployment

### Challenge

While deploying the dashboard on Streamlit Cloud, the application failed because required secrets such as the MongoDB connection string and API key were missing.

### Solution

The required secrets were added through Streamlit Cloud's Secrets Management, allowing the application to connect securely to MongoDB Atlas and display live AQI predictions successfully.

---

## 9. GitHub Integration

### Challenge

While pushing updates to GitHub, push conflicts occurred because the remote repository contained newer changes than the local repository.

### Solution

The repository was synchronized using `git pull --rebase`, after which the latest updates were committed and pushed successfully. The Streamlit application automatically redeployed using the updated GitHub repository.

---

# Conclusion

Throughout the project, several practical challenges were encountered, including duplicate data handling, feature engineering issues, model selection, prediction storage, dashboard deployment, and cloud integration. By addressing these issues step by step, the project evolved into a fully automated cloud-based AQI forecasting system capable of collecting live data, retraining models, and providing three-day AQI predictions through an interactive Streamlit dashboard.
