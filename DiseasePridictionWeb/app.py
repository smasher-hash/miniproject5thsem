from flask import Flask, render_template, request, send_from_directory  # pyright: ignore[reportMissingImports]
import tensorflow as tf  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
import numpy as np  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
from PIL import Image  # pyright: ignore[reportMissingImports]
import os

app = Flask(__name__)

# ==============================
# MODEL
# ==============================

MODEL_PATH = "models/fine_tuned_model.keras"

print("Loading disease prediction model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully!")


# ==============================
# DISEASE CLASSES
# ==============================

class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",

    "Blueberry___healthy",

    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",

    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",

    "Orange___Haunglongbing_(Citrus_greening)",

    "Peach___Bacterial_spot",
    "Peach___healthy",

    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",

    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",

    "Raspberry___healthy",

    "Soybean___healthy",

    "Squash___Powdery_mildew",

    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",

    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]


# ==============================
# UPLOAD FOLDER
# ==============================

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ==============================
# # HOME PAGE
# # ==============================

# @app.route("/")
# def home():
#     return render_template("disease.html")


# # ==============================
# # PREDICTION
# # ==============================

# @app.route("/predict", methods=["POST"])
# def predict():

# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():
    return render_template("disease.html")


# ==============================
# SERVE UPLOADED IMAGES
# ==============================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ==============================
# PREDICTION
# ==============================

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return render_template(
            "disease.html",
            error="Please upload an image."
        )

    file = request.files["image"]

    if file.filename == "":
        return render_template(
            "disease.html",
            error="Please select an image."
        )

    try:

        # Save uploaded image
        image_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(image_path)

        # Open image
        img = Image.open(image_path).convert("RGB")

        # Resize according to model
        img = img.resize((224, 224))

        # Convert image to array
        img_array = np.array(img)

        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        # IMPORTANT:
        # Do NOT use MobileNetV2 preprocess_input here.
        # The trained model already handles preprocessing.

        predictions = model.predict(img_array)

        predicted_index = np.argmax(predictions[0])

        predicted_class = class_names[predicted_index]

        confidence = float(
            predictions[0][predicted_index] * 100
        )

        # Format disease name
        disease_name = predicted_class.replace(
            "___", " - "
        ).replace("_", " ")

        return render_template(
            "disease.html",
            prediction=disease_name,
            confidence=round(confidence, 2),
            image_path="/" + image_path.replace("\\", "/")
        )

    except Exception as e:

        print("Prediction Error:", e)

        return render_template(
            "disease.html",
            error="Unable to process the image. Please try another image."
        )


# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5001
    )