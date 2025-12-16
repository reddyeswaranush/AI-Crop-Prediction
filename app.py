import requests
from datetime import datetime, timedelta
import google.generativeai as genai

# ----- Hugging Face API Settings -----
GOOGLE_API_KEY = "AIzaSyAAtFP4JvQCDPrQevQrNvd2CUxVJZTGWyE"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_crop_suggestions(soil_type, season, weather_summary, budget):
    prompt = f"""
You are the world's best agricultural advisor.

Farm details:
- Soil type: {soil_type}
- Season: {season}
- Average Temperature: {weather_summary['avg_temp']}°C
- Total Rainfall: {weather_summary['total_rainfall']} mm
- Average Humidity: {weather_summary['avg_humidity']}%
- Budget: ₹{budget}

Output format (STRICT):
List exactly 5–7 crops. 
For each crop:
1. Write the crop name in **bold**.  
2. Give a **5–7 line explanation** why it is suitable.  
3. Add:
   - Approx. **input cost** (₹ per acre).  
   - Approx. **market price** (₹ per kg or quintal).  
   - Approx. **profit range** (₹).  
   - 6-7 suggestions on what to take care of that crop.

Do NOT write essays or intros. Just crops in this structured format.
"""
    response = model.generate_content(prompt)

    # Save response to file for later use
    with open("crop_suggestions.txt", "w", encoding="utf-8") as f:
        f.write(response.text)

    # Return clean text instead of forcing JSON
    return {
        "message": "Crop suggestions generated successfully",
        "crops": response.text
    }


# ----- Season Months -----
season_months = {
    "kharif": (6, 10),
    "rabi": (11, 3),
    "summer": (4, 5)
}

# ----- Kerala Soil Map -----
kerala_soil_map = {
    "695001": "Laterite Soil", "695014": "Coastal Alluvial Soil",
    "691001": "Laterite Soil", "691013": "Riverine Alluvial Soil",
    "689645": "Laterite Soil", "689121": "Forest Soil",
    "688001": "Coastal Alluvial Soil", "688524": "Mangrove Soil",
    "686001": "Laterite Soil", "686004": "Alluvial Soil",
    "685584": "Forest Soil", "685602": "Hill Soil",
    "682001": "Coastal Alluvial Soil", "683101": "Riverine Alluvial Soil",
    "680001": "Laterite Soil", "680567": "Alluvial Soil",
    "678001": "Black Soil (Regur)", "678551": "Alluvial Soil",
    "676505": "Laterite Soil", "676101": "Sandy Soil",
    "673001": "Laterite Soil", "673032": "Coastal Alluvial Soil",
    "673121": "Forest Soil", "673577": "Hill Soil",
    "670001": "Laterite Soil", "670307": "Sandy Soil",
    "671121": "Laterite Soil", "671315": "Sandy Soil"
}

# ----- Geocode Pincode -----
def geocode_nominatim(pincode):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": pincode, "format": "json"}
    try:
        r = requests.get(url, params=params, headers={"User-Agent": "CropAI"}, timeout=20)
        r.raise_for_status()
        data = r.json()
        if data:
            return [float(data[0]['lat']), float(data[0]['lon'])]
        else:
            return None
    except requests.exceptions.RequestException:
        return None
    

# ----- Get Soil Type -----
def get_soil(pincode):
    return kerala_soil_map.get(str(pincode), "Unknown Soil Type")


# ----- Get Seasonal Weather Summary -----
def get_weather(lat_lon, season):
    lat, lon = lat_lon
    now = datetime.now()
    start_month, end_month = season_months.get(season.lower(), (6, 10))
    
    start_year = now.year
    end_year = now.year
    if end_month < start_month:
        end_year += 1

    start_date = datetime(start_year, start_month, 1).strftime("%Y-%m-%d")
    end_day = (datetime(end_year, end_month + 1, 1) - timedelta(days=1)).day
    end_date = datetime(end_year, end_month, end_day).strftime("%Y-%m-%d")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_max"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", {})

        # Extract safely
        temp_max = daily.get("temperature_2m_max", [])
        temp_min = daily.get("temperature_2m_min", [])
        rainfall = daily.get("precipitation_sum", [])
        humidity = daily.get("relative_humidity_2m_max", [])

        # Field-wise safe calculations
        avg_temp = (
            sum(temp_max + temp_min) / (len(temp_max) + len(temp_min))
            if temp_max and temp_min else 0
        )
        total_rainfall = sum(rainfall) if rainfall else 0
        avg_humidity = sum(humidity) / len(humidity) if humidity else 0

        return {
            "season": season,
            "avg_temp": round(avg_temp, 2),
            "total_rainfall": round(total_rainfall, 2),
            "avg_humidity": round(avg_humidity, 2)
        }

    except requests.exceptions.RequestException:
        return {
            "season": season,
            "avg_temp": 27,
            "total_rainfall": 3100,
            "avg_humidity": 73
        }
    except Exception:
        return {
            "season": season,
            "avg_temp": 27,
            "total_rainfall": 3100,
            "avg_humidity": 73
        }


# ----- Main Program -----
if __name__ == "__main__":
    pincode = input("Enter pincode: ").strip()
    season = input("Enter season (kharif/rabi/summer): ").strip().lower()
    budget = float(input("Enter your budget (in ₹): "))

    lat_lon = geocode_nominatim(pincode)
    if lat_lon is None:
        print("Invalid pincode or geocoding failed.")
    else:
        soil_type = get_soil(pincode)
        weather_summary = get_weather(lat_lon, season)

        print(f"\n📍 Location (lat, lon): {lat_lon}")
        print(f"🌱 Soil Type: {soil_type}")
        print(f"🗓 Estimated Seasonal Weather: {weather_summary}")
        suggestions = get_crop_suggestions(soil_type, season, weather_summary, budget)
        print("\n🌾 Crop Recommendations Completed")