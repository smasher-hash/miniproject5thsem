from flask import Flask, render_template, request, jsonify

mandi = Flask(__name__)

# --- Sample Mandi Data (you can later connect to DB or API) ---
mandi_data = [
    {"crop": "Wheat", "price": "₹2200 / Quintal", "location": "Kanpur", "date": "2025-10-12"},
    {"crop": "Rice", "price": "₹2500 / Quintal", "location": "Lucknow", "date": "2025-10-12"},
    {"crop": "Maize", "price": "₹1800 / Quintal", "location": "Varanasi", "date": "2025-10-12"},
    {"crop": "Sugarcane", "price": "₹320 / Quintal", "location": "Bareilly", "date": "2025-10-12"},
    {"crop": "Pulses", "price": "₹7200 / Quintal", "location": "Gorakhpur", "date": "2025-10-12"},
]

@mandi.route("/mandi")
def home():
    return render_template("mandi.html")

@mandi.route("/search", methods=["POST"])
def search_crop():
    crop_name = request.json.get("crop", "").strip().lower()
    result = [item for item in mandi_data if item["crop"].lower() == crop_name]

    if result:
        return jsonify({"status": "success", "data": result})
    else:
        return jsonify({"status": "not_found", "message": "No data found for this crop."})

if __name__ == "_main_":
    mandi.run(debug=True)

    from flask import Flask, jsonify, request, render_template
import requests
import datetime
from bs4 import BeautifulSoup  # if using scraping fallback

mandi = Flask(__name__)

# Example endpoint URL(s) — adjust based on real API/scraping source
DATA_API_URL = "https://data.gov.in/resource/XXXXXXXX"  # replace with actual resource endpoint
CEDA_API_URL = "https://agmarknet.ceda.ashoka.edu.in/api/marketdata"  # example

def fetch_today_data():
    """Fetch current day's mandi data via API (Data.gov.in or CEDA)."""
    params = {"format": "json"}
    try:
        resp = requests.get(DATA_API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # The structure may have `records` or `data` etc.
        return data.get("records", data)
    except Exception as e:
        print("Failed fetch today:", e)
        return []

def fetch_yesterday_data():
    """Fetch previous day's data — either via API (filter by date) or fallback scrape."""
    # Option 1: If API supports date filter, use it
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    params = {"date": yesterday, "format": "json"}
    try:
        resp = requests.get(DATA_API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("records", data)
    except Exception as e:
        print("API date filter failed:", e)
    # Fallback: scrape from Agmarknet’s “Datewise Commodity Report”
    return scrape_yesterday_from_agmarknet(yesterday)

def scrape_yesterday_from_agmarknet(date_str):
    # Simple scraping of HTML page for datewise report
    url = "https://www.agmarknet.gov.in/PriceAndArrivals/DatewiseCommodityReport.aspx"
    params = {
        "DateFrom": date_str,
        "DateTo": date_str,
        # other query parameters may be needed: commodity, state, etc.
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table", {"id": "GVCGrid"})  # example table id (inspect real page)
        rows = table.find_all("tr")[1:]  # skip header
        result = []
        for r in rows:
            cols = [c.get_text(strip=True) for c in r.find_all("td")]
            # You’ll need to map columns to your fields
            # Example: [ State, District, Market, Commodity, Variety, Min, Max, Modal, Date ]
            if len(cols) >= 9:
                rec = {
                    "state": cols[0],
                    "district": cols[1],
                    "market": cols[2],
                    "commodity": cols[3],
                    "variety": cols[4],
                    "min_price": float(cols[5]) if cols[5] else None,
                    "max_price": float(cols[6]) if cols[6] else None,
                    "modal_price": float(cols[7]) if cols[7] else None,
                    "date": cols[8]
                }
                result.append(rec)
        return result
    except Exception as e:
        print("Scraping failed:", e)
        return []

@mandi.route('/')
def home():
    return render_template('mandi_compare.html')

@mandi.route('/api/mandi_compare')
def mandi_compare():
    # fetch both days
    today_data = fetch_today_data()
    yesterday_data = fetch_yesterday_data()

    # index by key (state + market + commodity) for matching
    def make_key(item):
        return f"{item.get('state','')}|{item.get('market','')}|{item.get('commodity','')}|{item.get('variety','')}"

    y_map = { make_key(item): item for item in yesterday_data }
    combined = []

    for t in today_data:
        key = make_key(t)
        y = y_map.get(key)
        combined.append({
            "today": t,
            "yesterday": y
        })

    return jsonify(combined)

if __name__ == '__main__':
    mandi.run(debug=True)
