# 🩺 Health Consultation App

A comprehensive, professional-grade Streamlit application for initial health assessment. The app accepts free-text symptom descriptions and provides likely causes, OTC/home remedy guidance, emergency triage alerts, and holistic wellness tips.

## Features

### 🌐 Symptom Analyzer
- **100+ Symptom Database:** Recognizes and interprets symptoms from user input, covering a wide spectrum of common complaints.
- **Clinical Triage:** Identifies urgent and emergent symptoms, offering clear, actionable guidance for red-flag situations (e.g., chest pain, stroke signs).
- **OTC & Home Recommendations:** Suggests evidence-based over-the-counter measures and supportive home care for detected symptoms.
- **Personalized Wellness Guidance:** Delivers essential lifestyle recommendations for general health maintenance.

## How It Works

1. **Symptom Entry:**  
   User describes symptoms in free text (e.g., `"chest pain and sweating, cough and fever"`).

2. **Analysis:**  
   The system parses and identifies symptoms, fetches potential underlying causes, assesses for emergencies, and suggests suitable remedies.

3. **Output:**  
   - **Recognized Symptoms**
   - **Possible Causes**
   - **OTC/Home Care**
   - **Urgent Triage Alerts** (when necessary)
   - **Wellness Advice**

## Example

**Input:**  
`high fever and difficulty breathing`

**Output:**  
- **Symptoms detected:** high fever, difficulty breathing
- **Possible causes:** Infection (Flu, COVID-19, Pneumonia), Heat stroke, Autoimmune disorders, Asthma, COPD, Heart failure
- **Urgent Alert:**  
  - ⚠️ High fever over 104F (40C) – seek care now.
  - ⚠️ Severe breathing issue can be life-threatening. Seek urgent help!
- **OTC/Home Care:**  
  - Fever: Paracetamol as directed, hydration, monitor closely, seek medical attention.
- **Wellness Tips:**  
  Hydration, balanced diet, adequate sleep, stress management, physical activity.

## Emergency Alerts

For any life-threatening or red-flag symptoms, the app provides immediate, visible alerts and clear instructions for escalation.

## Technology Stack

- **Streamlit** for interactive web development
- **Python** (for backend logic and NLP symptom detection)
- Lightweight, secure—no personal data stored

## Deployment

1. Save the application code as `consulthealth.py`
2. In terminal, run:  
   ```
   streamlit run consulthealth.py
   ```
3. Access via local or remote browser depending on deployment settings.

## Customization/Extension

- **Symptom Database:** Extend or update `COMMON_SYMPTOM_GROUPS` as desired.
- **Triage Logic:** Adjust or add to `EMERGENCY_SYMBOLS`.
- **OTC Advice:** Expand `OTC_MED_GUIDE` for more targeted recommendations.

## Professional Disclaimer

This application is designed to support initial health assessment and triage. It adheres to clinical decision-support best practices, but final decisions and individualized clinical judgment remain the responsibility of the healthcare provider. Integrate into clinical workflow as per institutional policy.

> **Developed by Anshuman Sinha**
