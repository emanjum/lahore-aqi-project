import streamlit as st
import pandas as pd
import plotly.express as px

from mongodb_utils import read_collection_as_dataframe


st.set_page_config(
    page_title="Lahore AQI Predictor",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Lahore Air Quality Prediction Dashboard")
st.write("MongoDB + Machine Learning based AQI forecasting system")


def get_aqi_label(aqi):
    if aqi <= 1:
        return "Good"
    elif aqi <= 2:
        return "Fair"
    elif aqi <= 3:
        return "Moderate"
    elif aqi <= 4:
        return "Poor"
    else:
        return "Very Poor"


def get_aqi_color(aqi):
    if aqi <= 1:
        return "#00cc44"
    elif aqi <= 2:
        return "#99cc00"
    elif aqi <= 3:
        return "#ffcc00"
    elif aqi <= 4:
        return "#ff6600"
    else:
        return "#cc0000"


raw_df = read_collection_as_dataframe("raw_aqi_data")
features_df = read_collection_as_dataframe("features")
metrics_df = read_collection_as_dataframe("model_metrics")
predictions_df = read_collection_as_dataframe("predictions")


if raw_df.empty:
    st.error("No AQI data found in MongoDB.")
    st.stop()


raw_df["timestamp"] = pd.to_datetime(raw_df["timestamp"])
raw_df = raw_df.sort_values("timestamp")

latest = raw_df.iloc[-1]

current_aqi = latest["aqi"]
current_label = get_aqi_label(current_aqi)
current_color = get_aqi_color(current_aqi)


st.markdown(
    f"""
    <div style="
        background-color:{current_color};
        padding:20px;
        border-radius:12px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>Current Lahore AQI: {current_aqi} - {current_label}</h2>
        <h4>PM2.5: {latest['pm25']} µg/m³ | PM10: {latest['pm10']} µg/m³</h4>
        <p>Last Updated: {latest['timestamp']}</p>
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("PM2.5", round(latest["pm25"], 2))

with col2:
    st.metric("PM10", round(latest["pm10"], 2))

with col3:
    st.metric("AQI Category", current_label)


st.subheader("🔮 Next 3 Days AQI Forecast")

if not predictions_df.empty:
    predictions_df["timestamp"] = pd.to_datetime(predictions_df["timestamp"])
    predictions_df = predictions_df.sort_values("timestamp")

    forecast_cols = st.columns(3)

    for i, row in predictions_df.tail(3).reset_index(drop=True).iterrows():
        pred_aqi = row["predicted_aqi"]
        label = get_aqi_label(pred_aqi)
        color = get_aqi_color(pred_aqi)

        with forecast_cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color:{color};
                    padding:20px;
                    border-radius:12px;
                    color:white;
                    text-align:center;
                ">
                    <h3>{row['day']}</h3>
                    <h2>AQI {pred_aqi}</h2>
                    <p>{label}</p>
                    <p>{row['timestamp'].date()}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.warning("No prediction data found yet. Run predict_next_3_days.py first.")


st.subheader("📊 Model Performance Comparison")

if not metrics_df.empty:
    st.dataframe(metrics_df)

    fig_metrics = px.bar(
        metrics_df,
        x="model_name",
        y="mae",
        title="Model Comparison by MAE",
        labels={"mae": "Mean Absolute Error", "model_name": "Model"}
    )
    st.plotly_chart(fig_metrics, use_container_width=True)
else:
    st.warning("No model metrics found yet.")


st.subheader("📈 Historical AQI Trend")

hist_df = raw_df.copy()
hist_df["date"] = hist_df["timestamp"].dt.date

daily_avg = hist_df.groupby("date")["aqi"].mean().reset_index()

fig_hist = px.line(
    daily_avg,
    x="date",
    y="aqi",
    title="Daily Average AQI Trend",
    labels={"date": "Date", "aqi": "AQI"}
)

st.plotly_chart(fig_hist, use_container_width=True)


st.subheader("🌫️ Pollutant Breakdown")

pollutant_df = pd.DataFrame({
    "Pollutant": ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"],
    "Value": [
        latest["pm25"],
        latest["pm10"],
        latest["no2"],
        latest["so2"],
        latest["co"],
        latest["o3"]
    ]
})

fig_pollutants = px.bar(
    pollutant_df,
    x="Pollutant",
    y="Value",
    title="Latest Pollutant Levels"
)

st.plotly_chart(fig_pollutants, use_container_width=True)


st.markdown("---")
st.markdown("### Developed for AQI Prediction Project")
st.write("Data Source: OpenWeather API | Storage: MongoDB Atlas | Model: Best of Linear Regression, Random Forest, XGBoost")