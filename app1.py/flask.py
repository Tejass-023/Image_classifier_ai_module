# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# import datetime

# app = Flask(__name__)

# # Database setup (SQLite for now)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Complaint Table
# class Complaint(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.Text, nullable=False)   # complaint text / speech result
#     category = db.Column(db.String(50), nullable=True) # AI will fill later
#     latitude = db.Column(db.Float, nullable=True)
#     longitude = db.Column(db.Float, nullable=True)
#     image_url = db.Column(db.String(200), nullable=True)
#     created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# # Create DB
# with app.app_context():
#     db.create_all()

# # ---------- API Endpoints ---------- #

# # Submit Complaint
# @app.route('/submit_complaint', methods=['POST'])
# def submit_complaint():
#     try:
#         data = request.json
#         description = data.get("description")
#         latitude = data.get("latitude")
#         longitude = data.get("longitude")
#         image_url = data.get("image_url")

#         if not description:
#             return jsonify({"error": "Complaint description is required"}), 400

#         new_complaint = Complaint(
#             description=description,
#             latitude=latitude,
#             longitude=longitude,
#             image_url=image_url
#         )
#         db.session.add(new_complaint)
#         db.session.commit()

#         return jsonify({"message": "Complaint submitted successfully!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # Get All Complaints
# @app.route('/complaints', methods=['GET'])
# def get_complaints():
#     try:
#         complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
#         data = []
#         for c in complaints:
#             data.append({
#                 "id": c.id,
#                 "description": c.description,
#                 "category": c.category,
#                 "latitude": c.latitude,
#                 "longitude": c.longitude,
#                 "image_url": c.image_url,
#                 "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S")
#             })
#         return jsonify(data), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # Get Single Complaint by ID
# @app.route('/complaint/<int:complaint_id>', methods=['GET'])
# def get_complaint(complaint_id):
#     complaint = Complaint.query.get_or_404(complaint_id)
#     return jsonify({
#         "id": complaint.id,
#         "description": complaint.description,
#         "category": complaint.category,
#         "latitude": complaint.latitude,
#         "longitude": complaint.longitude,
#         "image_url": complaint.image_url,
#         "created_at": complaint.created_at.strftime("%Y-%m-%d %H:%M:%S")
#     })


# # Update Complaint Category (for admin/AI)
# @app.route('/update_category/<int:complaint_id>', methods=['PUT'])
# def update_category(complaint_id):
#     complaint = Complaint.query.get_or_404(complaint_id)
#     data = request.json
#     complaint.category = data.get("category")
#     db.session.commit()
#     return jsonify({"message": "Category updated successfully"}), 200


# # ---------- Run Server ---------- #
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000, debug=True)


@app.post("/speech-to-text")
def speech_to_text(file: UploadFile = File(...)):
    model = whisper.load_model("base")
    result = model.transcribe(file.file, language="hi")
    return {"text": result["text"]}
