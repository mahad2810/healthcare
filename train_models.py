import os
import numpy as np
import cv2
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

DATA_PATH = "healthcare/Skin_Data"
MODEL_PATH = "models"

if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

def load_skin_data(img_size=(256, 256)):
    categories = ['Non_Cancer', 'Cancer']
    data, labels = [], []

    for category in categories:
        for subset in ['Training', 'Testing']:
            path = os.path.join(DATA_PATH, category, subset)
            for img_name in os.listdir(path):
                img_path = os.path.join(path, img_name)
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.resize(img, img_size) / 255.0  # Normalize
                    data.append(img)
                    labels.append(category)

    data = np.array(data)
    labels = LabelEncoder().fit_transform(labels)  # cancer -> 1, non_cancer -> 0
    return train_test_split(data, labels, test_size=0.2, random_state=42, stratify=labels)

def build_cnn(input_shape):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_models(X_train, X_test, y_train, y_test):
    X_train_flat = X_train.reshape(X_train.shape[0], -1)
    X_test_flat = X_test.reshape(X_test.shape[0], -1)

    models = {
        "SVM": SVC(kernel='linear', probability=True),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        "CNN": build_cnn(input_shape=X_train.shape[1:])
    }

    for model_name, model in models.items():
        if model_name == "CNN":
            model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
            model.save(os.path.join(MODEL_PATH, "cnn_model.h5"))
        else:
            model.fit(X_train_flat, y_train)
            joblib.dump(model, os.path.join(MODEL_PATH, f"{model_name}_model.pkl"))

X_train, X_test, y_train, y_test = load_skin_data()
train_models(X_train, X_test, y_train, y_test)
