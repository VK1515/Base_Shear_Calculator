"""
IS 1893 Seismic Base Shear Calculator
Author: Vrushali Kamalakar
Copyright (c) 2026

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
AUTHOR_NAME = "Vrushali Kamalakar"
INSTITUTE_NAME = "VK Institute"

# ==============================
# SESSION STATE INIT (CRITICAL FIX)
# ==============================
if "numeric_result" not in st.session_state:
    st.session_state["numeric_result"] = {}

if "values" not in st.session_state:
    st.session_state["values"] = {}

if "graph_image" not in st.session_state:
    st.session_state["graph_image"] = None

# ==============================
# YEAR DESCRIPTIONS (SHORT, FROM INFOGRAPHICS)
# ==============================
YEAR_DESCRIPTIONS = {
    1962: {
        "summary": "Foundation of seismic design. Introduced seismic coefficient ah.",
        "variables": {
            "ah": "Seismic coefficient representing expected ground shaking intensity.",
            "W": "Total seismic weight of the building."
        }
    },
    1966: {
        "summary": "Introduced flexibility coefficient C for building response.",
        "variables": {
            "C": "Flexibility coefficient related to height and structural response.",
            "ah": "Seismic coefficient.",
            "W": "Total seismic weight of the building."
        }
    },
    1970: {
        "summary": "Introduced soil–foundation factor β for soil interaction.",
        "variables": {
            "C": "Flexibility coefficient.",
            "ah": "Seismic coefficient.",
            "beta": "Soil–foundation interaction factor.",
            "W": "Total seismic weight of the building."
        }
    },
    1975: {
        "summary": "Added importance factor I and regional coefficient a₀.",
        "variables": {
            "C": "Flexibility coefficient.",
            "beta": "Soil–foundation factor.",
            "I": "Importance factor (higher for hospitals, schools, etc.).",
            "ao": "Basic horizontal seismic coefficient.",
            "W": "Total seismic weight of the building."
        }
    },
    1984: {
        "summary": "Introduced performance factor K for ductility and framing.",
        "variables": {
            "K": "Performance factor accounting for ductility.",
            "C": "Flexibility coefficient.",
            "beta": "Soil–foundation factor.",
            "I": "Importance factor.",
            "ao": "Basic horizontal seismic coefficient.",
            "W": "Total seismic weight of the building."
        }
    },
    2002: {
        "summary": "Major shift to dynamic design using Z, R and Sa/g.",
        "variables": {
            "Z": "Seismic zone factor.",
            "I": "Importance factor.",
            "R": "Response reduction factor.",
            "Sa/g": "Normalized spectral acceleration.",
            "W": "Total seismic weight of the building."
        }
    },
    2016: {
        "summary": "Refinement of 2002 dynamic provisions.",
        "variables": {
            "Z": "Seismic zone factor.",
            "I": "Importance factor.",
            "R": "Response reduction factor.",
            "Sa/g": "Normalized spectral acceleration.",
            "W": "Total seismic weight of the building."
        }
    },
    2025: {
        "summary": "Separate horizontal and vertical seismic demands.",
        "variables": {
            "Z": "Hazard factor.",
            "I": "Importance factor.",
            "R": "Ductility factor.",
            "A_NH": "Normalized horizontal spectral acceleration.",
            "A_NV": "Normalized vertical spectral acceleration.",
            "W": "Total seismic weight of the building."
        }
    }
}

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="IS 1893 Seismic Calculator", layout="wide")

# ==============================
# UI HEADER
# ==============================
st.warning(
    "Educational use only. Unauthorized copying, redistribution or commercial use is strictly prohibited."
)

st.title("IS 1893 Seismic Base Shear Calculator (1962–2025)")
st.caption("Author: Vrushali Kamalakar | Enter W in kN. Results in kN.")

user_tag = st.text_input("User Name / ID (for report)", value="")

st.divider()

# ==============================
# CLEAR VERTICAL TIMELINE PANEL
# ==============================
st.subheader("Evolution Timeline of IS 1893")

timeline_data = [
    ("1962", "Foundation of seismic design\nIntroduced ah", "#1f77b4"),
    ("1966", "Flexibility in building response\nIntroduced C", "#2ca02c"),
    ("1970", "Soil–structure interaction\nIntroduced β", "#ff7f0e"),
    ("1975", "Importance & regionality\nIntroduced I and a₀", "#d62728"),
    ("1984", "Performance & ductility\nIntroduced K", "#9467bd"),
    ("2002", "Dynamic design approach\nZ, R and Sa/g based", "#8c564b"),
    ("2016", "Refinement of dynamic provisions", "#17becf"),
    ("2025", "Separate horizontal & vertical forces", "#e377c2"),
]

fig_tl, ax_tl = plt.subplots(figsize=(8, 6))
y_positions = list(range(len(timeline_data), 0, -1))

for (year_lbl, text, color), y in zip(timeline_data, y_positions):
    ax_tl.text(0.1, y, year_lbl, fontsize=12, fontweight="bold",
               color="black", ha="right", va="center")
    ax_tl.text(0.15, y, text, fontsize=10, color="white",
               ha="left", va="center",
               bbox=dict(boxstyle="round,pad=0.4", facecolor=color, edgecolor="black"))

ax_tl.plot([0.12, 0.12], [0.5, len(timeline_data) + 0.5], color="black", linewidth=2)
ax_tl.set_xlim(0, 1)
ax_tl.set_ylim(0.5, len(timeline_data) + 0.5)
ax_tl.axis("off")

st.pyplot(fig_tl)
plt.close(fig_tl)

st.divider()

# ==============================
# SELECT YEAR
# ==============================
year = st.radio(
    "Select Code Year",
    [1962, 1966, 1970, 1975, 1984, 2002, 2016, 2025],
    horizontal=True
)

st.info(YEAR_DESCRIPTIONS[year]["summary"])

# ==============================
# VARIABLES
# ==============================
formula_text = ""

# ==============================
# INPUT + CALCULATION (SESSION SAFE)
# ==============================
if year == 1962:
    formula_text = "F = ah × W"

    ah = st.number_input("Horizontal Seismic Coefficient (ah)",
                         help=YEAR_DESCRIPTIONS[1962]["variables"]["ah"],
                         value=0.0)
    W = st.number_input("Seismic Weight W (kN)",
                        help=YEAR_DESCRIPTIONS[1962]["variables"]["W"],
                        value=0.0)

    if st.button("Calculate"):
        F = ah * W
        st.session_state["numeric_result"] = {"F (kN)": F}
        st.session_state["values"] = {"ah": ah, "W (kN)": W}

elif year == 1966:
    formula_text = "Vb = C × ah × W"

    C = st.number_input("Flexibility Coefficient (C)",
                        help=YEAR_DESCRIPTIONS[1966]["variables"]["C"],
                        value=0.0)
    ah = st.number_input("Horizontal Seismic Coefficient (ah)",
                         help=YEAR_DESCRIPTIONS[1966]["variables"]["ah"],
                         value=0.0)
    W = st.number_input("Seismic Weight W (kN)",
                        help=YEAR_DESCRIPTIONS[1966]["variables"]["W"],
                        value=0.0)

    if st.button("Calculate"):
        Vb = C * ah * W
        st.session_state["numeric_result"] = {"Vb (kN)": Vb}
        st.session_state["values"] = {"C": C, "ah": ah, "W (kN)": W}

elif year == 1970:
    formula_text = "Vb = C × ah × β × W"

    C = st.number_input("Flexibility Coefficient (C)",
                        help=YEAR_DESCRIPTIONS[1970]["variables"]["C"],
                        value=0.0)
    ah = st.number_input("Horizontal Seismic Coefficient (ah)",
                         help=YEAR_DESCRIPTIONS[1970]["variables"]["ah"],
                         value=0.0)
    beta = st.number_input("Soil Foundation Factor (beta)",
                           help=YEAR_DESCRIPTIONS[1970]["variables"]["beta"],
                           value=0.0)
    W = st.number_input("Seismic Weight W (kN)",
                        help=YEAR_DESCRIPTIONS[1970]["variables"]["W"],
                        value=0.0)

    if st.button("Calculate"):
        Vb = C * ah * beta * W
        st.session_state["numeric_result"] = {"Vb (kN)": Vb}
        st.session_state["values"] = {"C": C, "ah": ah, "beta": beta, "W (kN)": W}

elif year == 1975:
    formula_text = "Vb = C × β × I × a₀ × W"

    C = st.number_input("Flexibility Coefficient (C)",
                        help=YEAR_DESCRIPTIONS[1975]["variables"]["C"],
                        value=0.0)
    beta = st.number_input("Soil Foundation Factor (beta)",
                           help=YEAR_DESCRIPTIONS[1975]["variables"]["beta"],
                           value=0.0)
    I = st.number_input("Importance Factor (I)",
                        help=YEAR_DESCRIPTIONS[1975]["variables"]["I"],
                        value=1.0)
    ao = st.number_input("Basic Horizontal Seismic Coefficient (ao)",
                         help=YEAR_DESCRIPTIONS[1975]["variables"]["ao"],
                         value=0.0)
    W = st.number_input("Seismic Weight W (kN)",
                        help=YEAR_DESCRIPTIONS[1975]["variables"]["W"],
                        value=0.0)

    if st.button("Calculate"):
        Vb = C * beta * I * ao * W
        st.session_state["numeric_result"] = {"Vb (kN)": Vb}
        st.session_state["values"] = {"C": C, "beta": beta, "I": I, "ao": ao, "W (kN)": W}

elif year == 1984:
    formula_text = "Vb = K × C × β × I × a₀ × W"

    K = st.number_input("Performance Factor (K)",
                        help=YEAR_DESCRIPTIONS[1984]["variables"]["K"],
                        value=0.0)
    C = st.number_input("Flexibility Coefficient (C)",
                        help=YEAR_DESCRIPTIONS[1984]["variables"]["C"],
                        value=0.0)
    beta = st.number_input("Soil Foundation Factor (beta)",
                           help=YEAR_DESCRIPTIONS[1984]["variables"]["beta"],
                           value=0.0)
    I = st.number_input("Importance Factor (I)",
                        help=YEAR_DESCRIPTIONS[1984]["variables"]["I"],
                        value=1.0)
    ao = st.number_input("Basic Horizontal Seismic Coefficient (ao)",
                         help=YEAR_DESCRIPTIONS[1984]["variables"]["ao"],
                         value=0.0)
    W = st.number_input("Seismic Weight W (kN)",
                        help=YEAR_DESCRIPTIONS[1984]["variables"]["W"],
                        value=0.0)

    if st.button("Calculate"):
        Vb = K * C * beta * I * ao * W
        st.session_state["numeric_result"] = {"Vb (kN)": Vb}
        st.session_state["values"] = {"K": K, "C": C, "beta": beta, "I": I, "ao": ao, "W (kN)": W}

elif year in [2002, 2016]:
    formula_text = "Vb = (Z / 2) × (I / R) × (Sa/g) × W"

    Z = st.number_input("Seismic Zone Factor (Z)",
                        help=YEAR_DESCRIPTIONS[year]["variables"]["Z"],
                        value=0.0)
    I = st.number_input("Importance Factor (I)",
                        help=YEAR_DESCRIPTIONS[year]["variables"]["I"],
                        value=1.0)
    R = st.number_input("Response Reduction Factor (R)",
                        help=YEAR_DESCRIPTIONS[year]["variables"]["R"],
                        value=1.0)
    Sa_g = st.number_input("Spectral Acceleration Ratio (Sa/g)",
                           help=YEAR_DESCRIPTIONS[year]["variables"]["Sa/g"],
                           value=0.0)
    W = st.number_input("Seismic Weight W (kN)",
                        help=YEAR_DESCRIPTIONS[year]["variables"]["W"],
                        value=0.0)

    if st.button("Calculate"):
        Vb = (Z / 2.0) * (I / R) * Sa_g * W
        st.session_state["numeric_result"] = {"Vb (kN)": Vb}
        st.session_state["values"] = {"Z": Z, "I": I, "R": R, "Sa/g": Sa_g, "W (kN)": W}

elif year == 2025:
    formula_text = "VBD,H = (Z × I × A_NH / R) × W   |   VBD,V = (Z × I × A_NV) × W"

    Z = st.number_input("Hazard Factor (Z)",
                        help=YEAR_DESCRIPTIONS[2025]["variables"]["Z"],
                        value=0.0)
    I = st.number_input("Importance Factor (I)",
                        help=YEAR_DESCRIPTIONS[2025]["variables"]["I"],
                        value=1.0)
    R = st.number_input("Ductility Factor (R)",
                        help=YEAR_DESCRIPTIONS[2025]["variables"]["R"],
                        value=1.0)
    A_NH = st.number_input("Horizontal Response Coefficient (A_NH)",
                           help=YEAR_DESCRIPTIONS[2025]["variables"]["A_NH"],
                           value=0.0)
    A_NV = st.number_input("Vertical Response Coefficient (A_NV)",
                           help=YEAR_DESCRIPTIONS[2025]["variables"]["A_NV"],
                           value=0.0)
    W = st.number_input("Seismic Weight W (kN)",
                        help=YEAR_DESCRIPTIONS[2025]["variables"]["W"],
                        value=0.0)

    if st.button("Calculate"):
        VBD_H = (Z * I * A_NH / R) * W
        VBD_V = (Z * I * A_NV) * W
        st.session_state["numeric_result"] = {
            "VBD,H (kN)": VBD_H,
            "VBD,V (kN)": VBD_V
        }
        st.session_state["values"] = {
            "Z": Z, "I": I, "R": R, "A_NH": A_NH, "A_NV": A_NV, "W (kN)": W
        }

# ==============================
# DISPLAY
# ==============================
st.subheader("Formula Used")
st.code(formula_text)

st.subheader("Entered Values")
st.write(st.session_state["values"])

st.subheader("Result")
st.write(st.session_state["numeric_result"])

# ==============================
# BASE SHEAR DISTRIBUTION GRAPH (FIXED)
# ==============================
if st.session_state["numeric_result"]:
    st.subheader("Base Shear Distribution (Storey-wise)")

    storeys = st.number_input("Number of Storeys", min_value=1, step=1)

    if st.button("Generate Distribution Graph"):
        total_shear = list(st.session_state["numeric_result"].values())[0]
        storey_list = list(range(1, storeys + 1))
        shear = [(i / storeys) * total_shear for i in storey_list]

        fig, ax = plt.subplots()
        ax.bar(storey_list, shear)
        ax.set_xlabel("Storey")
        ax.set_ylabel("Shear (kN)")
        ax.set_title("Linear Base Shear Distribution")

        st.pyplot(fig)
        plt.close(fig)

        # Save graph to memory for PDF
        img_buffer = BytesIO()
        fig2, ax2 = plt.subplots()
        ax2.bar(storey_list, shear)
        ax2.set_xlabel("Storey")
        ax2.set_ylabel("Shear (kN)")
        ax2.set_title("Linear Base Shear Distribution")
        fig2.savefig(img_buffer, format="png", dpi=150)
        plt.close(fig2)
        img_buffer.seek(0)
        st.session_state["graph_image"] = img_buffer

# ==============================
# EXPORT TO EXCEL
# ==============================
if st.session_state["numeric_result"]:
    st.subheader("Export Result (Excel)")

    df = pd.DataFrame(list(st.session_state["values"].items()), columns=["Parameter", "Value"])
    for k, v in st.session_state["numeric_result"].items():
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
def add_watermark(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 36)
    canvas.setFillColor(lightgrey)
    canvas.translate(300, 400)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, f"{AUTHOR_NAME} - {INSTITUTE_NAME}")
    canvas.restoreState()

# ==============================
# FULL PDF EXPORT (FIXED)
# ==============================
if st.session_state["numeric_result"] and st.session_state["graph_image"] is not None:
    st.subheader("Download Full PDF Report")

    if st.button("Generate PDF Report"):
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

        story.append(Paragraph("<b>IS 1893 Seismic Calculation Report</b>", styles["Title"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph(f"<b>Author:</b> {AUTHOR_NAME}", styles["Normal"]))
        story.append(Paragraph(f"<b>Institute:</b> {INSTITUTE_NAME}", styles["Normal"]))
        story.append(Paragraph(f"<b>User:</b> {user_display}", styles["Normal"]))
        story.append(Paragraph(f"<b>Timestamp:</b> {timestamp}", styles["Normal"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph(f"<b>Code Year:</b> {year}", styles["Normal"]))
        story.append(Paragraph(f"<b>Formula Used:</b> {formula_text}", styles["Normal"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("<b>Entered Values:</b>", styles["Heading2"]))
        for k, v in st.session_state["values"].items():
            story.append(Paragraph(f"{k} = {v}", styles["Normal"]))

        story.append(Spacer(1, 12))

        story.append(Paragraph("<b>Result:</b>", styles["Heading2"]))
        for k, v in st.session_state["numeric_result"].items():
            story.append(Paragraph(f"{k} = {v:.4f} kN", styles["Normal"]))

        story.append(Spacer(1, 12))

        story.append(Paragraph("<b>Base Shear Distribution:</b>", styles["Heading2"]))
        img = RLImage(st.session_state["graph_image"], width=4 * inch, height=3 * inch)
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
st.caption("© 2026 Vrushali Kamalakar. All rights reserved. Unauthorized copying, redistribution or commercial use is strictly prohibited.")
