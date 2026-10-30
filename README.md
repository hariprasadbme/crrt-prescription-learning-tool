# CRRT Therapy Flow Dashboard

Version 2.0 is an educational Streamlit prototype for visualizing simplified flow-based calculations across CVVH, CVVHD, and CVVHDF.

## Safety statement
**Not for clinical use.** This software is not a medical device, has not undergone clinical validation, and must not be used to prescribe, adjust, or monitor CRRT. It does not provide treatment recommendations. It is not a substitute for qualified clinical judgement, local protocols, device instructions, or measured clinical assessment. Do not enter patient identifiers or personal health information.

Published formulas inform the implementation. This is not equivalent to independent clinical validation. Automated software tests check arithmetic and input handling only; passing tests does not establish clinical safety or validity.

## Simplified modality formulas (mL/hr)
- **CVVH:** pre-filter replacement + post-filter replacement + net patient fluid removal.
- **CVVHD:** dialysate + net patient fluid removal.
- **CVVHDF:** dialysate + pre-filter replacement + post-filter replacement + net patient fluid removal.
- **Unadjusted effluent dose:** total effluent flow / entered weight (mL/kg/hr).
- **Plasma water flow estimate:** blood flow (mL/min) × 60 × (1 − haematocrit fraction).
- **Pre-dilution factor:** plasma water flow / (plasma water flow + pre-filter replacement flow).
- **Pre-dilution adjusted estimate:** unadjusted dose × pre-dilution factor.
- **Uptime-adjusted estimate:** unadjusted dose × uptime fraction.

The pre-dilution adjusted value and uptime-adjusted value are separate illustrative estimates. The app does not combine them into a claimed delivered biological dose. It does not calculate filtration fraction.

## Run locally
Python 3.9 or newer:
```bash
python -m venv .venv
```
Windows activation: `.venv\\Scripts\\activate`
macOS/Linux activation: `source .venv/bin/activate`

Install and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```
Run automated tests:
```bash
pytest -q
```

## Upload updated files to GitHub
1. Open `hariprasadbme/crrt-prescription-learning-tool`.
2. Choose **Add file** → **Upload files**.
3. Upload `app.py`, `crrt_calculations.py`, `requirements.txt`, `README.md`, and the `tests` folder with `test_crrt_calculations.py`.
4. If folder upload is unavailable, use **Add file** → **Create new file** and name it `tests/test_crrt_calculations.py`, then paste the test file.
5. Commit with message: `Upgrade dashboard with modality calculations and tests`.
6. Streamlit Community Cloud should redeploy after the GitHub commit. Check app logs if deployment fails.

## Limitations
- No treatment recommendations, dose targets, modality selection, or fluid-removal recommendations.
- The app does not determine whether actual, ideal, or adjusted body weight should be used. Follow local protocol.
- The pre-dilution factor is simplified and does not account for every circuit configuration, pre-blood-pump fluids, access recirculation, sieving or saturation coefficients, or device-specific calculations.
- No filtration fraction calculation is provided because conventions and required inputs can vary by circuit and device.
- It does not model filter performance, clotting, adsorption, interruptions, measured effluent solute concentrations, or biological delivered clearance.
- Uptime adjustment is a simple time-availability estimate, not measured clearance.
- Qualified clinical review is essential. Do not enter protected or identifying data.

## References
1. Passi NN, Kirwan CJ. *JICS Education: Continuous renal replacement therapy* (2026). https://journals.sagepub.com/doi/10.1177/17511437261483952
2. ISCCM Guidelines on Acute Kidney Injury and Renal Replacement Therapy (2022). https://pmc.ncbi.nlm.nih.gov/articles/PMC9989875/
3. Villa G, et al. *Methods for dose quantification in continuous renal replacement therapy: Toward a more precise approach* (2021). https://onlinelibrary.wiley.com/doi/10.1111/aor.13991
4. KDIGO AKI guideline (2012). https://kdigo.org/wp-content/uploads/2017/04/KDIGO-AKI-Guideline_Cass-2014.pdf

References are for further review. Their inclusion does not constitute endorsement or clinical validation. Check current guidance and local protocols before interpreting any clinical parameter.
