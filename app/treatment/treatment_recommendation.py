import streamlit as st
import pandas as pd


# =====================================
# KNOWLEDGE BASE
# =====================================

DISEASE_DATABASE = {

    "Diabetes": {

        "specialist": "Endocrinologist",

        "tests": [
            "HbA1c Test",
            "Fasting Blood Sugar",
            "Kidney Function Test",
            "Eye Examination"
        ],

        "medications": [
            "Metformin",
            "Insulin (if required)"
        ],

        "lifestyle": [
            "Low Sugar Diet",
            "Daily Exercise",
            "Weight Management"
        ]
    },

    "Heart Disease": {

        "specialist": "Cardiologist",

        "tests": [
            "ECG",
            "Echocardiogram",
            "Lipid Profile",
            "Stress Test"
        ],

        "medications": [
            "Statins",
            "Beta Blockers",
            "Aspirin"
        ],

        "lifestyle": [
            "Low Salt Diet",
            "Regular Walking",
            "Quit Smoking"
        ]
    },

    "Kidney Disease": {

        "specialist": "Nephrologist",

        "tests": [
            "Creatinine Test",
            "Urine Analysis",
            "Kidney Ultrasound"
        ],

        "medications": [
            "ACE Inhibitors",
            "Blood Pressure Control"
        ],

        "lifestyle": [
            "Low Protein Diet",
            "Hydration Monitoring"
        ]
    },

    "Cancer": {

        "specialist": "Oncologist",

        "tests": [
            "Biopsy",
            "CT Scan",
            "MRI",
            "PET Scan"
        ],

        "medications": [
            "Chemotherapy",
            "Targeted Therapy"
        ],

        "lifestyle": [
            "Nutrition Support",
            "Regular Follow-up"
        ]
    }
}


# =====================================
# TREATMENT RECOMMENDATION
# =====================================

def treatment_recommendation():

    st.title("💊 AI Treatment Recommendation Engine")

    disease = st.selectbox(
        "Select Disease",
        [
            "Diabetes",
            "Heart Disease",
            "Kidney Disease",
            "Cancer"
        ]
    )

    severity = st.select_slider(
        "Severity Level",
        options=[
            "Low",
            "Moderate",
            "High"
        ]
    )

    if st.button("Generate Recommendation"):

        data = DISEASE_DATABASE[disease]

        st.success(
            f"Recommended Specialist: "
            f"{data['specialist']}"
        )

        st.subheader(
            "🧪 Recommended Diagnostic Tests"
        )

        for test in data["tests"]:
            st.write(f"✔ {test}")

        st.subheader(
            "💊 Medication Guidance"
        )

        for med in data["medications"]:
            st.write(f"✔ {med}")

        st.subheader(
            "🥗 Lifestyle Recommendations"
        )

        for item in data["lifestyle"]:
            st.write(f"✔ {item}")

        if severity == "High":

            st.error(
                "High Severity Detected"
            )

            st.warning(
                "Immediate Specialist Consultation Recommended"
            )

            st.warning(
                "Hospital Monitoring May Be Required"
            )

        elif severity == "Moderate":

            st.warning(
                "Schedule Follow-up Within 7 Days"
            )

        else:

            st.success(
                "Continue Routine Monitoring"
            )


# =====================================
# ANALYTICS
# =====================================

def treatment_analytics():

    st.subheader(
        "📊 Treatment Analytics"
    )

    data = pd.DataFrame({

        "Disease": [
            "Diabetes",
            "Heart Disease",
            "Kidney Disease",
            "Cancer"
        ],

        "Cases": [
            150,
            120,
            70,
            50
        ]
    })

    st.bar_chart(
        data.set_index(
            "Disease"
        )
    )


# =====================================
# MAIN FUNCTION
# =====================================

def treatment_module():

    menu = st.sidebar.selectbox(
        "Treatment Menu",
        [
            "Treatment Recommendation",
            "Treatment Analytics"
        ]
    )

    if menu == "Treatment Recommendation":
        treatment_recommendation()

    elif menu == "Treatment Analytics":
        treatment_analytics()