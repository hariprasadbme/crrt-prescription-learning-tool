import streamlit as st
import pandas as pd
from crrt_calculations import calculate_crrt

st.set_page_config(page_title="CRRT Therapy Flow Dashboard", page_icon="🩺", layout="wide")
st.title("CRRT Therapy Flow Dashboard")
st.caption("Educational calculation and visualization prototype")
st.error("EDUCATIONAL USE ONLY. This is not a medical device and has not been clinically validated. Do not use it to prescribe, adjust, or monitor CRRT. It provides no treatment recommendations. Outputs require independent review by qualified clinicians against local protocols and device instructions. Do not enter patient identifiers or personal health information.")

with st.sidebar:
    st.header("Calculation setup")
    modality = st.selectbox("CRRT modality", ["CVVH", "CVVHD", "CVVHDF"])
    weight = st.number_input("Weight used for dose normalization (kg)", 1.0, 400.0, 70.0, 0.5)
    uptime = st.slider("Estimated machine uptime (%)", 0, 100, 95)
    duration = st.number_input("Assessment period (hours)", 1, 24, 24)
    st.divider()
    st.subheader("Circuit flow inputs")
    blood_flow = st.number_input("Blood flow (mL/min)", 0, 1000, 150, 10)
    hct = st.number_input("Haematocrit (%)", 0.0, 80.0, 30.0, 0.5)
    dialysate = st.number_input("Dialysate flow (mL/hr)", 0, 20000, 1000, 50) if modality in ("CVVHD", "CVVHDF") else 0
    pre = st.number_input("Pre-filter replacement flow (mL/hr)", 0, 20000, 500, 50) if modality in ("CVVH", "CVVHDF") else 0
    post = st.number_input("Post-filter replacement flow (mL/hr)", 0, 20000, 500, 50) if modality in ("CVVH", "CVVHDF") else 0
    net_uf = st.number_input("Net patient fluid removal (mL/hr)", 0, 5000, 100, 10)

try:
    r = calculate_crrt(modality, weight, dialysate, pre, post, net_uf, blood_flow, hct, uptime, duration)
except ValueError as e:
    st.warning(str(e))
    st.stop()

st.subheader(f"{modality} calculation summary")
st.caption("Flow-based estimates only. These values do not establish an appropriate prescription or confirm biological solute clearance.")
a, b, c, d = st.columns(4)
a.metric("Total effluent flow", f"{r['effluent_ml_hr']:,.0f} mL/hr")
b.metric("Unadjusted effluent dose", f"{r['unadjusted_dose_ml_kg_hr']:.2f} mL/kg/hr")
c.metric("Pre-dilution factor", f"{r['predilution_factor']:.3f}")
d.metric("Uptime-adjusted estimate", f"{r['uptime_adjusted_dose_ml_kg_hr']:.2f} mL/kg/hr")

left, right = st.columns([1.15, 1])
with left:
    st.subheader("Flow distribution")
    chart = pd.DataFrame({"Flow (mL/hr)": [r["dialysate_ml_hr"], r["pre_replacement_ml_hr"], r["post_replacement_ml_hr"], r["net_uf_ml_hr"]]}, index=["Dialysate", "Pre-filter replacement", "Post-filter replacement", "Net patient fluid removal"])
    st.bar_chart(chart, horizontal=True)
with right:
    st.subheader("Calculation details")
    rows = [
        ("Modality", modality), ("Weight used", f"{weight:.1f} kg"),
        ("Total replacement flow", f"{r['replacement_total_ml_hr']:,.0f} mL/hr"),
        ("Plasma water flow estimate", f"{r['plasma_water_flow_ml_hr']:,.0f} mL/hr"),
        ("Pre-dilution correction applied", "Yes" if r["predilution_applied"] else "No"),
        ("Estimated running time", f"{r['estimated_running_hours']:.1f} hours"),
        ("Estimated effluent volume", f"{r['estimated_effluent_volume_ml']:,.0f} mL"),
    ]
    st.table(pd.DataFrame(rows, columns=["Parameter", "Value"]))

if r["predilution_applied"]:
    st.info("The pre-dilution adjusted value applies a simplified dilution factor. It is not a measured delivered dose and does not account for every circuit or modality factor.")
else:
    st.info("No pre-dilution correction was applied because pre-filter replacement flow is zero.")

st.subheader("Export")
st.download_button("Download calculation summary (CSV)", pd.DataFrame([r]).to_csv(index=False).encode(), "crrt_educational_calculation.csv", "text/csv")

with st.expander("Formula notes"):
    st.markdown("""
    - **CVVH:** pre-filter replacement + post-filter replacement + net patient fluid removal.
    - **CVVHD:** dialysate + net patient fluid removal.
    - **CVVHDF:** dialysate + pre-filter replacement + post-filter replacement + net patient fluid removal.
    - **Unadjusted dose:** total effluent flow / entered weight.
    - **Plasma water flow estimate:** blood flow × 60 × (1 − haematocrit fraction).
    - **Pre-dilution factor:** plasma water flow / (plasma water flow + pre-filter replacement flow).
    - **Uptime-adjusted estimate:** unadjusted dose × uptime fraction. This is not measured delivered clearance.
    """)

st.subheader("Clinical and technical limitations")
st.markdown("""
- No treatment recommendations, dose targets, modality selection, or fluid-removal recommendations.
- The app does not determine whether actual, ideal, or adjusted body weight should be used. Follow local protocol.
- The pre-dilution factor is simplified and does not account for every circuit configuration, pre-blood-pump fluids, access recirculation, sieving or saturation coefficients, or device-specific calculations.
- No filtration fraction calculation is provided because conventions and required inputs can vary by circuit and device.
- It does not model filter performance, clotting, adsorption, interruptions, measured effluent solute concentrations, or biological delivered clearance.
- Uptime adjustment is a simple time-availability estimate, not measured clearance.
- Qualified clinical review is essential. Do not enter protected or identifying data.
""")
st.caption("Version 2.0 | Educational open-source prototype | Not for clinical decision-making")
