import streamlit as st
import numpy as np
import pandas as pd
import joblib

MODEL_PATH = "models/outcome_model.pkl"


# =====================================
# LOAD MODEL
# =====================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


# =====================================
# ICU RISK
# =====================================

def icu_risk(severity, oxygen):

    if oxygen < 85 or severity > 8:
        return "High"

    elif oxygen < 90:
        return "Moderate"

    return "Low"


# =====================================
# READMISSION RISK
# =====================================

def readmission_risk(age, severity):

    score = (age * 0.3) + (severity * 8)

    if score > 70:
        return "High"

    elif score > 40:
        return "Moderate"

    return "Low"


# =====================================
# MORTALITY RISK
# =====================================

def mortality_risk(age, oxygen):

    score = age + (100 - oxygen)

    if score > 110:
        return "High"

    elif score > 80:
        return "Moderate"

    return "Low"


# =====================================
# PREDICTION
# =====================================

def predict_outcome():

    st.subheader("🏥 Patient Outcome Prediction")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=45
    )

    severity = st.slider(
        "Disease Severity",
        1,
        10,
        5
    )

    oxygen = st.slider(
        "Oxygen Saturation (%)",
        70,
        100,
        95
    )

    heart_rate = st.slider(
        "Heart Rate",
        40,
        180,
        80
    )

    hospital_days = st.slider(
        "Hospital Stay Days",
        1,
        30,
        5
    )

    if st.button("Predict Outcome"):

        model = load_model()

        input_data = np.array([
            [
                age,
                severity,
                oxygen,
                heart_rate,
                hospital_days
            ]
        ])

        probability = model.predict_proba(
            input_data
        )[0][1]

        recovery_probability = round(
            probability * 100,
            2
        )

        st.metric(
            "Recovery Probability",
            f"{recovery_probability}%"
        )

        st.metric(
            "Expected Stay",
            f"{hospital_days} Days"
        )

        st.info(
            f"ICU Requirement Risk: "
            f"{icu_risk(severity, oxygen)}"
        )

        st.warning(
            f"Readmission Risk: "
            f"{readmission_risk(age, severity)}"
        )

        st.error(
            f"Mortality Risk: "
            f"{mortality_risk(age, oxygen)}"
        )


# =====================================
# ANALYTICS
# =====================================

def outcome_analytics():

    st.subheader(
        "📊 Outcome Analytics"
    )

    data = pd.DataFrame({
        "Outcome": [
            "Recovered",
            "ICU",
            "Readmission",
            "Mortality Risk"
        ],
        "Patients": [
            450,
            80,
            120,
            40
        ]
    })

    st.bar_chart(
        data.set_index("Outcome")
    )


# =====================================
# MAIN MODULE
# =====================================

def outcome_prediction():

    st.title(
        "🏥 AI Outcome Prediction"
    )

    menu = st.sidebar.selectbox(
        "Outcome Prediction Menu",
        [
            "Predict Outcome",
            "Outcome Analytics"
        ]
    )

    if menu == "Predict Outcome":
        predict_outcome()

    elif menu == "Outcome Analytics":
        outcome_analytics()