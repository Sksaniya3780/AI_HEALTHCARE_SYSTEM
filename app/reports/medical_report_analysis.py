import streamlit as st
import pandas as pd
import os
import pdfplumber
from PIL import Image

# ==========================================
# CONFIGURATION
# ==========================================

UPLOAD_DIR = "uploads/reports"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

# ==========================================
# PDF TEXT EXTRACTION
# ==========================================

def extract_pdf_text(pdf_file):

    text = ""

    try:
        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

    except Exception as e:
        st.error(f"Error Reading PDF: {e}")

    return text


# ==========================================
# UPLOAD REPORT
# ==========================================

def upload_report():

    st.subheader("📄 Upload Medical Report")

    uploaded_file = st.file_uploader(
        "Upload PDF / Image Report",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        file_path = os.path.join(
            UPLOAD_DIR,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ Report Uploaded Successfully")

        if uploaded_file.type == "application/pdf":

            text = extract_pdf_text(file_path)

            st.subheader("📋 Extracted Report Content")

            st.text_area(
                "Report Text",
                text,
                height=300
            )

        else:

            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded Medical Report",
                use_container_width=True
            )


# ==========================================
# BLOOD TEST ANALYSIS
# ==========================================

def blood_test_analysis():

    st.subheader("🩸 Blood Test Analysis")

    col1, col2 = st.columns(2)

    with col1:

        hemoglobin = st.number_input(
            "Hemoglobin (g/dL)",
            min_value=0.0,
            max_value=25.0,
            value=13.5
        )

        sugar = st.number_input(
            "Blood Sugar (mg/dL)",
            min_value=0,
            max_value=500,
            value=100
        )

    with col2:

        cholesterol = st.number_input(
            "Cholesterol (mg/dL)",
            min_value=0,
            max_value=500,
            value=180
        )

        oxygen = st.number_input(
            "Oxygen Saturation (%)",
            min_value=0,
            max_value=100,
            value=98
        )

    if st.button("🔍 Analyze Report"):

        alerts = []

        if hemoglobin < 12:
            alerts.append("⚠ Low Hemoglobin Detected")

        if sugar > 180:
            alerts.append("⚠ High Blood Sugar Detected")

        if cholesterol > 240:
            alerts.append("⚠ High Cholesterol Detected")

        if oxygen < 90:
            alerts.append("🚨 Low Oxygen Level")

        st.markdown("---")

        if alerts:

            st.error("Abnormal Values Found")

            for alert in alerts:
                st.write(alert)

        else:

            st.success("✅ All Parameters Are Within Normal Range")

        st.subheader("🤖 AI Health Insights")

        if sugar > 180:
            st.warning("Possible Diabetes Risk")

        if cholesterol > 240:
            st.warning("Possible Cardiovascular Risk")

        if oxygen < 90:
            st.error("Immediate Medical Attention Recommended")

        if (
            sugar <= 180 and
            cholesterol <= 240 and
            oxygen >= 90 and
            hemoglobin >= 12
        ):
            st.success(
                "Patient Health Indicators Appear Stable"
            )


# ==========================================
# REPORT HISTORY
# ==========================================

def report_history():

    st.subheader("📁 Uploaded Reports")

    files = os.listdir(UPLOAD_DIR)

    if len(files) == 0:

        st.warning("No Reports Uploaded Yet")

    else:

        df = pd.DataFrame(
            {
                "Report Name": files
            }
        )

        st.dataframe(
            df,
            use_container_width=True
        )


# ==========================================
# ANALYTICS DASHBOARD
# ==========================================

def analytics_dashboard():

    st.subheader("📊 Medical Analytics Dashboard")

    sample_data = pd.DataFrame({

        "Condition": [
            "Diabetes Risk",
            "Heart Disease",
            "Anemia",
            "Low Oxygen"
        ],

        "Cases": [
            120,
            90,
            60,
            35
        ]
    })

    st.dataframe(
        sample_data,
        use_container_width=True
    )

    st.bar_chart(
        sample_data.set_index(
            "Condition"
        )
    )

    st.subheader("Hospital Risk Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Diabetes",
        "120"
    )

    c2.metric(
        "Heart Disease",
        "90"
    )

    c3.metric(
        "Anemia",
        "60"
    )

    c4.metric(
        "Low Oxygen",
        "35"
    )


# ==========================================
# MAIN FUNCTION
# ==========================================

def medical_report_analysis():

    st.title(
        "🧾 Medical Report Analysis System"
    )

    st.markdown(
        """
        Upload medical reports,
        analyze blood test values,
        monitor patient risks,
        and view healthcare analytics.
        """
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Upload Report",
        "🩸 Blood Test Analysis",
        "📁 Report History",
        "📊 Analytics Dashboard"
    ])

    with tab1:
        upload_report()

    with tab2:
        blood_test_analysis()

    with tab3:
        report_history()

    with tab4:
        analytics_dashboard()