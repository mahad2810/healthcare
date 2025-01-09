from flask import Blueprint, request, jsonify,current_app
from disease_predict import DiseasePredictionModel
from docsuggest import get_specialization, get_doctor_details

# Initialize the blueprint
disease_blueprint = Blueprint('disease', __name__)

# Instantiate the disease prediction model
disease_model = DiseasePredictionModel()

@disease_blueprint.route('/disease/predict_disease', methods=['POST'])
def predict_disease():
    try:
        # Get the symptoms list from the request body
        data = request.get_json()
        symptoms = data.get('symptoms')
        print("Symptoms Received: ", symptoms)


        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400

        # Call the predict method from the model
        predictions = disease_model.predict(symptoms)

        print(predictions)

        # Return the final prediction as a JSON response
        return jsonify(predictions)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@disease_blueprint.route('/get_doctors', methods=['POST'])
def get_doctors():
    try:
        # Parse the incoming JSON request
        data = request.get_json()
        disease = data.get('disease', '').strip()

        if not disease:
            return jsonify({"error": "Disease not specified."}), 400

        # Get specialization based on disease
        specialization = get_specialization(disease)
        if not specialization:
            return jsonify({"doctors": [], "message": f"No specialization found for disease: {disease}"}), 200

        # Query doctors based on specialization
        doctors = current_app.mongo.db.doctors.find({"specialization": {'$regex': specialization, '$options': 'i'}})

        # Prepare the response data
        response_data = []
        for doctor in doctors:
            try:
                response_data.append({
                    "name": doctor.get("name", "Name not available"),
                    "specialization": doctor.get("specialization", "Specialization not available"),
                    "description": {
                        "degrees": doctor.get("description", {}).get("degrees", []),
                        "experience": doctor.get("description", {}).get("experience", "No experience details available."),
                        "achievements": doctor.get("description", {}).get("achievements", []),
                    },
                    "phone_number": doctor.get("phone_number", "Not available"),
                    "hospital": doctor.get("hospital", "Not available"),
                    "availability": doctor.get("availability", {}),
                    "fees": doctor.get("fees", "Not specified")
                })
            except AttributeError as e:
                print(f"Error processing doctor: {doctor}. Error: {str(e)}")

        # Return response
        if not response_data:
            return jsonify({"doctors": [], "message": "No doctors currently available."}), 200

        return jsonify({"doctors": response_data}), 200

    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500
