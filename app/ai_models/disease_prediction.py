import streamlit as st
import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "models/disease_model.pkl"


# =====================================
# LOAD MODEL
# =====================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


# =====================================
# RISK CALCULATION
# =====================================

def calculate_severity(risk):

    if risk < 30:
        return "Low Risk"

    elif risk < 70:
        return "Moderate Risk"

    return "High Risk"


# =====================================
# PREDICTION
# =====================================

def predict_disease():

    st.subheader("🧠 Disease Prediction")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=30
    )

    blood_pressure = st.number_input(
        "Blood Pressure",
        min_value=50,
        max_value=250,
        value=120
    )

    sugar = st.number_input(
        "Sugar Level",
        min_value=50,
        max_value=400,
        value=100
    )

    cholesterol = st.number_input(
        "Cholesterol",
        min_value=50,
        max_value=500,
        value=150
    )

    bmi = st.number_input(
        "BMI",
        min_value=10.0,
        max_value=60.0,
        value=25.0
    )

    if st.button("Predict Disease Risk"):

        model = load_model()

        input_data = np.array([
            [
                age,
                blood_pressure,
                sugar,
                cholesterol,
                bmi
            ]
        ])

        prediction = model.predict(
            input_data
        )[0]

        probability = model.predict_proba(
            input_data
        )[0][1]

        risk_score = round(
            probability * 100,
            2
        )

        severity = calculate_severity(
            risk_score
        )

        st.success(
            f"Risk Score: {risk_score}%"
        )

        st.info(
            f"Severity Level: {severity}"
        )

        if prediction == 1:

            st.error(
                "Potential Disease Risk Detected"
            )

            if sugar > 180:
                st.warning(
                    "Possible Diabetes Risk"
                )

            if blood_pressure > 140:
                st.warning(
                    "Possible Heart Disease Risk"
                )

        else:

            st.success(
                "No Major Disease Risk Detected"
            )


# =====================================
# ANALYTICS DEMO
# =====================================

def disease_dashboard():

    st.subheader(
        "📊 Disease Analytics"
    )

    sample_data = pd.DataFrame({
        "Disease": [
            "Diabetes",
            "Heart Disease",
            "Kidney Disease",
            "Cancer"
        ],
        "Cases": [
            120,
            90,
            60,
            40
        ]
    })

    st.bar_chart(
        sample_data.set_index(
            "Disease"
        )
    )


# =====================================
# MAIN MODULE
# =====================================

def disease_prediction():

    st.title(
        "🧠 AI Disease Prediction System"
    )

    menu = st.sidebar.selectbox(
        "Disease Prediction Menu",
        [
            "Predict Disease",
            "Disease Analytics"
        ]
    )

    if menu == "Predict Disease":
        predict_disease()

    elif menu == "Disease Analytics":
        disease_dashboard()