import pymongo
from pymongo import MongoClient

from bson.objectid import ObjectId
from datetime import datetime, timedelta

import random

# Connect to MongoDB
connection_string = "mongodb+srv://mahadiqbalaiml27:9Gx_qVZ-tpEaHUu@healthcaresystem.ilezc.mongodb.net/healthcaresystem?retryWrites=true&w=majority&appName=Healthcaresystem"  # Replace with your MongoDB URI
client = MongoClient(connection_string)

# Select the database and collection
db = client["healthcaresystem"]  # Replace with your database name
doctors_collection = db["doctors"]

# List of hospitals
hospitals = [
    "Apollo Hospital", "Fortis Hospital", "Ruby General Hospital", 
    "CMRI", "Belle Vue Clinic", "Charnock Hospital",
    "Woodlands Multispeciality Hospital", "Desun Hospital", "AMRI Hospitals",
    "Medica Superspecialty Hospital","Apollo Multispeciality Hospital"
]

# List of specializations
specializations = [
    {"specialization": "ENT Specialist"},
    {"specialization": "Neurology"},
    {"specialization": "Dermatologist"},
    {"specialization": "Pediatrician"},
    {"specialization": "Cardiologist"},
    {"specialization": "General Medicine"},
    {"specialization": "Orthopedic Surgeon"},
    {"specialization": "Urologist"}
]

# Generate random availability
def generate_availability():
    availability = {}
    for _ in range(random.randint(2, 5)):
        date = (datetime.today() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        time = f"{random.randint(8, 20)}:00"
        slots = random.randint(3, 10)
        availability[date] = {time: slots}
    return availability

# Generate random doctors data
doctors = []
for i in range(1, 501):
    specialization = random.choice(specializations)["specialization"]
    doctor = {
        "name": f"Dr. Doctor {i}",
        "specialization": specialization,
        "phone_number": f"+91-9{random.randint(100000000, 999999999)}",
        "hospital": random.choice(hospitals),
        "availability": generate_availability(),
        "description": {
            "degrees": random.sample([
                "MBBS", "MD", "DM", "MS", "DNB", "MCh", "FRCS"], random.randint(1, 3)),
            "experience": f"Over {random.randint(5, 25)} years of experience in {specialization}.",
            "achievements": random.sample([
                "Published research papers.", "National Medical Award winner.", 
                "Performed hundreds of surgeries.", "Presented at global conferences.",
                "Authored medical textbooks.", "Recipient of Best Doctor Award."], random.randint(1, 3))
        },
        "fees": random.randint(500, 2000)
    }
    doctors.append(doctor)

# Insert into MongoDB
doctors_collection.insert_many(doctors)

print("500 doctors inserted into the 'doctors' collection.")
