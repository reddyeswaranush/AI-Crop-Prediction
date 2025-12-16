# AI-Crop-Prediction

AI-Crop-Prediction is a lightweight Python utility that suggests suitable crops for a farmer based on pincode (location), season, soil type, seasonal weather summary (fetched from Open-Meteo archive), and budget. It uses OpenStreetMap Nominatim for geocoding and can call a generative model (Google Gemini via `google.generativeai`) to produce structured crop recommendations.

**Key Features**
- Geocodes a pincode to latitude/longitude using Nominatim.
- Maps Kerala pincodes to a basic soil-type lookup.
- Fetches seasonal weather summaries from Open-Meteo archive API.
- Produces structured crop recommendations via a configured generative model and saves them to `crop_suggestions.txt`.

**Requirements**
- Python 3.10+
- The following Python packages:
  - `requests`
  - `google-generativeai` (or `google.generativeai` as the installed package)

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install requests google-generativeai
```

**Configuration & Security**
- The script expects a Google API key for the generative model. Do NOT commit real API keys into source files. Instead set an environment variable and update the script to read from it. Example:

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

Then update the script to read `os.environ["GOOGLE_API_KEY"]` (the provided example currently uses an inline key which should be removed).

**How to Run**
1. Save the provided Python script (example name: `crop_recommender.py`) in the repository root.
2. Ensure dependencies are installed and `GOOGLE_API_KEY` is set if you plan to call the generative model.
3. Run the script:

```bash
python crop_recommender.py
```

The script will prompt for:
- `pincode` — Indian postal code (the repo contains a Kerala pincode -> soil map for many pincodes)
- `season` — one of `kharif`, `rabi`, or `summer`
- `budget` — numeric budget in INR

Outputs:
- Console output with location, soil type, and estimated seasonal weather.
- A file named `crop_suggestions.txt` containing the generated crop recommendations in the structured format requested from the model.

**APIs Used / Notes**
- Nominatim (OpenStreetMap) is used for geocoding. Respect its usage policy and rate limits; for production use consider a paid geocoding service.
- Open-Meteo Archive API is used for historical/seasonal weather aggregation.
- The generative model call uses `google.generativeai`. Ensure your credentials and billing are appropriately configured.

**Sample Interaction**

```
Enter pincode: 671121
Enter season (kharif/rabi/summer): kharif
Enter your budget (in ₹): 20000

📍 Location (lat, lon): [11.87, 75.35]
🌱 Soil Type: Laterite Soil
🗓 Estimated Seasonal Weather: {'season': 'kharif', 'avg_temp': 27.12, 'total_rainfall': 1520.0, 'avg_humidity': 78.5}

Crop recommendations saved to crop_suggestions.txt
```

**Troubleshooting**
- If geocoding fails, verify internet connectivity and that Nominatim is reachable.
- If Open-Meteo returns empty data, the script falls back to conservative default values.
- If the generative model call fails, check `GOOGLE_API_KEY`, network access, and package compatibility.

**Contributing**
- Improvements welcome. Suggested enhancements: expand pincode->soil mapping, add validation for user inputs, cache API results, or swap Nominatim with a rate-limited geocoding provider.

**License & Credits**
- This repository is provided as-is. Include your preferred license if you want to open-source it (e.g., MIT).

---
If you want, I can:
- Add a small CLI wrapper with argument parsing.
- Refactor the script to read configuration from environment or a config file.
- Add unit tests for the helper functions.

Let me know which you'd like next.