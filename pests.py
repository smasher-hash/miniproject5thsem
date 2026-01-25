from flask import Flask, render_template, jsonify

pests = Flask(__name__)

# Sample pest data
pests_data = [
    {"name": "Rice Blast", "cause": "Fungus", "symptoms": "Gray leaf spots", "prevention": "Use resistant varieties"},
    {"name": "Bollworm", "cause": "Insect Larvae", "symptoms": "Holes in cotton bolls", "prevention": "Neem oil spray"},
    {"name": "Tomato Leaf Curl", "cause": "Virus", "symptoms": "Leaf curling, yellowing", "prevention": "Remove infected plants"}
]

@pests.route("/api/pests")
def get_pests():
    return jsonify(pests_data)

@pests.route("/")
def home():
    return render_template("pests.html")

if __name__ == "__main__":
    pests.run(debug=True)
