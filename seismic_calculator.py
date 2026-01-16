"""
IS 1893 Seismic Base Shear Calculator
Copyright (c) 2026 Vrushali Kamalakar

All rights reserved.

This software is provided for educational and non-commercial use only.
Redistribution, modification, or commercial use is strictly prohibited
without prior written permission from the author.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.colors import lightgrey
from reportlab.lib.units import inch

# ==============================
# OWNER DETAILS
# ==============================
OWNER_NAME = "Vrushali Kamalakar"
INSTITUTE_NAME = "MECS"

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="IS Seismic Calculator", layout="centered")

# ==============================
# UI WARNING / DETERRENCE
# ==============================
st.warning(
    "This tool is provided for educational and professional reference only. "
    "Unauthorized copying, redistribution, or commercial use is strictly prohibited."
)

st.title("IS 1893 Seismic Base Shear Calculator")
st.caption("Enter seismic weight W in kN. All results will be in kN.")

# User tag for audit trail
user_tag = st.text_input("User Name / ID (will appear in report)", value="")

st.divider()

# ==============================
# SELECT YEAR
# ==============================
year = st.selectbox(
    "Select Code Year",
    [1962, 1966, 1970, 1984, 2002, 2016, 2025]
)

st.divider()

# ==============================
# VARIABLES
# ==============================
formula_text = ""
values = {}
result_text = ""
numeric_result = {}

# ==============================
# INPUT + CALCULATION
# ==============================
if year == 1962:
    formula_text = "F = ah × W"

    ah = st.number_input("Horizontal Seismic Coefficient (ah)", value=0.0, format="%.5f")
    W = st.number_input("Seismic Weight W (kN)", value=0.0, format="%.2f")

    values = {"ah": ah, "W (kN)": W}

    if st.button("Calculate"):
        F = ah * W
        result_text = f"F = {F:.4f} kN"
        numeric_result = {"F (kN)": F}

elif year == 1966:
    formula_text = "Vb = C × ah × W"

    C = st.number_input("Flexibility Coefficient (C)", value=0.0, format="%.5f")
    ah = st.number_input("Horizontal Seismic Coefficient (ah)", value=0.0, format="%.5f")
    W = st.number_input("Seismic Weight W (kN)", value=0.0, format="%.2f")

    values = {"C": C, "ah": ah, "W (kN)": W}

    if st.button("Calculate"):
        Vb = C * ah * W
        result_text = f"Vb = {Vb:.4f} kN"
        numeric_result = {"Vb (kN)": Vb}

elif year == 1970:
    formula_text = "Vb = C × ah × beta × W"

    C = st.number_input("Flexibility Coefficient (C)", value=0.0, format="%.5f")
    ah = st.number_input("Horizontal Seismic Coefficient (ah)", value=0.0, format="%.5f")
    beta = st.number_input("Soil Foundation Factor (beta)", value=0.0, format="%.5f")
    W = st.number_input("Seismic Weight W (kN)", value=0.0, format="%.2f")

    values = {"C": C, "ah": ah, "beta": beta, "W (kN)": W}

    if st.button("Calculate"):
        Vb = C * ah * beta * W
        result_text = f"Vb = {Vb:.4f} kN"
        numeric_result = {"Vb (kN)": Vb}

elif year == 1984:
    formula_text = "Vb = K × C × beta × I × ao × W"

    K = st.number_input("Performance Factor (K)", value=0.0, format="%.5f")
    C = st.number_input("Flexibility Coefficient (C)", value=0.0, format="%.5f")
    beta = st.number_input("Soil Foundation Factor (beta)", value=0.0, format="%.5f")
    I = st.number_input("Importance Factor (I)", value=1.0, format="%.2f")
    ao = st.number_input("Zone Factor (ao)", value=0.0, format="%.5f")
    W = st.number_input("Seismic Weight W (kN)", value=0.0, format="%.2f")

    values = {"K": K, "C": C, "beta": beta, "I": I, "ao": ao, "W (kN)": W}

    if st.button("Calculate"):
        Vb = K * C * beta * I * ao * W
        result_text = f"Vb = {Vb:.4f} kN"
        numeric_result = {"Vb (kN)": Vb}

elif year in [2002, 2016]:
    formula_text = "Vb = (Z / 2) × (I / R) × (Sa/g) × W"

    Z = st.number_input("Seismic Zone Factor (Z)", value=0.0, format="%.3f")
    I = st.number_input("Importance Factor (I)", value=1.0, format="%.2f")
    R = st.number_input("Response Reduction Factor (R)", value=1.0, format="%.2f")
    Sa_by_g = st.number_input("Spectral Acceleration Ratio (Sa/g)", value=0.0, format="%.3f")
    W = st.number_input("Seismic Weight W (kN)", value=0.0, format="%.2f")

    values = {"Z": Z, "I": I, "R": R, "Sa/g": Sa_by_g, "W (kN)": W}

    if st.button("Calculate"):
        Vb = (Z / 2.0) * (I / R) * Sa_by_g * W
        result_text = f"Vb = {Vb:.4f} kN"
        numeric_result = {"Vb (kN)": Vb}

elif year == 2025:
    formula_text = "VBD,H = (Z × I × A_NH / R) × W   |   VBD,V = (Z × I × A_NV) × W"

    Z = st.number_input("Hazard Factor (Z)", value=0.0, format="%.3f")
    I = st.number_input("Importance Factor (I)", value=1.0, format="%.2f")
    R = st.number_input("Ductility Factor (R)", value=1.0, format="%.2f")
    A_NH = st.number_input("Horizontal Response Coefficient (A_NH)", value=0.0, format="%.4f")
    A_NV = st.number_input("Vertical Response Coefficient (A_NV)", value=0.0, format="%.4f")
    W = st.number_input("Seismic Weight W (kN)", value=0.0, format="%.2f")

    values = {"Z": Z, "I": I, "R": R, "A_NH": A_NH, "A_NV": A_NV, "W (kN)": W}

    if st.button("Calculate"):
        VBD_H = (Z * I * A_NH / R) * W
        VBD_V = (Z * I * A_NV) * W
        result_text = f"VBD,H = {VBD_H:.4f} kN   |   VBD,V = {VBD_V:.4f} kN"
        numeric_result = {"VBD,H (kN)": VBD_H, "VBD,V (kN)": VBD_V}

# ==============================
# DISPLAY
# ==============================
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
# BASE SHEAR DISTRIBUTION GRAPH
# ==============================
if numeric_result:
    st.divider()
    st.subheader("Base Shear Distribution (Storey-wise)")

    num_storeys = st.number_input("Number of Storeys", min_value=1, step=1)

    if st.button("Generate Distribution Graph"):
        total_shear = list(numeric_result.values())[0]

        storey_numbers = list(range(1, int(num_storeys) + 1))
        shear_distribution = [(i / num_storeys) * total_shear for i in storey_numbers]

        plt.figure()
        plt.bar(storey_numbers, shear_distribution)
        plt.xlabel("Storey Number")
        plt.ylabel("Shear (kN)")
        plt.title("Linear Base Shear Distribution")
        plt.tight_layout()

        graph_path = "base_shear_distribution.png"
        plt.savefig(graph_path, dpi=150)
        plt.close()

        st.image(graph_path, caption="Base Shear Distribution", use_column_width=True)
        st.session_state["graph_path"] = graph_path

# ==============================
# EXPORT TO EXCEL
# ==============================
if numeric_result:
    st.divider()
    st.subheader("Export Result")

    df = pd.DataFrame(list(values.items()), columns=["Parameter", "Value"])
    for k, v in numeric_result.items():
        df.loc[len(df)] = [k, v]

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Result")

    st.download_button(
        label="Download Result as Excel",
        data=excel_buffer.getvalue(),
        file_name="seismic_result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ==============================
# WATERMARK FUNCTION
# ==============================
from reportlab.pdfgen import canvas

def add_watermark(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 40)
    canvas.setFillColor(lightgrey)
    canvas.translate(300, 400)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, f"{OWNER_NAME} - {INSTITUTE_NAME}")
    canvas.restoreState()

# ==============================
# FULL PDF REPORT EXPORT
# ==============================
if numeric_result and "graph_path" in st.session_state:

    st.divider()
    st.subheader("Download Full Report (Inputs + Graph + Watermark)")

    if st.button("Download Full PDF Report"):

        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            onFirstPage=add_watermark,
            onLaterPages=add_watermark
        )

        styles = getSampleStyleSheet()
        story = []

        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        user_display = user_tag if user_tag.strip() != "" else "Not Provided"

        # Title
        story.append(Paragraph("<b>IS 1893 Seismic Calculation Report</b>", styles["Title"]))
        story.append(Spacer(1, 12))

        # Meta
        story.append(Paragraph(f"<b>Owner:</b> {OWNER_NAME}", styles["Normal"]))
        story.append(Paragraph(f"<b>Institute:</b> {INSTITUTE_NAME}", styles["Normal"]))
        story.append(Paragraph(f"<b>User:</b> {user_display}", styles["Normal"]))
        story.append(Paragraph(f"<b>Timestamp:</b> {timestamp}", styles["Normal"]))
        story.append(Spacer(1, 12))

        # Code info
        story.append(Paragraph(f"<b>Code Year:</b> {year}", styles["Normal"]))
        story.append(Paragraph(f"<b>Formula Used:</b> {formula_text}", styles["Normal"]))
        story.append(Spacer(1, 12))

        # Inputs
        story.append(Paragraph("<b>Entered Values:</b>", styles["Heading2"]))
        for k, v in values.items():
            story.append(Paragraph(f"{k} = {v}", styles["Normal"]))

        story.append(Spacer(1, 12))

        # Result
        story.append(Paragraph("<b>Result:</b>", styles["Heading2"]))
        for k, v in numeric_result.items():
            story.append(Paragraph(f"{k} = {v:.4f} kN", styles["Normal"]))

        story.append(Spacer(1, 12))

        # Graph
        story.append(Paragraph("<b>Base Shear Distribution:</b>", styles["Heading2"]))
        img = RLImage(st.session_state["graph_path"], width=4*inch, height=3*inch)
        story.append(img)

        doc.build(story)

        st.download_button(
            label="Download Full PDF Report",
            data=pdf_buffer.getvalue(),
            file_name="Seismic_Full_Report.pdf",
            mime="application/pdf"
        )

# ==============================
# LEGAL FOOTER
# ==============================
st.divider()
st.caption("© 2026 Vrushali Kamalakar. All rights reserved. Unauthorized copying, redistribution or commercial use is strictly prohibited.")
