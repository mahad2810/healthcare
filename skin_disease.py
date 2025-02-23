#!/usr/bin/env python
# coding: utf-8

# In[6]:


import kagglehub

# Download latest version
path = kagglehub.dataset_download("kylegraupe/skin-cancer-binary-classification-dataset")

print("Path to dataset files:", path)


# In[32]:


""" !pip install numpy
!pip install pandas
!pip install opencv-python 
!pip install matplotlib 
!pip install seaborn 
!pip install scikit-learn 
!pip install xgboost 
!pip install tensorflow 
!pip install keras """
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

def load_skin_data(base_path, img_size=(256, 256)):
    """
    Load skin cancer images from folder and preprocess them.
    Args:
    - base_path (str): Path to Skin_Data folder.
    - img_size (tuple): Desired image size (default: 128x128).
    
    Returns:
    - X_train, X_test, y_train, y_test (numpy arrays): Preprocessed images and labels.
    """
    categories = ['Non_Cancer','Cancer']
    data, labels = [], []

    for category in categories:
        path_train = os.path.join(base_path, category, 'Training')
        path_test = os.path.join(base_path, category, 'Testing')

        for img_folder, label in [(path_train, category), (path_test, category)]:
            for img_name in os.listdir(img_folder):
                img_path = os.path.join(img_folder, img_name)
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.resize(img, img_size) / 255.0  # Normalize
                    data.append(img)
                    labels.append(label)

    # Convert lists to numpy arrays
    data = np.array(data)
    labels = np.array(labels)

    # Encode labels
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)  # cancer -> 1, non_cancer -> 0

    # Split into training and testing
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42, stratify=labels)
    
    return X_train, X_test, y_train, y_test

def build_cnn(input_shape):
    """
    Build a simple CNN model for skin cancer classification.
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')  # Binary classification
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_models(X_train, X_test, y_train, y_test):
    """
    Train 4 ML models for skin cancer detection and evaluate their performance.
    """
    # Reshape data for ML models
    X_train_flat = X_train.reshape(X_train.shape[0], -1)
    X_test_flat = X_test.reshape(X_test.shape[0], -1)

    models = {
        "SVM": SVC(kernel='linear', probability=True),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        "CNN": build_cnn(input_shape=X_train.shape[1:])
    }

    results = {}

    for model_name, model in models.items():
        if model_name == "CNN":
            # Convert labels to categorical for CNN
            y_train_cnn = to_categorical(y_train, num_classes=2)
            y_test_cnn = to_categorical(y_test, num_classes=2)

            model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
            model.save("cnn_model.h5") 
            y_pred = (model.predict(X_test) > 0.5).astype("int32")
        else:
            model.fit(X_train_flat, y_train)
            y_pred = model.predict(X_test_flat)
            joblib.dump(model,model_name+"_model.pkl")

        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)

        results[model_name] = {
            "Accuracy": acc,
            "Confusion Matrix": cm
        }

        print(f"\nModel: {model_name}")
        print(f"Accuracy: {acc:.4f}")
        print("Confusion Matrix:\n", cm)
        print(classification_report(y_test, y_pred))

        # ROC Curve
        y_pred_prob = model.predict_proba(X_test_flat)[:, 1] if model_name != "CNN" else model.predict(X_test)
        fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
        roc_auc = auc(fpr, tpr)

        plt.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.2f})')

    # ROC Plot
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve Comparison')
    plt.legend()
    plt.show()

    return results

# Load Data
base_path = "C:/Users/DELL/.cache/kagglehub/datasets/kylegraupe/skin-cancer-binary-classification-dataset/versions/1/Skin_Data"
X_train, X_test, y_train, y_test = load_skin_data(base_path)

# Train and Evaluate Models
results = train_models(X_train, X_test, y_train, y_test)


# In[45]:


import joblib
import numpy as np
import cv2
import tensorflow as tf

def predict_skin_cancer(image_path, models_dir="."):
    """
    Predicts whether a skin image is cancerous using trained models.
    
    Use Case:
    This function can be used in medical diagnostic applications to assist dermatologists in identifying skin cancer
    from dermoscopic images. It can be integrated into healthcare platforms for automated skin lesion analysis.
    
    Args:
    - image_path (str): Path to the image file.
    - models_dir (str): Directory where models are stored.
    
    Returns:
    - results (dict): Dictionary containing predictions from each model in percentage for cancer and non-cancer.
    """
    # Load and preprocess the image
    img_size = (256, 256)
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unable to read.")
    img = cv2.resize(img, img_size) / 255.0  # Normalize
    img_flat = img.flatten().reshape(1, -1)  # Flatten for ML models
    img = np.expand_dims(img, axis=0)  # Reshape for CNN
    
    results = {}
    
    # Load and predict using SVM
    svm_model = joblib.load(f"{models_dir}/SVM_model.pkl")
    svm_probs = svm_model.predict_proba(img_flat)[0] * 100  # Probabilities for both classes
    results["SVM"] = f"Cancer: {svm_probs[0]:.2f}%, Non-Cancer: {svm_probs[1]:.2f}%"
    
    # Load and predict using Random Forest
    rf_model = joblib.load(f"{models_dir}/Random Forest_model.pkl")
    rf_probs = rf_model.predict_proba(img_flat)[0] * 100
    results["Random Forest"] = f"Cancer: {rf_probs[0]:.2f}%, Non-Cancer: {rf_probs[1]:.2f}%"
    
    # Load and predict using XGBoost
    xgb_model = joblib.load(f"{models_dir}/XGBoost_model.pkl")
    xgb_probs = xgb_model.predict_proba(img_flat)[0] * 100
    results["XGBoost"] = f"Cancer: {xgb_probs[0]:.2f}%, Non-Cancer: {xgb_probs[1]:.2f}%"
    
    # Load and predict using CNN
    cnn_model = tf.keras.models.load_model(f"{models_dir}/cnn_model.h5")
    cnn_prob = cnn_model.predict(img)[0][0] * 100
    results["CNN"] = f"Cancer: {100 - cnn_prob:.2f}%, Non-Cancer: {cnn_prob:.2f}%"
    
    return results


# In[47]:


image_path = "C:/Users/DELL/.cache/kagglehub/datasets/kylegraupe/skin-cancer-binary-classification-dataset/versions/1/Skin_Data/Non_Cancer/Training/597-03-1.JPG"
results = predict_skin_cancer(image_path)
print(results)

