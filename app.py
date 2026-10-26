from flask import Flask, request, jsonify, render_template, send_from_directory  # type: ignore[import-not-found]

app = Flask(__name__)

from diseaseModule import disease_bp

app.register_blueprint(disease_bp, url_prefix="/disease")

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# Sample crop advisory data 
crop_data = {
    "wheat": {
        "soil": "Loamy soil with good drainage",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 120:60:40",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Keep soil moist and avoid over-irrigation in the early stage."
    },
    "Paddy": {
        "soil": "Clayey soil with high water retention",
        "season": "Kharif (June - November)",
        "fertilizer": "NPK 100:50:50",
        "climate": "Warm and humid climate; optimum temperature 25–35°C.",
        "rainfall": "100–200 cm, standing water is beneficial.",
        "irrigation": "Frequent irrigation to maintain water levels.",
        "advice": "Maintain standing water and use pest control regularly."
    },
    "maize": {
        "soil": "Well-drained fertile soil",
        "season": "Kharif (June - September)",
        "fertilizer": "NPK 150:75:50",
        "climate": "Warm and humid climate; optimum temperature 25–30°C.",
        "rainfall": "50–100 cm, avoid waterlogging.",
        "irrigation": "3–4 irrigations; first after 15–20 days of sowing.",
        "advice": "Avoid waterlogging and ensure proper sunlight and spacing."
    },
    "cotton": {
        "soil": "Black cotton soil with good drainage",
        "season": "Kharif (June - October)",
        "fertilizer": "NPK 100:50:50",
        "climate": "Warm and humid climate; optimum temperature 25–30°C.",
        "rainfall": "50–100 cm, avoid waterlogging.",
        "irrigation": "3–4 irrigations; first after 15–20 days of sowing.",
        "advice": "Ensure proper irrigation and pest control."
    },
    "sugarcane": {
        "soil": "Loamy soil with good organic content",
        "season": "Planting in February - March",
        "fertilizer": "NPK 200:100:100",
        "climate": "Tropical climate; optimum temperature 20–30°C.",
        "rainfall": "75–100 cm, regular watering is essential.",
        "irrigation": "Frequent irrigation; avoid waterlogging.",
        "advice": "Regular irrigation and weed control are essential."
    },
    "groundnut": {
        "soil": "Sandy loam soil with good drainage",
        "season": "Kharif (June - September)",
        "fertilizer": "NPK 50:25:25",
        "climate": "Warm and humid climate; optimum temperature 25–30°C.",
        "rainfall": "50–100 cm, avoid waterlogging.",
        "irrigation": "3–4 irrigations; first after 15–20 days of sowing.",
        "advice": "Ensure proper spacing and avoid waterlogging."
    },
    "soybean": {
        "soil": "Well-drained loamy soil",
        "season": "Kharif (June - September)",
        "fertilizer": "NPK 60:30:30",
        "climate": "Warm and humid climate; optimum temperature 25–30°C.",
        "rainfall": "50–100 cm, avoid waterlogging.",
        "irrigation": "3–4 irrigations; first after 15–20 days of sowing.",
        "advice": "Maintain soil moisture and use rhizobium inoculant."
    },
    "sunflower": {
        "soil": "Sandy loam soil with good drainage",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 80:40:40",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure full sunlight and avoid waterlogging."
    },
    "potato": {
        "soil": "Well-drained loamy soil",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 150:75:75",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Keep soil moist and avoid over-irrigation."
    },
    "tomato": {
        "soil": "Loamy soil with good organic content",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 100:50:50",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure proper spacing and use fungicides to prevent diseases."
    },
    "onion": {
        "soil": "Sandy loam soil with good drainage",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 80:40:40",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Maintain soil moisture and avoid waterlogging."
    },
    "carrot": {
        "soil": "Sandy loam soil with good drainage",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 70:30:30",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure loose soil for root development and avoid waterlogging."
    },
    "cabbage": {
        "soil": "Loamy soil with good organic content",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 100:50:50",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Maintain soil moisture and use pest control regularly."
    },
    "cauliflower": {
        "soil": "Loamy soil with good organic content",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 100:50:50",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure proper spacing and use fungicides to prevent diseases."
    },
    "brinjal": {
        "soil": "Well-drained loamy soil",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 100:50:50",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Maintain soil moisture and use pest control regularly."
    },
    "chili": {
        "soil": "Well-drained loamy soil",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 80:40:40",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure full sunlight and avoid waterlogging."
    },
    "Barley":{
        "soil": "Well-drained loamy soil",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 90:45:45",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Maintain soil moisture and avoid waterlogging."
    },
    "Jowar":{
        "soil": "Well-drained loamy soil",
        "season": "Kharif (June - September)",
        "fertilizer": "NPK 100:50:50",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure proper spacing and avoid waterlogging."
    },
    "Bajra":{
        "soil": "Sandy loam soil with good drainage",
        "season": "Kharif (June - September)",
        "fertilizer": "NPK 80:40:40",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Maintain soil moisture and avoid waterlogging."
    },
    "Ragi":{
        "soil": "Well-drained loamy soil",
        "season": "Kharif (June - September)",
        "fertilizer": "NPK 70:30:30",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure proper spacing and avoid waterlogging."
    },
    "Mustard":{
        "soil": "Loamy soil with good organic content",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 60:30:30",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Maintain soil moisture and use pest control regularly."
    },
    "Peas":{
        "soil": "Well-drained loamy soil",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 50:25:25",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure proper spacing and avoid waterlogging."
    },
    "Grams":{
        "soil": "Sandy loam soil with good drainage",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 60:30:30",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Maintain soil moisture and use rhizobium inoculant."
    },
    "cucumber":{
        "soil": "Well-drained loamy soil",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 80:40:40",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure full sunlight and avoid waterlogging."
    },
    "watermelon":{
        "soil": "Sandy loam soil with good drainage",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 70:30:30",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Maintain soil moisture and avoid waterlogging."
    },
    "pumpkin":{
        "soil": "Well-drained loamy soil",
        "season": "Rabi (October - March)",
        "fertilizer": "NPK 80:40:40",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure proper spacing and avoid waterlogging."
    },
    "Moong":{
        "soil": "Sandy loam soil with good drainage",
        "season": "Kharif (June - September)",
        "fertilizer": "NPK 50:25:25",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Maintain soil moisture and use rhizobium inoculant."
    },
    "Urad":{
        "soil": "Well-drained loamy soil",
        "season": "Kharif (June - September)",
        "fertilizer": "NPK 60:30:30",
        "climate": "Cool and dry climate; optimum temperature 10–25°C.",
        "rainfall": "30–100 cm, avoid heavy rains during growth.",
        "irrigation": "5–6 irrigations; first after 20–25 days of sowing.",
        "advice": "Ensure proper spacing and avoid waterlogging."
    },
}


# @app.route('/')
# def home():
#     return "🌾Smart Krishi Portal Crop Advisory System Running"


from chatbotModule import chatbot_bp

app.register_blueprint(chatbot_bp)

@app.route("/")
def home():
    return send_from_directory(
        app.root_path,
        "index.html"
    )

@app.route('/advice', methods=['GET'])
def get_crop_advice():
    crop = request.args.get('crop', '').lower()
    if crop in crop_data:
        return jsonify({
            "Crop": crop.capitalize(),
            "Soil Type": crop_data[crop]["soil"],
            "Season": crop_data[crop]["season"],
            "Fertilizer": crop_data[crop]["fertilizer"],
            "Advisory": crop_data[crop]["advice"]
        })
    else:
        return jsonify({"Error": "Crop not found"}), 404

# Cache mandi data for reuse when the external API is unavailable.
CACHE = {
    "mandi_data": None,
    "timestamp": None
}

DATA_API_URL = "https://data.gov.in/api/avat?xyz=..."
# Replace the placeholder above with the actual data.gov.in resource endpoint.

from urllib.parse import urlencode
from urllib.request import urlopen
import json


def fetch_json(url, params=None, timeout=10):
    """Fetch and decode JSON using the Python standard library."""
    if params:
        url = f"{url}?{urlencode(params)}"
    with urlopen(url, timeout=timeout) as response:
        return json.load(response)


def fetch_mandi_data_from_api():
    """Fetch mandi data from the external API and return a list or records."""
    data = fetch_json(DATA_API_URL, {"format": "json"})
    records = data.get("records") or data.get("data") or data
    return records


@app.route('/mandi')
def mandi():
    return render_template('mandi.html')


@app.route('/api/mandi')
def get_mandi():
    crop = request.args.get("crop", "").lower()
    district = request.args.get("district", "").lower()

    try:
        mandi_list = fetch_mandi_data_from_api()
        CACHE["mandi_data"] = mandi_list
    except Exception:
        mandi_list = CACHE.get("mandi_data") or []

    filtered = []
    for item in mandi_list:
        comm = item.get("commodity", "")
        dist = item.get("district", "")
        if ((not crop or crop in comm.lower()) and
                (not district or district in dist.lower())):
            filtered.append(item)

    return jsonify(filtered)


API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    return fetch_json(BASE_URL, params)


def generate_weather_alert(data):
    alerts = []

    if "main" not in data:
        return ["Weather data unavailable"]

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["main"].lower()
    wind_speed = data["wind"]["speed"]

    if temp > 40:
        alerts.append("🔥 Heatwave Alert: Stay hydrated and avoid outdoor activities.")
    elif temp < 5:
        alerts.append("❄️ Cold Alert: Keep warm, risk of frost.")

    if "rain" in weather or "thunderstorm" in weather:
        alerts.append("🌧️ Rain/Storm Alert: Carry an umbrella, possible flooding in low areas.")

    if wind_speed > 25:
        alerts.append("💨 High Wind Alert: Secure loose objects and avoid open areas.")

    if humidity > 90:
        alerts.append("💧 High Humidity Alert: Discomfort may be high, stay hydrated.")

    if not alerts:
        alerts.append("✅ Weather conditions are normal.")

    return alerts


@app.route('/api/weather')
def weather():
    city = request.args.get("city", "Delhi")
    data = get_weather(city)
    alerts = generate_weather_alert(data)

    return jsonify({
        "city": city,
        "temperature": data.get("main", {}).get("temp"),
        "humidity": data.get("main", {}).get("humidity"),
        "condition": data["weather"][0]["description"] if "weather" in data else "N/A",
        "alerts": alerts
    })


if __name__ == '__main__':
    app.run(debug=True)
