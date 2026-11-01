import os

from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for  # type: ignore[import-not-found]


from pymongo import MongoClient  # type: ignore[import-not-found]
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore[import-not-found]
def load_dotenv():
    """Load simple KEY=VALUE entries from a local .env file without a dependency."""
    try:
        with open(".env", encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip("\"'")
                if key:
                    os.environ.setdefault(key, value)
    except FileNotFoundError:
        pass

app = Flask(__name__)

load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY is missing from .env")

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

client = MongoClient(os.getenv("MONGO_URI"))
db = client["KrishiMitra_AI"]
users_collection = db["users"]

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
 "paddy": {
    "soil": "Clayey loam or loamy soil with good water retention and drainage.",

    "season": "Kharif (June - November); also grown in Rabi and summer seasons in suitable regions.",

    "climate": "Warm and humid climate. Optimum temperature is approximately 20–35°C with adequate sunlight.",

    "rainfall": "Approximately 100–200 cm annually. Requires sufficient water during the growing season.",

    "fertilizer": "Apply balanced NPK fertilizer based on soil testing. Nitrogen is generally applied in split doses.",

    "irrigation": "Maintain adequate soil moisture. Transplanted rice generally requires shallow standing water during important growth stages. Drain fields before harvesting.",

    "recommendation": "Use healthy certified seeds, prepare a level field, maintain proper plant spacing, control weeds, monitor pests and diseases, and avoid excessive water wastage."
},
    "wheat": {
    "soil": "Loamy soil with good drainage",
    "season": "Rabi (October - March)",
    "fertilizer": "NPK 120:60:40",
    "climate": "Cool and dry climate; optimum temperature 10–25°C.",
    "rainfall": "30–100 cm, avoid heavy rains during growth.",
    "irrigation": "Irrigate at important growth stages.",
    "recommendation": "Keep soil moist and avoid over-irrigation in the early stage."
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

# =====================================
# USER AUTHENTICATION - MONGODB
# =====================================

@app.route("/login", methods=["GET"])
def login_page():
    return send_from_directory(app.root_path, "login.html")


@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 8 characters."
        }), 400

    if users_collection.find_one({"email": email}):
        return jsonify({
            "success": False,
            "message": "This email is already registered."
        }), 409

    hashed_password = generate_password_hash(password)

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    session.clear()
    session["user_email"] = email
    session["user_name"] = name

    return jsonify({
        "success": True,
        "message": "Registration successful!",
        "redirect": "/dashboard"
    }), 201


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Please enter email and password."
        }), 400

    user = users_collection.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    session.clear()
    session["user_email"] = user["email"]
    session["user_name"] = user["name"]

    return jsonify({
        "success": True,
        "message": "Login successful!",
        "redirect": "/dashboard"
    })




@app.route("/dashboard")
def dashboard():

    if "user_email" not in session:
        return redirect("/login")

    return send_from_directory(
        app.root_path,
        "dashboard.html"
    )


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")



@app.route("/login.css")
def login_css():
    return send_from_directory(app.root_path, "login.css")


@app.route("/login.js")
def login_js():
    return send_from_directory(app.root_path, "login.js")



@app.route("/")
def home():
    return send_from_directory(
        app.root_path,
        "index.html"
    )

@app.route('/advice', methods=['GET'])
def get_crop_advice():

    crop = request.args.get('crop', '').strip().lower()

    if crop not in crop_data:
        return jsonify({
            "Error": "Crop not found"
        }), 404

    data = crop_data[crop]

    return jsonify({
        "Crop": crop.capitalize(),

        "Soil Type": data.get("soil", "Information not available."),

        "Season": data.get("season", "Information not available."),

        "Climate": data.get("climate", "Information not available."),

        "Rainfall": data.get("rainfall", "Information not available."),

        "Fertilizer": data.get("fertilizer", "Information not available."),

        "Irrigation": data.get("irrigation", "Information not available."),

        "Advisory": (
            data.get("recommendation")
            or data.get("advice")
            or data.get("advisory")
            or "Information not available."
        )
    })

# Cache mandi data for reuse when the external API is unavailable.
CACHE = {
    "mandi_data": None,
    "timestamp": None
}

import time

MANDI_CACHE = {
    "data": None,
    "timestamp": 0
}

MANDI_CACHE_DURATION = 600  # 10 minutes

 
# ==========================================
# LIVE MANDI PRICE API - DATA.GOV.IN
# ==========================================

import os
import json
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

CACHE = {
    "mandi_data": None,
    "timestamp": None
}

DATA_API_URL = (
    "https://api.data.gov.in/resource/"
    "9ef84268-d588-465a-a308-a864a43d0070"
)

# Set DATA_GOV_API_KEY in your environment variables.
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY", "").strip()


def fetch_json(url, params=None, timeout=60):
    if params:
        url = f"{url}?{urlencode(params)}"

    req = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_mandi_data_from_api(crop="", district="", state=""):
    """Fetch live mandi prices from data.gov.in."""

    if not DATA_GOV_API_KEY:
        raise ValueError("DATA_GOV_API_KEY is not configured.")

    params = {
        "api-key": DATA_GOV_API_KEY,
        "format": "json",
        "limit": 20
    }

    if crop:
        params["filters[commodity]"] = crop

    if district:
        params["filters[district]"] = district

    if state:
        params["filters[state]"] = state
        # Temporary debugging statements
    print("API key loaded:", bool(DATA_GOV_API_KEY))
    print("API key length:", len(DATA_GOV_API_KEY))
    print("Request parameters:", {
        "format": params.get("format"),
        "limit": params.get("limit"),
        "api_key_present": bool(params.get("api-key"))
    })


    data = fetch_json(DATA_API_URL, params)

    if data.get("status") != "ok":
        raise ValueError(data.get("message", "Invalid API response"))

    return data.get("records", [])


@app.route("/mandi")
def mandi():
    return render_template("mandi.html")


@app.route("/api/mandi", methods=["GET"])
def get_mandi():

    crop = request.args.get("crop", "").strip()
    district = request.args.get("district", "").strip()
    state = request.args.get("state", "").strip()

    cache_key = (crop.lower(), district.lower(), state.lower())
    now = time.time()

    cached = MANDI_CACHE.get(cache_key)

    if cached and now - cached["timestamp"] < MANDI_CACHE_DURATION:
        return jsonify({
            "success": True,
            "source": "Cached data.gov.in - AGMARKNET",
            "count": len(cached["data"]),
            "records": cached["data"],
            "cached": True
        })

    try:
        mandi_list = fetch_mandi_data_from_api(
            crop=crop,
            district=district,
            state=state
        )

        MANDI_CACHE[cache_key] = {
            "data": mandi_list,
            "timestamp": now
        }

        return jsonify({
            "success": True,
            "source": "data.gov.in - AGMARKNET",
            "count": len(mandi_list),
            "records": mandi_list,
            "cached": False
        })

    except Exception as e:
        print("Mandi API Error:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 502


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

@app.route('/pest-disease-guide')
def pest_disease_guide():
    return render_template('pests.html')

# Pest and disease entries used by the pest-disease API, keyed by lowercase crop.
pest_disease_data = {
    "paddy": [
        {"category": "pest", "name": "Rice stem borer", "symptoms": "Dead hearts in young plants or whiteheads in mature plants.", "management": "Monitor fields, remove affected stems, and use locally recommended integrated pest management."},
        {"category": "disease", "name": "Rice blast", "symptoms": "Spindle-shaped lesions on leaves and dark lesions on stems.", "management": "Use resistant varieties, avoid excess nitrogen, and follow local disease-control guidance."},
    ],
    "wheat": [
        {"category": "pest", "name": "Aphids", "symptoms": "Clusters of small insects on leaves and ears, often with yellowing.", "management": "Monitor crops and conserve beneficial insects; follow local integrated pest management guidance."},
        {"category": "disease", "name": "Wheat rust", "symptoms": "Orange, brown, or black pustules on leaves and stems.", "management": "Grow resistant varieties and follow local recommendations for disease management."},
    ],
    "maize": [
        {"category": "pest", "name": "Fall armyworm", "symptoms": "Ragged leaf damage and masses of frass in the whorl.", "management": "Scout plants regularly and use locally recommended integrated pest management."},
        {"category": "disease", "name": "Turcicum leaf blight", "symptoms": "Long, cigar-shaped gray-green lesions on leaves.", "management": "Use resistant varieties and rotate crops where practical."},
    ],
    "cotton": [
        {"category": "pest", "name": "Cotton bollworm", "symptoms": "Feeding holes in squares, flowers, and bolls.", "management": "Scout regularly and follow local integrated pest management recommendations."},
        {"category": "disease", "name": "Cotton bacterial blight", "symptoms": "Angular leaf spots that may darken and cause leaf shedding.", "management": "Use healthy seed and resistant varieties, and avoid moving infected crop residue."},
    ],
    "tomato": [
        {"category": "pest", "name": "Whitefly", "symptoms": "Small white insects under leaves, leaf yellowing, and sticky honeydew.", "management": "Monitor plants and use locally recommended integrated pest management."},
        {"category": "disease", "name": "Early blight", "symptoms": "Dark leaf spots with concentric rings, often on older leaves.", "management": "Remove affected leaves, avoid overhead watering, and rotate crops."},
    ],
    "potato": [
        {"category": "pest", "name": "Potato tuber moth", "symptoms": "Larval tunnels in leaves or tubers, especially in exposed tubers.", "management": "Earth up plants, protect harvested tubers from light, and follow local guidance."},
        {"category": "disease", "name": "Late blight", "symptoms": "Water-soaked leaf patches that rapidly turn brown, sometimes with white growth underneath.", "management": "Use healthy seed tubers, remove infected plants, and follow local disease-control guidance."},
    ],
    "sugarcane": [
    {
        "name": "Sugarcane Early Shoot Borer",
        "category": "pest",
        "crop": "Sugarcane",
        "symptoms": "Dead hearts in young shoots, holes near the shoot base and drying of central leaves.",
        "causes": "Damage caused by early shoot borer larvae.",
        "prevention": "Use healthy planting material, remove affected shoots and maintain field sanitation.",
        "organic_management": "Use suitable biological control methods and monitor the crop regularly.",
        "management": "Follow locally recommended integrated pest management practices."
    },
    {
        "name": "Sugarcane Red Rot",
        "category": "disease",
        "crop": "Sugarcane",
        "symptoms": "Yellowing and drying of leaves; internal stalk tissue may show red discoloration with white patches.",
        "causes": "Fungal infection caused by Colletotrichum falcatum.",
        "prevention": "Use disease-free setts, resistant varieties and remove infected clumps.",
        "organic_management": "Maintain field sanitation and avoid using infected planting material.",
        "management": "Remove infected plants and consult local agricultural experts for suitable control."
    }
],
}

@app.route('/api/pest-disease', methods=['GET'])
def get_pest_disease():
    crop = request.args.get('crop', '').strip().lower()
    problem_type = request.args.get('type', '').strip().lower()

    if crop not in pest_disease_data:
        return jsonify({"Error": "Crop information not found"}), 404

    if problem_type not in ['pest', 'disease', 'both']:
        return jsonify({"Error": "Invalid problem type"}), 400

    items = pest_disease_data[crop]

    if problem_type != 'both':
        items = [item for item in items if item['category'] == problem_type]

    return jsonify({
        "crop": crop.capitalize(),
        "type": problem_type,
        "items": items
    })

if __name__ == '__main__':
    app.run(debug=True)
