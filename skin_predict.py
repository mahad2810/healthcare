import os
import joblib
import numpy as np
import cv2
from google.cloud import aiplatform
from flask import current_app


def predict_skin_cancer(image_path, img_size=(128, 128)):
    """
    Predict skin cancer classification using Vertex AI deployed models.

    Args:
    - image_path (str): Path to the input image.
    - img_size (tuple): Dimensions to resize the input image.

    Returns:
    - results (dict): Predictions from each model.
    """
    # Load and preprocess the input image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unable to read.")
    img = cv2.resize(img, img_size) / 255.0  # Normalize
    img_flat = img.flatten().tolist()  # Convert to list for JSON serialization

    # Vertex AI endpoint details
    endpoints = {
        "Random_Forest": {
            "endpoint_id": "1784345743671164928",
            "region": "us-central1"
        },
        "XGBoost": {
            "endpoint_id": "2689569268772634624",
            "region": "us-central1"
        },
        "SVM": {
            "endpoint_id": "2007836875179425792",
            "region": "us-central1"
        }
    }

    results = {}

    for model_name, details in endpoints.items():
        try:
            # Initialize Vertex AI client
            aiplatform.init(project=current_app.config["GCP_PROJECT"], location=details["region"])

            # Get endpoint
            endpoint = aiplatform.Endpoint(endpoint_name=details["endpoint_id"])

            # Make prediction
            prediction = endpoint.predict(instances=[img_flat])

            if prediction and prediction.predictions:
                prob = prediction.predictions[0]  # Assuming the response contains probabilities
                results[model_name] = f"Cancer: {prob[0]:.2f}%, Non-Cancer: {prob[1]:.2f}%"
            else:
                results[model_name] = "Prediction failed or empty response."
        except Exception as e:
            results[model_name] = f"Error: {str(e)}"

    return results

def ensemble_prediction(results):
    """
    Use majority voting to determine the final prediction.

    Args:
    - results (dict): Dictionary containing model predictions in the format:
      {'ModelName': 'Cancer: XX.XX%, Non-Cancer: YY.YY%'}

    Returns:
    - str: Final prediction ("Cancer" or "Non-Cancer").
    """
    # Extract Cancer and Non-Cancer probabilities
    cancer_votes = 0
    non_cancer_votes = 0

    for model, result in results.items():
        if "Error" in result or "Prediction failed" in result:
            continue  # Skip models that failed to predict

        # Parse probabilities from the string
        cancer_prob = float(result.split('Cancer: ')[1].split('%')[0])
        non_cancer_prob = float(result.split('Non-Cancer: ')[1].split('%')[0])

        # Increment vote for the higher probability class
        if cancer_prob > non_cancer_prob:
            cancer_votes += 1
        else:
            non_cancer_votes += 1

    # Determine final prediction based on majority voting
    if cancer_votes > non_cancer_votes:
        return "Final Prediction: Cancer"
    elif non_cancer_votes > cancer_votes:
        return "Final Prediction: Non-Cancer"
    else:
        return "Final Prediction: Tie (Equal Votes)"
