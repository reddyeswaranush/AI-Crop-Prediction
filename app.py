import streamlit as st
import requests
from datetime import datetime, timedelta
from google import genai

# API
client = genai.Client(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# PAGE
st.set_page_config(
    page_title="AI Crop Prediction",
    page_icon="🌾"
)

st.title("🌾 AI Crop Prediction")
st.write("Smart AI crop recommendations")

# DATA
season_months = {
    "kharif": (6, 10),
    "rabi": (11, 3),
    "summer": (4, 5)
}

kerala_soil_map = {
    "695001": "Laterite Soil",
    "671121": "Laterite Soil",
    "671315": "Sandy Soil"
}

# GEO
def geocode_nominatim(pincode):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": pincode,
        "format": "json"
    }
    try:

        r = requests.get(
            url,
            params=params,
            headers={"User-Agent": "CropAI"},
            timeout=20
        )
        data = r.json()

        if data:
            return [
                float(data[0]["lat"]),
                float(data[0]["lon"])
            ]

        return None

    except:
        return None

# SOIL
def get_soil(pincode):

    return kerala_soil_map.get(
        str(pincode),
        "Unknown Soil Type"
    )

# WEATHER
def get_weather(lat_lon, season):

    lat, lon = lat_lon

    now = datetime.now()

    start_month, end_month = season_months.get(
        season.lower(),
        (6, 10)
    )

    start_year = now.year
    end_year = now.year

    if end_month < start_month:
        end_year += 1

    start_date = datetime(
        start_year,
        start_month,
        1
    ).strftime("%Y-%m-%d")

    end_day = (
        datetime(end_year, end_month + 1, 1)
        - timedelta(days=1)
    ).day

    end_date = datetime(
        end_year,
        end_month,
        end_day
    ).strftime("%Y-%m-%d")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,"
        f"temperature_2m_min,"
        f"precipitation_sum,"
        f"relative_humidity_2m_max"
        f"&timezone=auto"
    )

    try:

        response = requests.get(url, timeout=60)
        data = response.json()
        daily = data.get("daily", {})
        temp_max = daily.get("temperature_2m_max",[])
        temp_min = daily.get("temperature_2m_min",[])
        rainfall = daily.get("precipitation_sum",[])
        humidity = daily.get(
            "relative_humidity_2m_max",
            []
        )
        avg_temp = (
            sum(temp_max + temp_min)
            / (len(temp_max) + len(temp_min))
            if temp_max and temp_min
            else 27
        )
        total_rainfall = (sum(rainfall)if rainfall else 3100)
        avg_humidity = (sum(humidity) / len(humidity)if humidity else 73)
        return {
            "season": season,
            "avg_temp": round(avg_temp, 2),
            "total_rainfall": round(total_rainfall, 2),
            "avg_humidity": round(avg_humidity, 2)
        }

    except:

        return {
            "season": season,
            "avg_temp": 27,
            "total_rainfall": 3100,
            "avg_humidity": 73
        }

# GEMINI
def get_crop_suggestions(
    soil_type,
    season,
    weather_summary,
    budget
):

    prompt = f"""
You are the world's best agricultural advisor.

Farm details:
- Soil type: {soil_type}
- Season: {season}
- Average Temperature: {weather_summary['avg_temp']}°C
- Total Rainfall: {weather_summary['total_rainfall']} mm
- Average Humidity: {weather_summary['avg_humidity']}%
- Budget: ₹{budget}

Suggest 5 suitable crops.

For each crop provide:
- Why suitable
- Input cost
- Market price
- Profit range
- Farming tips
"""
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
    
    except Exception as e:
        return f"Error: {str(e)}"

# UI
pincode = st.text_input("Enter Pincode")
season = st.selectbox("Select Season",["kharif", "rabi", "summer"])
budget = st.number_input("Enter Budget (₹)",min_value=1000)

# BUTTON
if st.button("Predict Crops"):
    with st.spinner("Generating recommendations..."):
        lat_lon = geocode_nominatim(pincode)
        if lat_lon is None:
            st.error("Invalid Pincode")
        else:
            soil_type = get_soil(pincode)
            weather_summary = get_weather(
                lat_lon,
                season
            )
            st.success(
                "Analysis Completed"
            )
            st.write(
                f" Location: {lat_lon}"
            )
            st.write(
                f" Soil Type: {soil_type}"
            )
            st.write(weather_summary)
            suggestions = get_crop_suggestions(
                soil_type,
                season,
                weather_summary,
                budget
            )
            st.markdown(suggestions)
