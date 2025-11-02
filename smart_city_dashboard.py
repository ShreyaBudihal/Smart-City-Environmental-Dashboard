import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(page_title="Smart City Dashboard", layout="wide")

st.title("🏙️ Smart City Environmental Dashboard")
st.markdown("Get **real-time weather and air quality insights** for your city 🌤️")

# ----------------------------
# Input Section
# ----------------------------
col1, col2 = st.columns(2)
with col1:
    city = st.text_input("Enter City", "London")
with col2:
    api_key = st.text_input("Enter OpenWeatherMap API Key", type="password")

# ----------------------------
# Main Logic
# ----------------------------
if api_key and city:
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    w = requests.get(weather_url).json()

    if w.get("coord"):
        lat, lon = w["coord"]["lat"], w["coord"]["lon"]
        air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        a = requests.get(air_url).json()

        # ----------------------------
        # Weather Summary Metrics
        # ----------------------------
        st.subheader(f"🌤️ Current Weather in {city.title()}")
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡 Temperature (°C)", f"{w['main']['temp']} °C")
        col2.metric("💧 Humidity (%)", f"{w['main']['humidity']} %")
        col3.metric("🌬 Wind Speed (m/s)", f"{w['wind']['speed']}")

        # Add Metric Card Styling
        style_metric_cards(background_color="#fafafa", border_left_color="#6c63ff")

        # ----------------------------
        # Air Quality Visualization
        # ----------------------------
        aq = a["list"][0]["components"]
        df = pd.DataFrame(aq.items(), columns=["Pollutant", "Concentration (μg/m³)"])
        st.subheader("🌫️ Air Quality Levels")

        fig = px.bar(
            df,
            x="Pollutant",
            y="Concentration (μg/m³)",
            color="Concentration (μg/m³)",
            color_continuous_scale="Plasma",
            text_auto=".2f"
        )
        fig.update_layout(
            title=f"Air Quality Components in {city.title()}",
            xaxis_title="Pollutant",
            yaxis_title="Concentration (μg/m³)",
            template="plotly_white",
            title_x=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------
        # Extra Metrics (example layout grid)
        # ----------------------------
        st.subheader("📊 Additional Data Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Visibility (m)", f"{w['visibility']}")
        col2.metric("Pressure (hPa)", f"{w['main']['pressure']}")
        col3.metric("Feels Like (°C)", f"{w['main']['feels_like']}")
        style_metric_cards(background_color="#fafafa", border_left_color="#6c63ff")

    else:
        st.error("City not found. Please check the spelling or try another location.")
else:
    st.info("Please enter your city and a valid OpenWeatherMap API key to view results.")
