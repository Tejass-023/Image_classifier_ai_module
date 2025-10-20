# enhanced_backend.py
from flask import Flask, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from sentence_transformers import SentenceTransformer, util

# -----------------------
# 1️⃣ Initialize Flask App
# -----------------------
app = Flask(__name__)

# -----------------------
# 2️⃣ Load AI Models
# -----------------------
# Image Classifier
image_model = load_model("civic_eye_model.h5")
classes = ["garbage", "pothole", "streetlight", "water_leakage"]

# Duplicate Detector
text_model = SentenceTransformer('all-MiniLM-L6-v2')

# In-memory DB demo (replace with real DB)
complaints_db = [
    {"id": 1, "text": "Pothole near MG Road", "location": "MG Road"},
    {"id": 2, "text": "Water leakage in park area", "location": "Central Park"},
    {"id": 3, "text": "Streetlight not working near main square", "location": "Main Square"}
]

# -----------------------
# 3️⃣ Helper Functions
# -----------------------
def predict_category(text, img_path=None):
    """Predict category using image classifier if image provided, else simple text heuristic"""
    if img_path:
        img = image.load_img(img_path, target_size=(224,224))
        img_array = np.expand_dims(image.img_to_array(img)/255.0, axis=0)
        pred = image_model.predict(img_array)
        class_idx = np.argmax(pred)
        confidence = float(np.max(pred)) * 100
        return classes[class_idx], confidence
    else:
        # Simple heuristic for demo
        text_lower = text.lower()
        if "garbage" in text_lower:
            return "garbage", 90
        elif "pothole" in text_lower:
            return "pothole", 91
        elif "streetlight" in text_lower:
            return "streetlight", 90
        elif "water" in text_lower or "leakage" in text_lower:
            return "water_leakage", 89
        else:
            return "others", 70

def check_duplicate(new_text, location, top_k=3, threshold=0.8):
    """Check for duplicates using cosine similarity"""
    db_texts = [c['text'] for c in complaints_db]
    embeddings_db = text_model.encode(db_texts, convert_to_tensor=True)
    new_embedding = text_model.encode(new_text, convert_to_tensor=True)
    
    cos_scores = util.cos_sim(new_embedding, embeddings_db)[0]
    duplicates = []
    for idx, score in enumerate(cos_scores):
        if float(score) > threshold and location == complaints_db[idx]['location']:
            duplicates.append({"id": complaints_db[idx]['id'], "text": complaints_db[idx]['text'], "similarity": float(score)})
    
    duplicates = sorted(duplicates, key=lambda x: x['similarity'], reverse=True)[:top_k]
    return (True if duplicates else False), duplicates

# -----------------------
# 4️⃣ API Route
# -----------------------
@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    text = request.form.get('text', '')
    location = request.form.get('location', '')
    image_file = request.files.get('image')
    
    # Save image if provided
    img_path = None
    if image_file:
        img_path = f"uploads/{image_file.filename}"
        image_file.save(img_path)
    
    # AI category prediction
    category, confidence = predict_category(text, img_path)
    
    # Duplicate check
    duplicate_flag, top_similar = check_duplicate(text, location)
    
    # Save complaint in DB (demo)
    complaint_id = len(complaints_db) + 1
    complaints_db.append({
        "id": complaint_id,
        "text": text,
        "location": location,
        "category": category,
        "confidence": confidence,
        "duplicate_flag": duplicate_flag
    })
    
    # Build interactive text output
    output_lines = []
    output_lines.append("✅ Complaint submitted successfully!")
    if duplicate_flag:
        output_lines.append("⚠️ Duplicate Alert: Similar complaint(s) already exist.\n")
        for idx, dup in enumerate(top_similar, 1):
            output_lines.append(f"{idx}️⃣ \"{dup['text']}\" | Similarity: {int(dup['similarity']*100)}%")
        output_lines.append("")  # blank line
    output_lines.append(f"🛠 AI Prediction: Category = {category} | Confidence = {int(confidence)}%")
    output_lines.append(f"Complaint ID : {complaint_id}")
    
    return "\n".join(output_lines)

# -----------------------
# 5️⃣ Run Flask
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
