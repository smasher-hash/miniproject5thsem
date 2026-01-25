from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app1 = Flask(__name__)
CORS(app1)
@app1.route('/api/mandi')
def get_mandi():
    crop = request.args.get('crop', '').strip().lower()
    district = request.args.get('district', '').strip().lower()

    conn = sqlite3.connect('pests.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = "SELECT * FROM mandi_rates WHERE 1=1"
    params = []
    if crop:
        query += " AND LOWER(commodity) LIKE ?"
        params.append(f"%{crop}%")
    if district:
        query += " AND LOWER(district) LIKE ?"
        params.append(f"%{district}%")

    rows = cur.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

