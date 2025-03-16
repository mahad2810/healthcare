# AuraMed

AuraMed is a comprehensive healthcare management platform that optimizes hospital operations, enhances patient flow, and integrates inventory tracking solutions. It consists of two applications:

- **User App**: A one-stop solution for users to book appointments, check hospital services, track their health records, and receive AI-powered medical assistance.
- **Hospital App**: Enables hospitals to manage appointments, update availability, handle inventory, and facilitate virtual consultations.

## Features

### User Dashboard
- **Nearby Hospital Locator**: View hospitals on a map and find the best route.
- **Appointment & Test Booking**: Book, cancel, or adjust hospital visits.
- **Symptom Checker & Disease Prediction**: AI-driven tool to predict possible diseases based on symptoms.
- **Skin Cancer Detection**: Upload skin images for AI-based analysis.
- **Bed Availability & Requests**: Check real-time bed availability and send requests.
- **Health Records Management**: Upload and store prescriptions, reports, and track health parameters.
- **Reminders**: Automated alerts for appointments, tests, and health data updates.
- **AuraBot Chat Assistant**: AI chatbot for assistance with bookings and queries.
- **Video Call Consultation**: Secure WebRTC-based video calls with doctors.

### Hospital Dashboard
- **Live Updates**: Manage doctor availability, test slots, and bed status.
- **Appointment & Test Handling**: Mark appointments as completed and upload reports.
- **Inventory Management**: Add, edit, delete medicines/equipment with low-stock reminders.
- **Call Management**: Create and manage virtual consultations.

## Technology Stack

### Backend
- **Flask**: Python web framework
- **Flask Extensions**: Flask-CORS, Flask-PyMongo, Werkzeug
- **MongoDB Atlas**: NoSQL database for healthcare data
- **Google OAuth2**: Secure authentication
- **SMTP**: Email notifications
- **APScheduler**: Task scheduling
- **Firebase**: Handle push notifications and user data.

### Frontend
- **HTML, CSS**: UI design
- **Flask Templates**: Server-side rendering
- **Leaflet.js & OpenStreetMap**: Hospital mapping and navigation
- **Dialogflow**: AI-powered chatbot

### Machine Learning
- **Scikit-learn**: Random Forest, Naive Bayes, SVC for disease prediction
- **XGBoost**
- **TensorFlow & Keras**

### Video Call Integration
- **React.js, WebRTC, Socket.io**: Peer-to-peer video communication
- **Node.js & Express.js**: Backend signaling server

### Map Technology Stack
- **Leaflet.js**: Interactive map rendering
- **OpenStreetMap**: Open-source mapping data
- **Google Geocoding API**: Address-to-coordinate conversion
- **Geopy**: Distance calculations
- **Flask & Python**: Backend for processing map data

## Setup Instructions(Dont Use Google Login as https isnt provided)

1. Clone the repository:
   ```bash
   git clone https://github.com/mahad2810/healthcare.git
   ```
2. Navigate to the project folder:
   ```bash
   cd healthcare
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python app.py
   ```

## API Integrations
- **Google OAuth 2.0 API**: User authentication
- **SMTP**: Email notifications for bookings and reminders
- **APScheduler**: Automated reminders for appointments and health updates
- **Google Geocoding API**: Convert hospital addresses into coordinates
- **Geopy**: Distance calculations for hospital proximity


## Future Enhancements
- **Separation of User and Hospital Apps** for better stability
- **UI Improvements**
- **Advanced Video Calling**: We are able to make the server and create the call, but there is a slight issue in managing incoming calls and the frontend. We need to improve it fully.

## Additional Resources
- **[Project Article](https://medium.com/@dwaipayanmath/auramed-comprehensive-healthcare-management-platform-2941d904888c)**: Detailed description of AuraMed.
- **[Map Integration GitHub](https://github.com/SAPtadeep27/hospital_map/blob/master/app.js)**: Real-time hospital mapping.

---

AuraMed aims to revolutionize healthcare accessibility by integrating AI, machine learning, and real-time services for an optimized hospital experience.

