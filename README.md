# 🌾 AI Crop Prediction System

An intelligent crop recommendation system that combines real-time weather data,
soil analysis, and Gemini AI to suggest the most suitable crops for a given location.

## Features

- 📍 Pincode-based location detection (India Post API + Nominatim)
- 🌦️ Real-time weather data via Open-Meteo Archive API
- 🌱 Soil type mapping for Kerala regions
- 🤖 AI-powered crop recommendations using Google Gemini
- 💰 Budget-aware suggestions with cost, market price & profit range

## Tech Stack

- **Frontend:** Streamlit
- **AI:** Google Gemini API (`gemini-1.5-flash`)
- **Weather:** Open-Meteo Archive API
- **Geocoding:** India Post API + Nominatim (OpenStreetMap)
- **Language:** Python

## Setup

1. Clone the repo
```bash
   git clone https://github.com/yourusername/ai-crop-prediction.git
   cd ai-crop-prediction
```

2. Install dependencies
```bash
   pip install streamlit requests google-genai
```

3. Add your Gemini API key to `.streamlit/secrets.toml`
```toml
   GOOGLE_API_KEY = "your_api_key_here"
```

4. Run the app
```bash
   streamlit run app.py
```

## How It Works

1. User enters a pincode, season, and budget
2. India Post API resolves pincode → district/state
3. Nominatim geocodes district → lat/lon coordinates
4. Open-Meteo fetches historical weather for the season
5. Gemini AI generates 5 crop recommendations with cost & profit analysis

## APIs Used

| API | Purpose |
|-----|---------|
| Google Gemini | Crop recommendations |
| Open-Meteo Archive | Historical weather data |
| India Post API | Pincode resolution |
| Nominatim (OSM) | Geocoding |
