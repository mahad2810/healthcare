# In doclist.py (Blueprint for Doctor and Appointment Management)
from flask import Blueprint, jsonify, request, render_template,current_app
from bson.objectid import ObjectId
import random, string, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

doclist_bp = Blueprint('doclist', __name__)



def generate_appointment_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@doclist_bp.route('/specializations', methods=['GET'])
def fetch_specializations():
    hospital = request.args.get('hospital')
    if not hospital:
        return jsonify({"error": "Hospital is required"}), 400

    specializations = [
        "Cardiologist",
        "Neurology",
        "Orthopedics",
        "Pediatrics",
        "General Medicine"
    ]

    return jsonify(specializations)



@doclist_bp.route('/doctors', methods=['GET'], endpoint='fetch_doctors_list')
def fetch_doctors():
    hospital = request.args.get('hospital')
    if not hospital:
        return jsonify({"error": "Hospital parameter is required"}), 400

    doctors_collection = current_app.mongo.db.doctors
    query = {'hospital': hospital}
    doctors = doctors_collection.find(query)
    doctor_list = [
        {
            "id": str(doc["_id"]),
            "name": doc["name"],
            "specialization": doc.get("specialization", "General"),
            "hospital": doc["hospital"],
            "degrees": doc.get("degrees", []),
            "experience": doc.get("experience", "Not specified"),
            "achievements": doc.get("achievements", [])
        }
        for doc in doctors
    ]

    return jsonify(doctor_list if doctor_list else [])

@doclist_bp.route('/doctor/<doctor_id>', methods=['GET'], endpoint='fetch_doctor_details_view')
def fetch_doctor_details(doctor_id):
    doctors_collection = current_app.mongo.db.doctors
    doctor = doctors_collection.find_one({"_id": ObjectId(doctor_id)})

    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    description = doctor.get("description", {})
    doctor_details = {
        "name": doctor.get("name"),
        "specialization": doctor.get("specialization"),
        "phone_number": doctor.get("phone_number"),
        "hospital": doctor.get("hospital"),
        "fees": doctor.get("fees"),
        "degrees": description.get("degrees", []),
        "experience": description.get("experience", "Not specified"),
        "achievements": description.get("achievements", []),
        "availability": doctor.get("availability", {})
    }

    return jsonify(doctor_details)

@doclist_bp.route('/appointment', methods=['POST'])
def create_appointment():
    data = request.json
    print("Received data:", data)

    # Define required fields
    required_fields = [
        'patient_name', 'doctor_name', 'doctor_specialization',
        'doctor_hospital', 'phone', 'email', 'date_time'
    ]

    # Validate if all required fields are present
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    # Extract date and time from the date_time field
    try:
        date, time = data['date_time'].split('T')
        time = time[:5]  # Truncate to match HH:MM format if seconds are included
    except ValueError:
        return jsonify({"error": "Invalid date_time format. Use ISO 8601 format: YYYY-MM-DDTHH:MM:SS"}), 400

    # Access the database collections
    doctors_collection = current_app.mongo.db.doctors
    appointments_collection = current_app.mongo.db.appointments

    # Find the doctor in the database
    doctor = doctors_collection.find_one({"name": data['doctor_name']})
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    # Check the doctor's availability
    availability = doctor.get('availability', {})
    print("Doctor's availability:", availability)  # Debugging information

    # Ensure the requested date and time are correctly formatted and exist in availability
    if date not in availability:
        return jsonify({
            "error": f"No availability for the requested date: {date}.",
            "available_dates": list(availability.keys())
        }), 400

    if time not in availability[date]:
        available_slots = [
            f"{available_time} ({slots} slots)"
            for available_time, slots in availability[date].items() if slots > 0
        ]
        return jsonify({
            "error": f"No availability for the requested time: {time}.",
            "available_slots": available_slots
        }), 400

    if availability[date][time] <= 0:
        available_slots = [
            f"{available_time} ({slots} slots)"
            for available_time, slots in availability[date].items() if slots > 0
        ]
        return jsonify({
            "error": "Selected time slot is fully booked.",
            "available_slots": available_slots
        }), 400

    # Generate a unique appointment ID
    appointment_id = generate_appointment_id()

    # Create the appointment document
    appointment = {
        "appointment_id": appointment_id,
        "patient_name": data['patient_name'],
        "doctor_name": data['doctor_name'],
        "doctor_specialization": data['doctor_specialization'],
        "doctor_hospital": data['doctor_hospital'],
        "patient_phone": data['phone'],
        "patient_email": data['email'],
        "date_time": data['date_time'],
        "status": "ongoing"
    }

    # Insert the appointment into the appointments collection
    appointments_collection.insert_one(appointment)

    # Decrement the available slots for the selected time
    doctors_collection.update_one(
        {"name": data['doctor_name']},
        {"$inc": {f"availability.{date}.{time}": -1}}
    )

    # Send confirmation email to the patient
    send_confirmation_email(
        data['email'], data['patient_name'], data['doctor_name'],
        data['doctor_specialization'], data['doctor_hospital'],
        data['date_time'], appointment_id
    )

    # Return success response
    return jsonify({"message": "Appointment booked successfully", "appointment_id": appointment_id})



def send_confirmation_email(patient_email, patient_name, doctor_name, doctor_specialization, doctor_hospital, date_time, appointment_id):
    msg = MIMEMultipart()
    msg['From'] = 'auramed1628@gmail.com'
    msg['To'] = patient_email
    msg['Subject'] = 'Appointment Confirmation Details'

    body = f"""
    Dear {patient_name},

    Greetings from The AuraMed!

    We are pleased to confirm your appointment booking. Below are the details:

    - **Patient Name**: {patient_name}
    - **Doctor Name**: {doctor_name}
    - **Specialization**: {doctor_specialization}
    - **Hospital Name**: {doctor_hospital}
    - **Appointment Date and Time**: {date_time}
    - **Appointment ID**: {appointment_id}

    Please arrive 15 minutes before the scheduled time.

    Regards,
    The SevaSetu Foundation Team
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('auramed1628@gmail.com', 'kxmg wngq ksyp pzss')
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print(f"Email sent to {patient_email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
