
# AuraMed

**Your One-Stop Solution for All Hospital and Healthcare Needs**

---

## **Overview**
AuraMed is designed to simplify hospital visits and enhance healthcare services. It allows users to book, cancel, or adjust appointments at nearby hospitals, select the most suitable doctors based on fees and availability, and even book test slots at their convenience. Users can also check bed availability at hospitals and request beds by sending an email. If unsure about symptoms, users can utilize the symptom checker to predict potential diseases and get doctor recommendations. Health records can be uploaded and tracked, including prescriptions, reports, and health data such as blood pressure, sugar levels, and period tracking for females. AuraMed also provides a map of nearby hospitals with routes, along with the AuraBot chatbot for user assistance.

---

## **Key Features**

### **User Dashboard**
1. **Nearby Hospital Locator**: View a list of nearby hospitals and their locations on an interactive map with route navigation.
2. **Test and Appointment Booking**: Book, cancel, or adjust appointments and test slots.
3. **Symptom Checker**: Predict potential diseases based on user-provided symptoms and get doctor recommendations.
4. **Bed Availability**: Check bed availability in nearby hospitals and send email requests for needed beds.
5. **Health Record Management**: Upload and track prescriptions, lab reports, and health data (e.g., blood pressure, sugar levels, periods tracking for females).
6. **Reminders**: Notifications for updating health data, upcoming appointments or tests, and new reports and prescriptions uploaded by hospitals.
7. **AuraBot**: AI-powered chatbot for assistance with appointments, test slots, bed inquiries, and navigating the platform.

### **Hospital Dashboard**
1. **Data Management**: Update and manage doctor availability, test slots, bed availability, and other hospital data.
2. **Appointment & Test Management**: Handle appointments, mark tests as done, and upload prescriptions and reports.

---

## **Technology Stack**

### **Backend**
- **Flask**: Manages backend logic and API routing.
- **MongoDB**: Stores user, hospital, appointment, test ,doctors and health record data.
- **Google OAuth 2.0**: Provides secure user authentication.
- **SMTP**: Automates email communications (e.g., confirmations, reminders, and bed requests).
- **APScheduler**: Schedules notifications and background tasks.

### **Frontend**
- **HTML/CSS**: Responsive and user-friendly design.
- **JavaScript**: Implements dynamic functionality.
- **Leaflet.js**: Real-time hospital mapping and routing.

### **APIs and Geolocation**
- **Google Geocoding API**: Converts addresses into geographic coordinates.
- **Geopy**: Calculates distances to hospitals for better recommendations.

### **Machine Learning**
- **Scikit-learn**: Implements disease prediction using three models:
  - Random Forest
  - Naive Bayes
  - Support Vector Classifier (SVC)

---

## **Machine Learning Models**

### **Disease Prediction**
- **Description**: Predicts diseases based on symptoms using machine learning.
  - **Models**: Random Forest, Naive Bayes, and Support Vector Classifier (SVC).
  - **Process**: Combines model outputs using statistical mode for enhanced accuracy.

### **Doctor-Specialization Mapping**
- **Description**: Maps predicted diseases to relevant medical specializations and fetches doctor details for appointment booking.
  - **Data Source**: Doctor details are stored in JSON files, which are processed using Pandas.

---

## **APIs Used**
1. **Google OAuth 2.0 API**: Secure user authentication.
2. **SMTP**: Sends automated emails for booking confirmations, reminders, and notifications.
3. **APScheduler**: Sends reminders for appointments, tests, and health data updates.
4. **Google Geocoding API**: Converts addresses to coordinates for mapping.
5. **Geopy**: Calculates distances between user and hospital locations.

---

## **Maps Integration**
- **Platform**: OpenStreetMap
- **Routing**: Leaflet Routing Machine for navigation.
- **Backend**: Node.js and Express.js.
- **Frontend**: HTML and CSS.
- **Data Source**: MongoDB stores hospital details and locations.

**GitHub Repository for Maps Integration:**  [GitHub Repository for Maps Integration](https://github.com/SAPtadeep27/hospital_map)
---

## **Setup Instructions**

1. **Clone the Repository**:  
   ```bash
   git clone <repository_url>
   ```
2. **Navigate to the Project Directory**:  
   ```bash
   cd healthcare
   ```
3. **Install Requirements**:  
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**:  
   ```bash
   python app.py
   ```

---

## **Testing**
- The backend routes and endpoints were rigorously tested using Postman, with a collection file (`AuraMed.postman_collection.json`) included for reference.

---

## **Database**
The platform uses MongoDB for storing test data during development. Once the website is launched, hospitals will register themselves and provide all the details dynamically.

---

## **Reminders**

Health data Reminder intervals are set for a short interval of time for testing purpose

---

### Future Goals

1. **Advanced API Integration**  
   - Integrate FHIR (Fast Healthcare Interoperability Resources) API to enhance interoperability with electronic health records (EHR).  
   - Add support for teleconsultation APIs to enable virtual doctor appointments.

2. **Data Security and Compliance**  
   - Implement industry-standard encryption techniques to safeguard user data.  
   - Ensure compliance with healthcare data regulations like HIPAA and GDPR to protect user privacy.

3. **Mobile Application Development**  
   - Build a dedicated mobile app for iOS and Android platforms to extend accessibility and convenience.  
   - Leverage push notifications for reminders, updates, and alerts to enhance user engagement.

---


## Resources  
- **Article:** [Read about AuraMed on Medium](https://medium.com/@dwaipayanmath/all-about-auramed-our-healthcare-management-website-b402e9ec2bc3)  
- **Demo Video:** [YouTube Video](https://www.youtube.com/watch?v=nMtvSfWKZA8)  
- **Postman Collection:** [AuraMed Postman Collection](https://auramed-351316.postman.co/workspace/New-Team-Workspace~10702ae5-fd3b-493b-b1c1-ec1e4e6c43eb/request/40647141-d2860a14-13e9-4566-84d0-20b8fcd70b28?action=share&creator=40647141&ctx=documentation)  

---

