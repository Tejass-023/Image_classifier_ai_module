from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Model load karo
MODEL_PATH = "civic_eye_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Class labels (dataset ke folders ke hisaab se)
class_labels = ["garbage", "pothole", "streetlight", "water_leakage"]

@app.route("/")
def home():
    return "Civic Eye AI Model is Running 🚀"

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # File ko temp save karo
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    # Preprocess image
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Prediction
    preds = model.predict(img_array)
    class_idx = np.argmax(preds)
    result = class_labels[class_idx]

    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True)
