
from pathlib import Path
from uuid import uuid4

import numpy as np  # pyright: ignore[reportMissingImports]
import tensorflow as tf  # pyright: ignore[reportMissingModuleSource]
from PIL import Image, UnidentifiedImageError  # pyright: ignore[reportMissingImports]
from flask import (  # pyright: ignore[reportMissingImports]
    Blueprint,
    current_app,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename  # pyright: ignore[reportMissingImports]


# Paths to the existing disease detection project
MODULE_DIR = Path(__file__).resolve().parent / "DiseasePridictionWeb"
MODEL_PATH = MODULE_DIR / "models" / "fine_tuned_model.keras"
UPLOAD_FOLDER = MODULE_DIR / "uploads"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Separate disease detection module
disease_bp = Blueprint(
    "disease",
    __name__,
    template_folder=str(MODULE_DIR / "templates"),
    static_folder=str(MODULE_DIR / "static"),
    static_url_path="/disease-static",
)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Keep the exact 38 class names from your original disease app.py.
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
    "Tomato___healthy",
]

print("Loading KrishiMitra disease detection model...")

model = tf.keras.models.load_model(str(MODEL_PATH))

print("Disease detection model loaded successfully!")


@disease_bp.route("/")
def home():
    return render_template("disease.html")


# @disease_bp.route("/uploads/<filename>")
# def uploaded_file(filename):
#     return current_app.send_static_file("nonexistent") if False else __import__(
#         "flask"
#     ).send_from_directory(str(UPLOAD_FOLDER), filename)

@disease_bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(str(UPLOAD_FOLDER), filename)


@disease_bp.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return render_template(
            "disease.html", error="Please upload an image."
        )

    file = request.files["image"]

    if not file.filename:
        return render_template(
            "disease.html", error="Please select an image."
        )

    original_name = secure_filename(file.filename)
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return render_template(
            "disease.html",
            error="Please upload a JPG, JPEG, or PNG image.",
        )

    # Unique filenames prevent collisions and unsafe file paths.
    filename = f"{uuid4().hex}{extension}"
    image_path = UPLOAD_FOLDER / filename

    try:
        file.save(str(image_path))

        with Image.open(image_path) as source:
            img = source.convert("RGB").resize((224, 224))
            img_array = np.asarray(img, dtype=np.float32)

        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array, verbose=0)

        if (
            predictions.ndim != 2
            or predictions.shape[0] != 1
            or predictions.shape[1] != len(class_names)
        ):
            raise ValueError("Model output does not match disease classes.")

        predicted_index = int(np.argmax(predictions[0]))
        predicted_class = class_names[predicted_index]

        confidence = float(predictions[0][predicted_index] * 100)

        disease_name = predicted_class.replace(
            "___", " - "
        ).replace("_", " ")

        return render_template(
            "disease.html",
            prediction=disease_name,
            confidence=round(confidence, 2),
            image_path=url_for(
                "disease.uploaded_file", filename=filename
            ),
        )

    except (UnidentifiedImageError, OSError):
        return render_template(
            "disease.html",
            error="Unable to read this image. Please try another image.",
        )

    except Exception:
        current_app.logger.exception("Disease prediction failed")
        return render_template(
            "disease.html",
            error="Prediction failed. Please check the server terminal.",
        )
