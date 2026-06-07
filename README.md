# 🌤️ Lahore Air Quality Prediction Dashboard

## 🚀 Live Demo

https://lahore-aqi-project-et3ijapxuaflm7cabd29jt.streamlit.app

# Lahore AQI Prediction Project

A cloud-based machine learning system for monitoring and forecasting Lahore's Air Quality Index (AQI).

## Technologies Used
- Python
- OpenWeather API
- MongoDB Atlas
- Scikit-learn
- XGBoost
- Streamlit
- GitHub Actions

## Features
- Hourly AQI data collection from OpenWeather API
- Automated feature engineering
- Training of 3 machine learning models:
  - Linear Regression
  - Random Forest
  - XGBoost
- Automatic best model selection based on MAE
- 3-day AQI forecasting
- Cloud storage using MongoDB Atlas
- Interactive Streamlit dashboard
- Fully automated hourly and daily pipelines

## Project Workflow
1. Fetch AQI data every hour
2. Store raw data in MongoDB
3. Generate lag and time-based features
4. Train multiple models daily
5. Select the best-performing model
6. Predict AQI for the next 3 days
7. Save predictions to MongoDB
8. Visualize results in Streamlit

## Best Model
The system automatically selects the best model each day based on Mean Absolute Error (MAE).

## Automation
- Hourly Pipeline: Updates raw data and features
- Daily Pipeline: Retrains models and generates forecasts

## Repository
https://github.com/emanjum/lahore-aqi-project

## Author
Eman Anjum
