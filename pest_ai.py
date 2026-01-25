from flask import Blueprint, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os, sqlite3, json
from werkzeug.utils import secure_filename

ai_bp = Blueprint('pest_ai', __name__)
UPLOAD_FOLDER = 'static/uploads/'
MODEL_PATH = 'model/pest_model.h5'
PESTICIDE_FILE = 'static/data/pesticides.json'

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Load pesticide data
with open(PESTICIDE_FILE) as f:
    pesticide_data = json.load(f)

def get_pesticide_info(disease_name):
    for item in pesticide_data:
        if item["disease"].lower() == disease_name.lower():
            return item
    return {"pesticide": "No data", "dosage": "-", "safety": "-"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg','jpeg','png'}

def save_to_db(farmer_name, image_path, prediction, confidence):
    conn = sqlite3.connect('data/krishi.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO detections (farmer_name, image_path, prediction, confidence)
        VALUES (?, ?, ?, ?)
    ''', (farmer_name, image_path, prediction, confidence))
    conn.commit()
    conn.close()

@ai_bp.route('/pest_ai')
def pest_ai_page():
    return render_template('pest_ai.html')

@ai_bp.route('/pest_ai/detect', methods=['POST'])
def detect_disease():
    if 'image' not in request.files:
        return jsonify({'error':'No image uploaded'})

    file = request.files['image']
    farmer_name = request.form.get('farmer_name', 'Unknown Farmer')

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error':'Invalid file type'})

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Image preprocessing
    img = image.load_img(file_path, target_size=(128,128))
    img_array = np.expand_dims(image.img_to_array(img)/255.0, axis=0)
    preds = model.predict(img_array)
    classes = ['Healthy','Rust','Blight','Leaf Curl','Brown Spot']
    predicted_class = classes[np.argmax(preds)]
    confidence = round(float(np.max(preds))*100,2)

    pesticide_info = get_pesticide_info(predicted_class)

    save_to_db(farmer_name, file_path, predicted_class, confidence)

    return jsonify({
        'prediction': predicted_class,
        'confidence': confidence,
        'image_url': file_path,
        'pesticide': pesticide_info['pesticide'],
        'dosage': pesticide_info['dosage'],
        'safety': pesticide_info['safety']
    })

@ai_bp.route('/pest_ai/history')
def pest_history():
    conn = sqlite3.connect('data/krishi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM detections ORDER BY date DESC")
    history = cursor.fetchall()
    conn.close()
    return render_template('pest_history.html', history=history)
