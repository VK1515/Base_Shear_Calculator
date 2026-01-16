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
import plotly.graph_objects as go


from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.colors import lightgrey
from reportlab.lib.units import inch

# ==============================
# OWNER DETAILS
# ==============================
OWNER_NAME = "Vrushali Kamalakar"
INSTITUTE_NAME = "VK"

# ==============================
# YEAR DESCRIPTIONS
# ==============================
YEAR_DESCRIPTIONS = {
    1962: "Foundation of seismic design. Introduced seismic coefficient ah.",
    1966: "Introduced flexibility coefficient C for building response.",
    1970: "Introduced soil–foundation factor β for soil interaction.",
    1975: "Added importance factor I and regional coefficient a₀.",
    1984: "Introduced performance factor K for ductility and framing.",
    2002: "Major shift to dynamic design using Z, R and Sa/g.",
    2016: "Refinement of 2002 provisions.",
    2025: "Separate horizontal and vertical seismic demands."
}

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="IS 1893 Seismic Calculator", layout="wide")

# ==============================
# UI WARNING
# ==============================
st.warning("Educational use only. Unauthorized copying or commercial use is prohibited.")

st.title("IS 1893 Seismic Base Shear Calculator (1962–2025)")

user_tag = st.text_input("User Name / ID (for report)", value="")

st.divider()

# ==============================
# TIMELINE VISUALIZATION PANEL
# ==============================
# ==============================


# ==============================
# CLEAR VERTICAL TIMELINE PANEL
# ==============================
st.subheader("Evolution Timeline of IS 1893")

timeline_data = [
    ("1962", "Foundation of seismic design\nIntroduced seismic coefficient ah", "#1f77b4"),
    ("1966", "Flexibility in building response\nIntroduced coefficient C", "#2ca02c"),
    ("1970", "Soil–structure interaction\nIntroduced soil factor β", "#ff7f0e"),
    ("1975", "Importance & regionality\nIntroduced I and a₀", "#d62728"),
    ("1984", "Performance & ductility\nIntroduced factor K", "#9467bd"),
    ("2002", "Dynamic design approach\nZ, R and Sa/g based design", "#8c564b"),
    ("2016", "Refinement of dynamic provisions", "#17becf"),
    ("2025", "Separate horizontal & vertical forces", "#e377c2"),
]

fig, ax = plt.subplots(figsize=(8, 6))

y_positions = list(range(len(timeline_data), 0, -1))

for (year, text, color), y in zip(timeline_data, y_positions):
    ax.text(
        0.1, y,
        f"{year}",
        fontsize=12,
        fontweight="bold",
        color="black",
        ha="right",
        va="center"
    )
    ax.text(
        0.15, y,
        text,
        fontsize=10,
        color="white",
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=color, edgecolor="black")
    )

# Vertical line
ax.plot([0.12, 0.12], [0.5, len(timeline_data) + 0.5], color="black", linewidth=2)

ax.set_xlim(0, 1)
ax.set_ylim(0.5, len(timeline_data) + 0.5)
ax.axis("off")

st.pyplot(fig)
plt.close(fig)


st.plotly_chart(fig, use_container_width=True)

st.caption("Hover over points to see description. Use the selector below to jump to a year.")
st.markdown("### Quick Jump to Year")

year = st.radio(
    "Select Code Year",
    [1962, 1966, 1970, 1975, 1984, 2002, 2016, 2025],
    horizontal=True
)

st.info(YEAR_DESCRIPTIONS[year])


# ==============================
# SELECT YEAR
# ==============================
year = st.selectbox("Select Code Year", [1962, 1966, 1970, 1975, 1984, 2002, 2016, 2025])
st.info(YEAR_DESCRIPTIONS[year])

# ==============================
# VARIABLES
# ==============================
formula_text = ""
values = {}
numeric_result = {}

# ==============================
# INPUT + CALCULATION
# ==============================
if year == 1962:
    formula_text = "F = ah × W"
    ah = st.number_input("ah", value=0.0)
    W = st.number_input("W (kN)", value=0.0)
    values = {"ah": ah, "W": W}
    if st.button("Calculate"):
        numeric_result = {"F (kN)": ah * W}

elif year == 1966:
    formula_text = "Vb = C × ah × W"
    C = st.number_input("C", value=0.0)
    ah = st.number_input("ah", value=0.0)
    W = st.number_input("W (kN)", value=0.0)
    values = {"C": C, "ah": ah, "W": W}
    if st.button("Calculate"):
        numeric_result = {"Vb (kN)": C * ah * W}

elif year == 1970:
    formula_text = "Vb = C × ah × β × W"
    C = st.number_input("C", value=0.0)
    ah = st.number_input("ah", value=0.0)
    beta = st.number_input("beta", value=0.0)
    W = st.number_input("W (kN)", value=0.0)
    values = {"C": C, "ah": ah, "beta": beta, "W": W}
    if st.button("Calculate"):
        numeric_result = {"Vb (kN)": C * ah * beta * W}

elif year == 1975:
    formula_text = "Vb = C × β × I × a₀ × W"
    C = st.number_input("C", value=0.0)
    beta = st.number_input("beta", value=0.0)
    I = st.number_input("I", value=1.0)
    ao = st.number_input("a₀", value=0.0)
    W = st.number_input("W (kN)", value=0.0)
    values = {"C": C, "beta": beta, "I": I, "ao": ao, "W": W}
    if st.button("Calculate"):
        numeric_result = {"Vb (kN)": C * beta * I * ao * W}

elif year == 1984:
    formula_text = "Vb = K × C × β × I × a₀ × W"
    K = st.number_input("K", value=0.0)
    C = st.number_input("C", value=0.0)
    beta = st.number_input("beta", value=0.0)
    I = st.number_input("I", value=1.0)
    ao = st.number_input("a₀", value=0.0)
    W = st.number_input("W (kN)", value=0.0)
    values = {"K": K, "C": C, "beta": beta, "I": I, "ao": ao, "W": W}
    if st.button("Calculate"):
        numeric_result = {"Vb (kN)": K * C * beta * I * ao * W}

elif year in [2002, 2016]:
    formula_text = "Vb = (Z/2) × (I/R) × (Sa/g) × W"
    Z = st.number_input("Z", value=0.0)
    I = st.number_input("I", value=1.0)
    R = st.number_input("R", value=1.0)
    Sa_g = st.number_input("Sa/g", value=0.0)
    W = st.number_input("W (kN)", value=0.0)
    values = {"Z": Z, "I": I, "R": R, "Sa/g": Sa_g, "W": W}
    if st.button("Calculate"):
        numeric_result = {"Vb (kN)": (Z/2) * (I/R) * Sa_g * W}

elif year == 2025:
    formula_text = "VBD,H = (Z × I × A_NH / R) × W ,  VBD,V = (Z × I × A_NV) × W"
    Z = st.number_input("Z", value=0.0)
    I = st.number_input("I", value=1.0)
    R = st.number_input("R", value=1.0)
    A_NH = st.number_input("A_NH", value=0.0)
    A_NV = st.number_input("A_NV", value=0.0)
    W = st.number_input("W (kN)", value=0.0)
    values = {"Z": Z, "I": I, "R": R, "A_NH": A_NH, "A_NV": A_NV, "W": W}
    if st.button("Calculate"):
        numeric_result = {
            "VBD,H (kN)": (Z * I * A_NH / R) * W,
            "VBD,V (kN)": (Z * I * A_NV) * W
        }

# ==============================
# DISPLAY
# ==============================
st.subheader("Formula Used")
st.code(formula_text)

st.subheader("Entered Values")
st.json(values)

st.subheader("Result")
st.json(numeric_result)

# ==============================
# BASE SHEAR DISTRIBUTION GRAPH (FIXED)
# ==============================
if numeric_result:
    st.subheader("Base Shear Distribution")

    storeys = st.number_input("Number of Storeys", min_value=1, step=1)

    if st.button("Generate Distribution"):
        total_shear = list(numeric_result.values())[0]
        storey_list = list(range(1, storeys+1))
        shear = [(i/storeys) * total_shear for i in storey_list]

        fig, ax = plt.subplots()
        ax.bar(storey_list, shear)
        ax.set_xlabel("Storey")
        ax.set_ylabel("Shear (kN)")
        ax.set_title("Linear Base Shear Distribution")

        st.pyplot(fig)
        plt.close(fig)

        # Save to memory for PDF
        img_buffer = BytesIO()
        fig2, ax2 = plt.subplots()
        ax2.bar(storey_list, shear)
        ax2.set_xlabel("Storey")
        ax2.set_ylabel("Shear (kN)")
        ax2.set_title("Linear Base Shear Distribution")
        fig2.savefig(img_buffer, format='png', dpi=150)
        plt.close(fig2)
        img_buffer.seek(0)
        st.session_state["graph_image"] = img_buffer

# ==============================
# FULL PDF EXPORT (FIXED)
# ==============================
if numeric_result and "graph_image" in st.session_state:
    st.subheader("Download Full PDF Report")

    if st.button("Generate PDF Report"):
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        user_display = user_tag if user_tag else "Not Provided"

        story.append(Paragraph("<b>IS 1893 Seismic Calculation Report</b>", styles["Title"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph(f"<b>Owner:</b> VK", styles["Normal"]))
        story.append(Paragraph(f"<b>User:</b> {user_display}", styles["Normal"]))
        story.append(Paragraph(f"<b>Timestamp:</b> {timestamp}", styles["Normal"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph(f"<b>Code Year:</b> {year}", styles["Normal"]))
        story.append(Paragraph(f"<b>Formula:</b> {formula_text}", styles["Normal"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("<b>Inputs:</b>", styles["Heading2"]))
        for k, v in values.items():
            story.append(Paragraph(f"{k} = {v}", styles["Normal"]))

        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>Results:</b>", styles["Heading2"]))
        for k, v in numeric_result.items():
            story.append(Paragraph(f"{k} = {v}", styles["Normal"]))

        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>Base Shear Distribution:</b>", styles["Heading2"]))

        img = RLImage(st.session_state["graph_image"], width=4*inch, height=3*inch)
        story.append(img)

        doc.build(story)

        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer.getvalue(),
            file_name="Seismic_Full_Report.pdf",
            mime="application/pdf"
        )

# ==============================
# FOOTER
# ==============================
st.divider()
st.caption("© 2026 Vrushali Kamalakar. All rights reserved. Unauthorized copying or commercial use is prohibited.")
