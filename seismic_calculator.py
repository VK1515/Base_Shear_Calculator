"""
IS 1893 Seismic Base Shear Calculator
Copyright (c) 2026 Your Name / Organization

All rights reserved.

This software is provided for educational and non-commercial use only.
Redistribution, modification, or commercial use is strictly prohibited
without prior written permission from the author.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import cm
from reportlab.lib.colors import lightgrey

# ==============================
# CONFIG
# ==============================
AUTHOR_NAME = "Vrushali Kamalakar "
APP_TITLE = "IS 1893 Seismic Base Shear Calculator"

st.set_page_config(page_title="IS Seismic Calculator", layout="centered")

# ==============================
# UI WARNING / DETERRENCE
# ==============================
st.warning(
    "This tool is provided for educational and professional reference only. "
    "Unauthorized copying, redistribution, or commercial use is prohibited."
)

st.title(APP_TITLE)
st.caption("Enter seismic weight W in kN. All results will be in kN.")

# ------------------------------
# User Tag (for export traceability)
# ------------------------------
user_tag = st.text_input("Enter your name / ID (will appear on report)", value="")

st.divider()

# ------------------------------
# Select Year
# ------------------------------
year = st.selectbox(
    "Select Code Year",
    [1962, 1966, 1970, 1984, 2002, 2025]
)

st.divider()

formula_text = ""
values = {}
result_text = ""
numeric_result = {}

# ------------------------------
# INPUT + CALCULATION
# ------------------------------
if year == 1962:
    formula_text = "F = ah × W"
    ah = st.number_input("Horizontal Seismic Coefficient (ah)", value=0.0)
    W = st.number_input("Seismic Weight W (kN)", value=0.0)
    values = {"ah": ah, "W (kN)": W}

    if st.button("Calculate"):
        F = ah * W
        result_text = f"F = {F:.4f} kN"
        numeric_result = {"F (kN)": F}

elif year == 1966:
    formula_text = "Vb = C × ah × W"
    C = st.number_input("Flexibility Coefficient (C)", value=0.0)
    ah = st.number_input("Horizontal Seismic Coefficient (ah)", value=0.0)
    W = st.number_input("Seismic Weight W (kN)", value=0.0)
    values = {"C": C, "ah": ah, "W (kN)": W}

    if st.button("Calculate"):
        Vb = C * ah * W
        result_text = f"Vb = {Vb:.4f} kN"
        numeric_result = {"Vb (kN)": Vb}

elif year == 1970:
    formula_text = "Vb = C × ah × beta × W"
    C = st.number_input("Flexibility Coefficient (C)", value=0.0)
    ah = st.number_input("Horizontal Seismic Coefficient (ah)", value=0.0)
    beta = st.number_input("Soil Foundation Factor (beta)", value=0.0)
    W = st.number_input("Seismic Weight W (kN)", value=0.0)
    values = {"C": C, "ah": ah, "beta": beta, "W (kN)": W}

    if st.button("Calculate"):
        Vb = C * ah * beta * W
        result_text = f"Vb = {Vb:.4f} kN"
        numeric_result = {"Vb (kN)": Vb}

elif year == 1984:
    formula_text = "Vb = K × C × beta × I × ao × W"
    K = st.number_input("Performance Factor (K)", value=0.0)
    C = st.number_input("Flexibility Coefficient (C)", value=0.0)
    beta = st.number_input("Soil Foundation Factor (beta)", value=0.0)
    I = st.number_input("Importance Factor (I)", value=1.0)
    ao = st.number_input("Zone Factor (ao)", value=0.0)
    W = st.number_input("Seismic Weight W (kN)", value=0.0)
    values = {"K": K, "C": C, "beta": beta, "I": I, "ao": ao, "W (kN)": W}

    if st.button("Calculate"):
        Vb = K * C * beta * I * ao * W
        result_text = f"Vb = {Vb:.4f} kN"
        numeric_result = {"Vb (kN)": Vb}

elif year == 2002:
    formula_text = "Vb = (Z / 2) × (I / R) × (Sa/g) × W"
    Z = st.number_input("Seismic Zone Factor (Z)", value=0.0)
    I = st.number_input("Importance Factor (I)", value=1.0)
    R = st.number_input("Response Reduction Factor (R)", value=1.0)
    Sa_by_g = st.number_input("Spectral Acceleration Ratio (Sa/g)", value=0.0)
    W = st.number_input("Seismic Weight W (kN)", value=0.0)
    values = {"Z": Z, "I": I, "R": R, "Sa/g": Sa_by_g, "W (kN)": W}

    if st.button("Calculate"):
        Vb = (Z / 2.0) * (I / R) * Sa_by_g * W
        result_text = f"Vb = {Vb:.4f} kN"
        numeric_result = {"Vb (kN)": Vb}

elif year == 2025:
    formula_text = "VBD,H = (Z × I × A_NH / R) × W ,  VBD,V = (Z × I × A_NV) × W"
    Z = st.number_input("Hazard Factor (Z)", value=0.0)
    I = st.number_input("Importance Factor (I)", value=1.0)
    R = st.number_input("Ductility Factor (R)", value=1.0)
    A_NH = st.number_input("Horizontal Response Coefficient (A_NH)", value=0.0)
    A_NV = st.number_input("Vertical Response Coefficient (A_NV)", value=0.0)
    W = st.number_input("Seismic Weight W (kN)", value=0.0)
    values = {"Z": Z, "I": I, "R": R, "A_NH": A_NH, "A_NV": A_NV, "W (kN)": W}

    if st.button("Calculate"):
        VBD_H = (Z * I * A_NH / R) * W
        VBD_V = (Z * I * A_NV) * W
        result_text = f"VBD,H = {VBD_H:.4f} kN , VBD,V = {VBD_V:.4f} kN"
        numeric_result = {"VBD,H (kN)": VBD_H, "VBD,V (kN)": VBD_V}

# ------------------------------
# DISPLAY
# ------------------------------
st.subheader("Formula Used")
st.code(formula_text)

st.subheader("Entered Values")
for k, v in values.items():
    st.write(f"{k} = {v}")

st.subheader("Result")
if result_text:
    st.success(result_text)
else:
    st.info("Enter values and click Calculate.")

# ==============================
# GRAPHICAL BASE SHEAR DISTRIBUTION
# ==============================
fig = None
if numeric_result:
    st.divider()
    st.subheader("Base Shear Distribution (Storey-wise)")

    num_storeys = st.number_input("Number of Storeys", min_value=1, step=1)

    if st.button("Generate Distribution Graph"):
        total_shear = list(numeric_result.values())[0]

        storey_numbers = list(range(1, int(num_storeys) + 1))
        shear_distribution = [(i / num_storeys) * total_shear for i in storey_numbers]

        fig = plt.figure()
        plt.bar(storey_numbers, shear_distribution)
        plt.xlabel("Storey Number")
        plt.ylabel("Shear (kN)")
        plt.title("Linear Base Shear Distribution")
        st.pyplot(fig)

# ==============================
# FULL PDF EXPORT (INPUTS + GRAPH)
# ==============================
if numeric_result and fig is not None:

    st.divider()
    st.subheader("Export Full Report (PDF)")

    if st.button("Download Full Report as PDF"):

        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Save graph to buffer
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format="png", dpi=300, bbox_inches="tight")
        img_buffer.seek(0)

        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # -------- Title --------
        story.append(Paragraph(f"<b>{APP_TITLE}</b>", styles["Title"]))
        story.append(Spacer(1, 8))

        # -------- Meta --------
        story.append(Paragraph(f"Author / Institute: {AUTHOR_NAME}", styles["Normal"]))
        story.append(Paragraph(f"Generated by: {user_tag if user_tag else 'Not Provided'}", styles["Normal"]))
        story.append(Paragraph(f"Timestamp: {timestamp}", styles["Normal"]))
        story.append(Spacer(1, 10))

        # -------- Formula --------
        story.append(Paragraph(f"<b>Code Year:</b> {year}", styles["Normal"]))
        story.append(Paragraph(f"<b>Formula Used:</b> {formula_text}", styles["Normal"]))
        story.append(Spacer(1, 10))

        # -------- Inputs --------
        story.append(Paragraph("<b>Entered Values:</b>", styles["Heading2"]))
        for k, v in values.items():
            story.append(Paragraph(f"{k} = {v}", styles["Normal"]))

        story.append(Spacer(1, 10))

        # -------- Result --------
        story.append(Paragraph("<b>Result:</b>", styles["Heading2"]))
        for k, v in numeric_result.items():
            story.append(Paragraph(f"{k} = {v:.4f} kN", styles["Normal"]))

        story.append(Spacer(1, 12))

        # -------- Graph --------
        story.append(Paragraph("<b>Base Shear Distribution:</b>", styles["Heading2"]))
        img = Image(img_buffer, width=14 * cm, height=8 * cm)
        story.append(img)

        story.append(Spacer(1, 12))

        # -------- Footer --------
        story.append(Paragraph(
            "© 2026 " + AUTHOR_NAME + ". All rights reserved. "
            "Unauthorized copying, redistribution or commercial use is strictly prohibited.",
            styles["Italic"]
        ))

        doc.build(story)

        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer.getvalue(),
            file_name="seismic_full_report.pdf",
            mime="application/pdf"
        )

# ==============================
# LEGAL FOOTER
# ==============================
st.divider()
st.caption("© 2026 " +" "Vrushali Kamalakar"+ ". All rights reserved. Unauthorized copying, redistribution or commercial use is strictly prohibited.")
