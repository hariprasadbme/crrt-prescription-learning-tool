import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CRRT Calculation Learning Tool", page_icon="🩺", layout="centered")

st.title("CRRT Calculation Learning Tool")
st.caption("Educational prototype for understanding basic CRRT flow calculations")

st.warning(
    "EDUCATIONAL USE ONLY. This tool is not a medical device and must not be used "
    "to prescribe, adjust, or monitor treatment. It does not replace clinical "
    "judgement, local protocols, device instructions, or review by a qualified "
    "nephrology and critical care team. Do not enter patient names, identifiers, "
    "or other personal health information."
)

st.subheader("1. Enter calculation inputs")

col1, col2 = st.columns(2)
with col1:
    weight_kg = st.number_input(
        "Patient weight (kg)", min_value=1.0, max_value=500.0,
        value=70.0, step=0.5
    )
    dialysate_ml_hr = st.number_input(
        "Dialysate flow (mL/hr)", min_value=0, max_value=20000,
        value=1000, step=50
    )
with col2:
    replacement_ml_hr = st.number_input(
        "Replacement fluid flow (mL/hr)", min_value=0, max_value=20000,
        value=1000, step=50
    )
    net_uf_ml_hr = st.number_input(
        "Net patient fluid removal (mL/hr)", min_value=0, max_value=5000,
        value=100, step=10
    )

st.subheader("2. Treatment time")
uptime_pct = st.slider(
    "Estimated machine uptime (%)", min_value=0, max_value=100, value=95,
    help="For learning only. This estimates the effect of downtime on the time-averaged effluent rate."
)
hours = st.number_input(
    "Elapsed period (hours)", min_value=1, max_value=24, value=24, step=1
)

st.subheader("3. Calculation assumptions")
predilution = st.checkbox(
    "Some or all replacement fluid is delivered pre-filter",
    value=False
)
if predilution:
    st.info(
        "This prototype does not apply a pre-dilution correction. The displayed "
        "effluent dose is an unadjusted calculation and may overstate the "
        "dose-equivalent clearance in pre-dilution settings."
    )

st.caption(
    "Formula used: effluent flow = dialysate flow + replacement fluid flow "
    "+ net patient fluid removal. Effluent dose = effluent flow ÷ weight."
)

if st.button("Calculate", type="primary", use_container_width=True):
    if weight_kg <= 0:
        st.error("Weight must be greater than zero.")
        st.stop()

    effluent_flow = dialysate_ml_hr + replacement_ml_hr + net_uf_ml_hr
    effluent_dose = effluent_flow / weight_kg
    effective_hours = hours * (uptime_pct / 100)
    period_effluent_ml = effluent_flow * effective_hours
    time_averaged_dose = effluent_dose * (uptime_pct / 100)

    st.subheader("Calculation results")
    c1, c2 = st.columns(2)
    c1.metric("Effluent flow", f"{effluent_flow:,.0f} mL/hr")
    c2.metric("Unadjusted effluent dose", f"{effluent_dose:.2f} mL/kg/hr")
    c3, c4 = st.columns(2)
    c3.metric("Estimated time-averaged dose", f"{time_averaged_dose:.2f} mL/kg/hr")
    c4.metric("Estimated effluent over period", f"{period_effluent_ml:,.0f} mL")

    st.write(
        f"At {uptime_pct}% uptime over {hours} hours, the estimated machine "
        f"running time is {effective_hours:.1f} hours."
    )

    if predilution:
        st.warning(
            "Pre-dilution is selected. No correction has been applied, so do "
            "not interpret the unadjusted dose as an adjusted delivered dose."
        )

    result = {
        "calculation_timestamp": datetime.now().isoformat(timespec="seconds"),
        "weight_kg": weight_kg,
        "dialysate_flow_ml_hr": dialysate_ml_hr,
        "replacement_flow_ml_hr": replacement_ml_hr,
        "net_patient_fluid_removal_ml_hr": net_uf_ml_hr,
        "machine_uptime_percent": uptime_pct,
        "elapsed_period_hours": hours,
        "pre_dilution_selected": predilution,
        "effluent_flow_ml_hr": effluent_flow,
        "unadjusted_effluent_dose_ml_kg_hr": round(effluent_dose, 3),
        "estimated_time_averaged_dose_ml_kg_hr": round(time_averaged_dose, 3),
        "estimated_effluent_over_period_ml": round(period_effluent_ml, 1),
    }
    csv = pd.DataFrame([result]).to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download calculation summary (CSV)",
        data=csv,
        file_name="crrt_learning_calculation.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()
st.subheader("Important limitations")
st.markdown(
    """
    - This is a learning demonstration, not a validated clinical calculator.
    - It does not recommend a CRRT dose, fluid removal rate, modality, or treatment setting.
    - It does not account for access recirculation, filter performance, clotting,
      fluid composition, anticoagulation, interruptions beyond the uptime estimate,
      or all modality-specific and dilution-related effects.
    - The calculation is an unadjusted flow-based estimate. Clinical interpretation
      requires qualified review and local protocol.
    - Validate all calculations independently before any educational or research use.
    """
)
st.caption("Open-source learning project. Use at your own risk; not for clinical care.")
