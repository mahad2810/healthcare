Here’s how your README will look with the tech stack details included:  

---

# **AuraMed**  

AuraMed is a comprehensive healthcare management platform designed to simplify hospital and healthcare-related services. From booking appointments and managing test slots to checking bed availability and using an AI-powered symptom checker, AuraMed ensures a seamless experience for users while providing robust tools for hospitals.  

---

## **Features**  

### **User Dashboard**  
1. **Nearby Hospital Locator**: View a list of nearby hospitals or see them on a map with routes.  
2. **Appointment and Test Booking**: Book, cancel, or adjust appointments and test slots.  
3. **Symptom Checker**: Predict diseases based on symptoms and get recommended doctors.  
4. **Bed Availability**: Check bed availability in nearby hospitals and request beds via email.  
5. **Health Records Management**: Upload and access past prescriptions and reports.  
6. **Health Data Tracker**: Track metrics like sugar levels, blood pressure, weight, and periods, with reminders for updates.  
7. **Reminders**: Get notified about upcoming appointments, tests, and health data updates.  
8. **AuraBot**: A chatbot assistant for booking, cancellations, checking availability, and other queries.  

### **Hospital Dashboard**  
1. **Manage Availability**: Update doctor availability, test slots, and bed status.  
2. **Handle Bookings**: Mark appointments and tests as done and upload reports or prescriptions.  
3. **Add New Services**: Seamlessly add new doctors, tests, or beds to the system.  

---

## **Tech Stack**  

### **Backend**  
- **Flask**: Lightweight Python framework for routing, templates, and business logic.  
- **Flask Extensions**:  
  - Flask-CORS: Handles Cross-Origin Resource Sharing.  
  - Flask-PyMongo: Simplifies MongoDB interactions.  
  - Werkzeug: Secure uploads and password hashing.  
- **MongoDB**: NoSQL database managed through MongoDB Atlas.  
- **Authentication**: Google OAuth2 for secure user authentication.  
- **Email Services**: SMTP for sending emails for confirmations, reminders, and bed requests.  
- **Scheduler**: APScheduler for handling background tasks and notifications.  

### **Frontend**  
- **HTML/CSS**: Templates and styling for user interfaces.  
- **Flask Templates**: For server-side rendering of web pages.  

### **Data Processing and Machine Learning**  
- **Pandas & NumPy**: Data manipulation and numerical computation.  
- **Scikit-learn**: Implements machine learning models:  
  - Random Forest Classifier  
  - Naive Bayes  
  - Support Vector Classifier (SVC)  
- **Statistics**: Used for disease prediction and analysis.  

### **APIs and Geolocation**  
- **Google Maps API**: Geocoding and distance calculations.  
- **Geopy**: Location-based distance measurements.  

### **File Handling**  
- **Secure Uploads**: Handles user-uploaded files like prescriptions and reports.  

### **Blueprints**  
- Modular app structure with specific modules for dashboards, routes, and search functionalities.  

### **Other Technologies**  
- **BSON**: For handling MongoDB ObjectIds.  
- **Random/String Generation**: For secure IDs and tokens.  

---

## **Machine Learning Models**  

### Disease Prediction Model  
Uses Random Forest, Naive Bayes, and Support Vector Classifier (SVC) to predict diseases based on symptoms. It:  
- Accepts symptoms as input and converts them into one-hot encoded vectors.  
- Predicts diseases using all three models and determines the final prediction via statistical mode.  
- Provides fallback mechanisms for invalid inputs or prediction conflicts.  

### Doctor-Specialization Mapping System  
- Maps diseases to specializations using a JSON-based system.  
- Retrieves doctor details for a given specialization to recommend suitable professionals.  

---

## **APIs and Libraries**  

1. **Google OAuth 2.0 API**: For secure user authentication.  
2. **SMTP**: Sends emails for confirmations, reminders, and bed requests.  
3. **APScheduler**: Schedules tasks and reminders.  
4. **Google Geocoding API**: Converts addresses into geographical coordinates.  
5. **Geopy**: Fetches location data and calculates distances.  

---

## **How to Run the Project**  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-repo-url  
   ```  

2. Navigate to the project directory:  
   ```bash  
   cd AuraMed  
   ```  

3. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. Set up the environment variables:  
   - `MONGO_URI`: MongoDB Atlas URI.  
   - `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`: For Google OAuth.  
   - `SMTP_SERVER` and `SMTP_CREDENTIALS`: For email services.  

5. Run the Flask application:  
   ```bash  
   flask run  
   ```  

6. Access the application at `http://localhost:5000`.  

---

## **Future Enhancements**  
- Mobile app integration for seamless accessibility.  
- Enhanced AI capabilities for personalized health recommendations.  
- Real-time bed and doctor availability tracking using IoT.  

---

## **Contributing**  
Contributions are welcome! Feel free to submit issues or pull requests to enhance AuraMed.  

---

## **License**  
This project is licensed under the MIT License.  

---  

This README ensures clarity, professionalism, and a comprehensive overview of your submission.
