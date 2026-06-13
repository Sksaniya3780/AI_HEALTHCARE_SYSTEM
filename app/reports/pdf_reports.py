import streamlit as st
from reportlab.pdfgen import canvas

def pdf_reports():

    st.title("📄 PDF Report Generator")

    if st.button("Generate PDF"):

        pdf_file = "patient_report.pdf"

        c = canvas.Canvas(pdf_file)

        c.drawString(
            100,
            750,
            "AI Healthcare Report"
        )

        c.save()

        with open(pdf_file, "rb") as f:

            st.download_button(
                "Download PDF",
                f,
                file_name=pdf_file
            )