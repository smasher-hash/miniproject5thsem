from flask import Blueprint, Flask, render_template, request, send_from_directory, url_for  # pyright: ignore[reportMissingImports]
from werkzeug.utils import secure_filename  # pyright: ignore[reportMissingImports]
import tensorflow as tf  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
import numpy as np  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
from PIL import Image  # pyright: ignore[reportMissingImports]
import os
import uuid

app = Flask(__name__)
  
 

# Disease detection blueprint
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

disease_bp = Blueprint(
    "disease",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ==============================
# MODEL
# ==============================
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "fine_tuned_model.keras"
)
# MODEL_PATH = "models/fine_tuned_model.keras"

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


# ==========================================
# DISEASE-SPECIFIC GUIDANCE (38 CLASSES)
# ==========================================

disease_guidance = {

    "Apple___Apple_scab": [
        "Remove fallen infected leaves to reduce disease spread.",
        "Prune crowded branches to improve air circulation.",
        "Monitor new leaves and fruits for olive-green or dark lesions.",
        "Follow locally recommended apple scab management practices."
    ],

    "Apple___Black_rot": [
        "Remove mummified fruits and infected plant material.",
        "Prune diseased branches where appropriate.",
        "Maintain orchard sanitation.",
        "Monitor fruits and leaves for expanding dark lesions."
    ],

    "Apple___Cedar_apple_rust": [
        "Inspect leaves for orange or yellow spots.",
        "Remove nearby infected alternate-host junipers where appropriate and permitted.",
        "Maintain good orchard sanitation.",
        "Seek local guidance for rust management."
    ],

    "Apple___healthy": [
        "Your apple leaf appears healthy.",
        "Maintain balanced irrigation and nutrition.",
        "Prune trees appropriately for good air circulation.",
        "Inspect leaves and fruits regularly."
    ],

    "Blueberry___healthy": [
        "Your blueberry leaf appears healthy.",
        "Maintain suitable soil moisture and acidity.",
        "Avoid waterlogging around plant roots.",
        "Monitor plants regularly for unusual leaf symptoms."
    ],

    "Cherry_(including_sour)___Powdery_mildew": [
        "Remove severely infected plant parts where appropriate.",
        "Improve air circulation through proper pruning.",
        "Avoid excessive nitrogen fertilizer.",
        "Monitor new leaves for white powdery fungal growth."
    ],

    "Cherry_(including_sour)___healthy": [
        "Your cherry leaf appears healthy.",
        "Maintain proper watering practices.",
        "Prune crowded branches to improve airflow.",
        "Regularly inspect leaves and fruits."
    ],

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": [
        "Remove heavily infected crop residues after harvest.",
        "Use crop rotation to reduce disease carryover.",
        "Avoid continuous maize cultivation in the same field.",
        "Monitor leaves for rectangular grey or brown lesions."
    ],

    "Corn_(maize)___Common_rust_": [
        "Inspect leaves for reddish-brown rust pustules.",
        "Monitor the crop regularly, especially during humid weather.",
        "Use locally recommended resistant maize varieties.",
        "Consult an agricultural expert if infection increases."
    ],

    "Corn_(maize)___Northern_Leaf_Blight": [
        "Remove or manage infected crop residues after harvest.",
        "Practice crop rotation.",
        "Use resistant maize varieties where available.",
        "Monitor leaves for long cigar-shaped lesions."
    ],

    "Corn_(maize)___healthy": [
        "Your maize leaf appears healthy.",
        "Maintain balanced fertilizer application.",
        "Ensure proper irrigation and field drainage.",
        "Inspect the crop regularly for early disease symptoms."
    ],

    "Grape___Black_rot": [
        "Remove infected berries and dried grape clusters.",
        "Prune affected plant parts where appropriate.",
        "Maintain an open canopy for better airflow.",
        "Monitor leaves and fruits for dark lesions."
    ],

    "Grape___Esca_(Black_Measles)": [
        "Prune and remove severely affected wood where appropriate.",
        "Avoid injuries to grapevine trunks during pruning.",
        "Remove infected plant material from the vineyard.",
        "Consult a viticulture expert for disease management."
    ],

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": [
        "Remove heavily infected leaves where appropriate.",
        "Maintain proper vine spacing and airflow.",
        "Avoid unnecessary wetting of leaves.",
        "Monitor nearby grapevines for similar symptoms."
    ],

    "Grape___healthy": [
        "Your grape leaf appears healthy.",
        "Maintain proper vine training and pruning.",
        "Provide balanced irrigation and nutrition.",
        "Inspect leaves and grape clusters regularly."
    ],

    "Orange___Haunglongbing_(Citrus_greening)": [
        "Inspect leaves for blotchy yellowing and uneven discoloration.",
        "Check trees for signs of the Asian citrus psyllid.",
        "Do not move potentially infected plant material to other orchards.",
        "Contact an agricultural expert for confirmation and local management advice."
    ],

    "Peach___Bacterial_spot": [
        "Remove heavily infected leaves and fallen plant debris where appropriate.",
        "Avoid overhead irrigation.",
        "Maintain proper orchard sanitation.",
        "Consult an expert for locally recommended bacterial disease management."
    ],

    "Peach___healthy": [
        "Your peach leaf appears healthy.",
        "Maintain proper irrigation and balanced nutrition.",
        "Prune trees for good air circulation.",
        "Monitor leaves and fruits regularly."
    ],

    "Pepper,_bell___Bacterial_spot": [
        "Remove severely infected plant material where appropriate.",
        "Avoid working among wet plants.",
        "Use healthy seeds and disease-free seedlings.",
        "Consult an agricultural expert for suitable management practices."
    ],

    "Pepper,_bell___healthy": [
        "Your bell pepper leaf appears healthy.",
        "Maintain consistent soil moisture.",
        "Provide balanced fertilizer.",
        "Monitor leaves and fruits for unusual spots."
    ],

    "Potato___Early_blight": [
        "Remove heavily infected lower leaves where appropriate.",
        "Practice crop rotation with non-host crops.",
        "Avoid unnecessary leaf wetness.",
        "Monitor older leaves for brown spots with concentric rings."
    ],

    "Potato___Late_blight": [
        "Isolate and manage infected plants promptly.",
        "Avoid overhead irrigation and prolonged leaf wetness.",
        "Monitor the crop carefully during cool, humid weather.",
        "Seek expert advice for locally approved late blight management."
    ],

    "Potato___healthy": [
        "Your potato leaf appears healthy.",
        "Maintain proper soil moisture and drainage.",
        "Use balanced fertilizer according to soil requirements.",
        "Inspect plants regularly for disease symptoms."
    ],

    "Raspberry___healthy": [
        "Your raspberry leaf appears healthy.",
        "Maintain proper pruning and plant spacing.",
        "Avoid waterlogging around plant roots.",
        "Inspect leaves and fruits regularly."
    ],

    "Soybean___healthy": [
        "Your soybean leaf appears healthy.",
        "Maintain balanced soil nutrition.",
        "Monitor plants for insects and leaf diseases.",
        "Follow recommended irrigation and crop rotation practices."
    ],

    "Squash___Powdery_mildew": [
        "Remove severely infected leaves where appropriate.",
        "Improve air circulation between plants.",
        "Avoid excessive nitrogen fertilization.",
        "Monitor leaves for white powdery fungal growth."
    ],

    "Strawberry___Leaf_scorch": [
        "Remove severely affected leaves where appropriate.",
        "Maintain proper plant spacing and airflow.",
        "Avoid unnecessary overhead watering.",
        "Monitor new leaves for reddish-purple spots and browning."
    ],

    "Strawberry___healthy": [
        "Your strawberry leaf appears healthy.",
        "Maintain consistent soil moisture.",
        "Remove dead leaves and maintain field hygiene.",
        "Inspect plants regularly for disease symptoms."
    ],

    "Tomato___Bacterial_spot": [
        "Remove severely infected plant parts where appropriate.",
        "Avoid handling plants when leaves are wet.",
        "Use disease-free seeds and seedlings.",
        "Consult an expert for appropriate bacterial disease management."
    ],

    "Tomato___Early_blight": [
        "Remove infected lower leaves where appropriate.",
        "Avoid overhead watering.",
        "Practice crop rotation and maintain field hygiene.",
        "Monitor leaves for dark spots with concentric rings."
    ],

    "Tomato___Late_blight": [
        "Remove and isolate infected plant material promptly.",
        "Avoid prolonged leaf wetness.",
        "Monitor plants carefully during cool and humid weather.",
        "Consult an agricultural expert for appropriate disease management."
    ],

    "Tomato___Leaf_Mold": [
        "Improve ventilation around tomato plants.",
        "Avoid excessive humidity and leaf wetness.",
        "Remove severely infected leaves where appropriate.",
        "Monitor the underside of leaves for olive-green fungal growth."
    ],

    "Tomato___Septoria_leaf_spot": [
        "Remove infected lower leaves where appropriate.",
        "Avoid splashing soil onto leaves during watering.",
        "Maintain proper spacing between plants.",
        "Remove infected crop debris after harvest."
    ],

    "Tomato___Spider_mites Two-spotted_spider_mite": [
        "Inspect the underside of leaves for mites and fine webbing.",
        "Remove severely damaged leaves where appropriate.",
        "Monitor plants regularly for increasing mite populations.",
        "Seek expert advice on suitable integrated pest management."
    ],

    "Tomato___Target_Spot": [
        "Remove heavily infected leaves where appropriate.",
        "Maintain good air circulation around plants.",
        "Avoid unnecessary overhead watering.",
        "Monitor leaves for circular brown lesions."
    ],

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": [
        "Inspect plants for yellowing, leaf curling and stunted growth.",
        "Monitor for whiteflies, which can transmit the virus.",
        "Remove severely infected plants where appropriate.",
        "Use healthy seedlings and locally recommended resistant varieties."
    ],

    "Tomato___Tomato_mosaic_virus": [
        "Remove and isolate suspected infected plants where appropriate.",
        "Disinfect hands and tools after handling affected plants.",
        "Use certified disease-free seeds and seedlings.",
        "Avoid handling healthy plants immediately after infected plants."
    ],

    "Tomato___healthy": [
        "Your tomato leaf appears healthy.",
        "Maintain balanced watering and nutrition.",
        "Monitor plants regularly for insects and disease symptoms.",
        "Maintain proper plant spacing and field hygiene."
    ]
}


# ==============================
# ==========================================
# UPLOAD FOLDER
# ==========================================

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# HOME PAGE
# ==========================================

@disease_bp.route("/")
def home():
    return render_template("disease.html")


# ==========================================
# SERVE UPLOADED IMAGES
# ==========================================

@disease_bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ==========================================
# DISEASE PREDICTION
# ==========================================

@disease_bp.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return render_template(
            "disease.html",
            error="Please upload an image."
        )

    file = request.files["image"]

    if not file.filename:
        return render_template(
            "disease.html",
            error="Please select an image."
        )

    try:

        # Secure and uniquely name uploaded image
        original_name = secure_filename(file.filename)

        if not original_name:
            return render_template(
                "disease.html",
                error="Invalid image filename."
            )

        extension = os.path.splitext(original_name)[1].lower()

        if extension not in [".jpg", ".jpeg", ".png"]:
            return render_template(
                "disease.html",
                error="Only JPG, JPEG and PNG images are supported."
            )

        filename = str(uuid.uuid4()) + extension

        image_file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(image_file_path)

        # Open and resize image
        img = Image.open(image_file_path).convert("RGB")

        img = img.resize((224, 224))

        img_array = np.array(img)

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        # Model prediction
        # Keep the same preprocessing used during training.
        predictions = model.predict(
            img_array,
            verbose=0
        )

        predicted_index = int(
            np.argmax(predictions[0])
        )

        predicted_class = class_names[predicted_index]

        confidence = float(
            predictions[0][predicted_index] * 100
        )

        # Format disease name
        disease_name = predicted_class.replace(
            "___", " - "
        ).replace("_", " ")

        # ==================================
        # GET DISEASE-SPECIFIC GUIDANCE
        # ==================================

        guidance = disease_guidance.get(
            predicted_class,
            [
                "Monitor the plant regularly.",
                "Maintain proper crop hygiene.",
                "Consult an agricultural expert for suitable advice."
            ]
        )

        # Send all results to HTML
        return render_template(
            "disease.html",
            prediction=disease_name,
            confidence=round(confidence, 2),
            image_path=url_for("disease.uploaded_file", filename=filename),
            guidance=guidance
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

# if __name__ == "__main__":
#     app.run(
#         debug=True,
#         port=5001
#     )