# CRRT Calculation Learning Tool

A small Streamlit application for demonstrating basic, flow-based CRRT calculations.

## Important safety notice

This project is an educational prototype only. It is not a medical device and must not be used to prescribe, adjust, or monitor treatment. It does not provide clinical recommendations. Do not enter patient names, identifiers, or personal health information.

The app calculates:

- Effluent flow = dialysate flow + replacement fluid flow + net patient fluid removal.
- Unadjusted effluent dose = effluent flow / patient weight.
- An illustrative time-averaged estimate using the uptime percentage entered by the user.

The app does **not** apply a pre-dilution correction. If pre-dilution is selected, it displays a warning. It does not account for all clinical, device, modality, or treatment factors. A qualified clinical team must independently review any interpretation.

## Requirements

- Python 3.9 or newer
- pip

## Run locally

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Create a virtual environment:

   Windows:
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

6. Your browser should open the local app. If it does not, open the local address shown in the terminal.

## Upload this project to GitHub using the website

1. Sign in to GitHub.
2. Open your profile and select **Repositories**.
3. Select **New**.
4. Repository name: `crrt-prescription-learning-tool`.
5. Description: `Educational Streamlit prototype for basic CRRT flow calculations`.
6. Select **Public** if you want the code to be open source.
7. Select **Add a README file** only if you are creating a new empty repository and plan to upload the other files separately. If uploading this complete folder, it is simpler to leave it unchecked.
8. Select **Create repository**.
9. On the new repository page, select **Add file**, then **Upload files**.
10. Upload `app.py`, `requirements.txt`, `README.md`, and `LICENSE`.
11. Enter a commit message such as `Add initial educational CRRT calculator`.
12. Select **Commit changes**.

## Upload using Git commands

After creating an empty repository on GitHub, open a terminal in this folder and run:

```bash
git init
git add .
git commit -m "Add initial educational CRRT calculator"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/crrt-prescription-learning-tool.git
git push -u origin main
```

Replace `YOUR-GITHUB-USERNAME` with your GitHub username. If Git asks you to sign in, complete GitHub's sign-in flow.

## Suggested next steps

- Add automated tests for the arithmetic.
- Have the formula and assumptions reviewed by qualified CRRT clinicians.
- Document the intended educational use and limitations clearly.
- Invite feedback and contributions without presenting the project as clinically validated.
