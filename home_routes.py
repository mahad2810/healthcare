from flask import Blueprint, request, jsonify
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import random
import string
from werkzeug.utils import secure_filename
import os
from flask import current_app  # To access the `mongo` instance from app.py
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from bson import ObjectId

# Blueprint setup
home_bp = Blueprint("home", __name__)


# Geolocator setup
geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)

# Configuration for uploads
UPLOAD_FOLDER = 'static/test_presc/'
ALLOWED_EXTENSIONS = {'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper functions
def get_coordinates(address):
    api_key = 'AIzaSyDIenms8YDVpiOiIQGUc5VNgPqbGDGVgNI'
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': address, 'key': api_key}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None

def calculate_distance(user_address, hospital_address):
    user_coords = get_coordinates(user_address)
    hospital_coords = get_coordinates(hospital_address)
    if user_coords and hospital_coords:
        return geodesic(user_coords, hospital_coords).km
    return None

def serialize_hospital(hospital):
    hospital['_id'] = str(hospital['_id'])
    return hospital

def send_confirmation_email(patient_email, patient_name, test_slot_code, hospital_name, test_type, test_date, test_time):
    msg = MIMEMultipart()
    msg['From'] = 'thesevasetufoundation@gmail.com'
    msg['To'] = patient_email
    msg['Subject'] = 'Your Test Slot Confirmation Details'

    body = f"""
    Dear {patient_name},

    Greetings from The AuraMed!

    We are pleased to confirm your test slot booking. Below are the details:

    - Patient Name: {patient_name}
    - Confirmation Code: {test_slot_code}
    - Hospital Name: {hospital_name}
    - Test Type: {test_type}
    - Date: {test_date}
    - Time: {test_time}

    Please carry a valid ID proof and your prescription at the time of your appointment.

    Thank you for choosing SevaSetu Foundation.
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('auramed1628@gmail.com', 'kxmg wngq ksyp pzss')
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Routes
@home_bp.route('/get-hospitals', methods=['GET'])
def get_hospitals():
    try:
        user_lat = float(request.args.get('lat'))
        user_lng = float(request.args.get('lng'))
        hospitals_collection = current_app.mongo.db.hospitals
        hospitals = hospitals_collection.find()

        max_distance = 500  # Define the maximum distance (in km)
        nearest_hospitals = []

        for hospital in hospitals:
            address = hospital['address']
            hospital_coords = get_coordinates(address)
            if hospital_coords:
                distance = geodesic((user_lat, user_lng), hospital_coords).km
                if distance <= max_distance:
                    hospital['distance'] = distance
                    nearest_hospitals.append(serialize_hospital(hospital))

        nearest_hospitals.sort(key=lambda x: x['distance'])
        return jsonify(nearest_hospitals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@home_bp.route('/get-tests', methods=['GET'])
def get_test_availability():
    hospital_name = request.args.get('hospital')
    if not hospital_name:
        return jsonify({"error": "Hospital name is required"}), 400

    hospitals_collection = current_app.mongo.db.hospitals
    hospital = hospitals_collection.find_one({"name": hospital_name})

    if hospital:
        return jsonify({
            'tests': hospital.get('test_availability', {})
        })
    else:
        return jsonify({"error": "Hospital not found"}), 404

@home_bp.route('/book-test', methods=['POST'])
def book_test():
    if 'prescription_pdf' not in request.files:
        return jsonify({'error': 'Prescription PDF is required.'}), 400

    file = request.files['prescription_pdf']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed.'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    data = request.form
    patient_name = data.get('patient_name')
    patient_phone = data.get('patient_phone')
    patient_email = data.get('patient_email')
    hospital_name = data.get('hospital_name')
    test_category = data.get('test_category')
    test_type = data.get('test_type')
    test_date = data.get('test_date')
    test_time = data.get('test_time')

    if not all([patient_name, patient_phone, patient_email, hospital_name, test_category, test_type, test_date, test_time]):
        return jsonify({'error': 'All fields are required.'}), 400

    hospitals_collection = current_app.mongo.db.hospitals
    hospital = hospitals_collection.find_one({"name": hospital_name})
    if not hospital:
        return jsonify({'error': 'Hospital not found.'}), 404

    test_data = hospital.get('test_availability', {}).get(test_category, {}).get(test_type)
    if not test_data:
        return jsonify({'error': 'Invalid test category or type.'}), 400

    price = test_data['price']
    if test_date in test_data and test_time in test_data[test_date]:
        slots_available = test_data[test_date][test_time]['slots']
        if slots_available > 0:
            hospitals_collection.update_one(
                {"name": hospital_name},
                {"$inc": {f"test_availability.{test_category}.{test_type}.{test_date}.{test_time}.slots": -1}}
            )

            test_slot_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

            tests_collection = current_app.mongo.db.tests
            test_entry = {
                'patient_name': patient_name,
                'patient_phone': patient_phone,
                'patient_email': patient_email,
                'hospital_name': hospital_name,
                'test_category': test_category,
                'test_type': test_type,
                'test_date': test_date,
                'test_time': test_time,
                'price': price,
                'test_slot_code': test_slot_code,
                'prescription_path': file_path,
                'report': None,
                'status': 'ongoing'
            }
            tests_collection.insert_one(test_entry)

            send_confirmation_email(patient_email, patient_name, test_slot_code, hospital_name, test_type, test_date, test_time)

            return jsonify({'message': 'Test booked successfully!', 'test_slot_code': test_slot_code})
        else:
            return jsonify({'error': 'No available slots for the selected time.'}), 400
    else:
        return jsonify({'error': 'Invalid date or time selected.'}), 400
