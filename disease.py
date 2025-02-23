from flask import Blueprint, request, jsonify, current_app
from disease_predict import DiseasePredictionModel
from docsuggest import get_specialization
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
import joblib



# Initialize the blueprint
disease_blueprint = Blueprint('disease', __name__)

# Instantiate the disease prediction model
disease_model = DiseasePredictionModel()

@disease_blueprint.route('/disease/predict_disease', methods=['POST'])
def predict_disease():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms')
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400

        predictions = disease_model.predict(symptoms)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@disease_blueprint.route('/get_doctors', methods=['POST'])
def get_doctors():
    try:
        data = request.get_json()
        disease = data.get('disease', '').strip()
        if not disease:
            return jsonify({'error': 'Disease not specified.'}), 400

        specialization = get_specialization(disease)
        if not specialization:
            return jsonify({'doctors': [], 'message': f'No specialization found for disease: {disease}'}), 200

        doctors = current_app.mongo.db.doctors.find({"specialization": {'$regex': specialization, '$options': 'i'}})
        response_data = [{
            "name": doc.get("name", "Name not available"),
            "specialization": doc.get("specialization", "Specialization not available"),
            "description": doc.get("description", {}),
            "phone_number": doc.get("phone_number", "Not available"),
            "hospital": doc.get("hospital", "Not available"),
            "availability": doc.get("availability", {}),
            "fees": doc.get("fees", "Not specified")
        } for doc in doctors]

        return jsonify({"doctors": response_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Directory containing trained models
MODELS_DIR = "models"

@disease_blueprint.route("/predict", methods=["POST"])
def predict():
    print("Prediction request received.")
    if "image" not in request.files:
        print("No file uploaded.")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["image"]
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    print(f"File saved at {file_path}.")

    try:
        # Load and preprocess the image
        img_size = (256, 256)
        img = cv2.imread(file_path)
        if img is None:
            raise ValueError("Invalid image file")
        print("Image loaded successfully.")
        img = cv2.resize(img, img_size) / 255.0  # Normalize
        img_flat = img.flatten().reshape(1, -1)  # Flatten for ML models
        print("Image preprocessed successfully.")

        results = {}

        # Predict using Random Forest
        rf_model = joblib.load(f"{MODELS_DIR}/Random Forest_model.pkl")
        print("Random Forest model loaded.")
        rf_probs = rf_model.predict_proba(img_flat)[0] * 100
        results["Random_Forest"] = f"Cancer: {rf_probs[0]:.2f}%, Non-Cancer: {rf_probs[1]:.2f}%"
        print(f"Random Forest Prediction: {results['Random_Forest']}")

        # Predict using XGBoost
        xgb_model = joblib.load(f"{MODELS_DIR}/XGBoost_model.pkl")
        print("XGBoost model loaded.")
        xgb_probs = xgb_model.predict_proba(img_flat)[0] * 100
        results["XGBoost"] = f"Cancer: {xgb_probs[0]:.2f}%, Non-Cancer: {xgb_probs[1]:.2f}%"
        print(f"XGBoost Prediction: {results['XGBoost']}")

        return jsonify(results)
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)
        print(f"File {file_path} removed.")
