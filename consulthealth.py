import streamlit as st

# -----------------------------------------------------------------------------
# 1. CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Clinical Support System",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. PROFESSIONAL STYLING (Seamless Panel Layout)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- LAYOUT FIXES (PANEL ALIGNMENT) --- */
    
    /* Remove the huge white gap at the top of the main area */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
    }
    
    /* Remove the gap at the top of the sidebar */
    [data-testid="stSidebarUserContent"] {
        padding-top: 2rem !important;
    }
    
    /* Force the main background to be a professional medical grey */
    [data-testid="stAppViewContainer"] {
        background-color: #f4f6f8;
    }
    
    /* Sidebar Styling - Distinct Panel */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #dce1e6;
    }
    
    /* --- TYPOGRAPHY --- */
    h1, h2, h3, h4, h5 {
        color: #1e293b !important; /* Dark Slate */
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    p, li, span, label, div {
        color: #475569 !important; /* Slate Grey */
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* --- COMPONENTS --- */
    
    /* Input Areas - White Panel look */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* Buttons - High Contrast & Visible Text */
    div.stButton > button {
        background-color: #2563eb !important; /* Royal Blue */
        color: #ffffff !important;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Cards */
    .clinical-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Alerts */
    .alert-box {
        background-color: #fef2f2;
        border: 1px solid #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    .alert-title {
        color: #991b1b !important;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    
    /* Info Box */
    .info-box {
        background-color: #eff6ff;
        border: 1px solid #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 6px;
    }
    
    /* Header Divider */
    hr {
        margin: 1.5rem 0;
        border-color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. KNOWLEDGE BASE
# -----------------------------------------------------------------------------
COMMON_SYMPTOM_GROUPS = {
    "fever": ["Infectious Pathology", "Systemic Inflammatory Response", "Autoimmune Etiology"],
    "chills": ["Bacteremia", "Hypothermia", "Acute Febrile Illness"],
    "cough": ["URI", "Bronchitis", "Pneumonia", "Reactive Airway Disease"],
    "sore throat": ["Pharyngitis", "Tonsillitis", "Epiglottitis"],
    "headache": ["Migraine", "Tension Cephalalgia", "Intracranial Hypertension", "Sinusitis"],
    "dizziness": ["Orthostatic Hypotension", "Vestibular Dysfunction", "Anemia", "Hypovolemia"],
    "fatigue": ["Anemia", "Endocrine Dysfunction", "Chronic Fatigue", "Post-Viral Sequelae"],
    "chest pain": ["Acute Coronary Syndrome", "Angina Pectoris", "GERD", "Costochondritis"],
    "shortness of breath": ["Dyspnea", "COPD Exacerbation", "Congestive Heart Failure", "Pneumonia"],
    "nausea": ["Gastroenteritis", "Gastritis", "Vestibular Neuritis"],
    "abdominal pain": ["Acute Abdomen", "Appendicitis", "Cholecystitis", "Diverticulitis"],
    "back pain": ["Lumbar Strain", "Herniated Nucleus Pulposus", "Pyelonephritis"],
    "joint pain": ["Arthralgia", "Osteoarthritis", "Rheumatoid Arthritis", "Septic Arthritis"],
    "rash": ["Dermatitis", "Urticaria", "Viral Exanthem", "Drug Eruption"],
    "blurred vision": ["Refractive Error", "Retinopathy", "Cataract"],
    "palpitations": ["Arrhythmia", "Sinus Tachycardia", "Thyrotoxicosis"],
    "swollen feet": ["Peripheral Edema", "Venous Insufficiency", "Deep Vein Thrombosis"],
    "insomnia": ["Psychophysiological Insomnia", "Sleep Apnea", "Restless Leg Syndrome"],
    "high blood pressure": ["Essential Hypertension", "Hypertensive Urgency", "Renal Artery Stenosis"],
}

EMERGENCY_SYMBOLS = {
    "chest pain": "High Priority: Rule out ACS/Cardiac Event",
    "shortness of breath": "High Priority: Assess Respiratory Status",
    "unconscious": "Emergency: Immediate Resuscitation Required",
    "slurred speech": "Emergency: Stroke Protocol Activation",
    "blood in vomit": "High Priority: GI Bleed Risk Assessment",
    "severe headache": "High Priority: Neurological Evaluation Required",
    "seizure": "Emergency: Seizure Management Protocol",
    "suicidal thoughts": "Emergency: Psychiatric Evaluation Required",
}

OTC_MED_GUIDE = {
    "fever": "Acetaminophen/Paracetamol. Monitor temperature.",
    "cough": "Antitussives or Expectorants. Hydration.",
    "headache": "Analgesics (NSAID or Acetaminophen).",
    "migraine": "Analgesics. Rest in low-light environment.",
    "nausea": "Antiemetics or clear fluids.",
    "heartburn": "Antacids or H2 Blockers.",
    "allergy": "Antihistamines (Diphenhydramine/Cetirizine).",
    "diarrhea": "Loperamide. Electrolyte hydration.",
    "muscle cramps": "Electrolyte replacement. Stretching.",
    "skin rash": "Topical Hydrocortisone. Antihistamine.",
}

# -----------------------------------------------------------------------------
# 4. ANALYSIS LOGIC
# -----------------------------------------------------------------------------
def analyze_symptoms(text):
    text = text.lower()
    detected = []
    potential_causes = set()
    emergency_msgs = []
    otc_recommendations = []
    
    for symptom, alert in EMERGENCY_SYMBOLS.items():
        if symptom in text:
            emergency_msgs.append(alert)
            
    for symptom, causes in COMMON_SYMPTOM_GROUPS.items():
        if symptom in text:
            detected.append(symptom)
            potential_causes.update(causes)
            
            otc = OTC_MED_GUIDE.get(symptom)
            if otc:
                otc_recommendations.append(f"<b>{symptom.title()}</b>: {otc}")
                
    if not detected and not emergency_msgs:
        return None, None, None, None
        
    return detected, sorted(list(potential_causes)), otc_recommendations, emergency_msgs

# -----------------------------------------------------------------------------
# 5. SIDEBAR LAYOUT
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### System Tools")
    st.markdown("Use this interface to analyze reported symptoms against the clinical database.")
    
    st.markdown("---")
    
    st.markdown("#### Database Version")
    st.caption("Standard Clinical Set v1.0")
    
    st.markdown("#### Mode")
    st.caption("Triage Assistance")
    
    st.markdown("---")
    st.caption("Note: This system provides algorithmic suggestions based on keyword matching.")

# -----------------------------------------------------------------------------
# 6. MAIN INTERFACE
# -----------------------------------------------------------------------------
# Creating a "Header" look manually since we removed default padding
st.markdown("""
<div style="background-color: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 2rem;">
    <h1 style="margin: 0; font-size: 1.8rem; color: #0f172a;">Clinical Decision Support System</h1>
    <p style="margin: 0.5rem 0 0 0; color: #64748b;">Symptom Triage & Differential Analysis</p>
</div>
""", unsafe_allow_html=True)

input_col, help_col = st.columns([2, 1])

with input_col:
    st.markdown("#### Clinical Notes / Symptoms")
    user_input = st.text_area(
        "Input",
        height=150,
        label_visibility="collapsed",
        placeholder="Enter patient symptoms here (e.g., severe headache, nausea, mild fever)..."
    )
    
    process_btn = st.button("Run Analysis")

with help_col:
    st.markdown("""
    <div class="clinical-card" style="padding: 1rem;">
        <div style="font-weight: 700; font-size: 0.8rem; text-transform: uppercase; color: #94a3b8; margin-bottom: 0.5rem;">Instructions</div>
        <div style="font-size: 0.9rem; line-height: 1.5;">
        • Enter primary symptoms separated by commas or in natural language.<br>
        • The system will identify clinical keywords.<br>
        • Critical keywords will trigger high-priority alerts.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. RESULTS DISPLAY
# -----------------------------------------------------------------------------
if process_btn:
    st.markdown("### Analysis Results")
    
    if user_input:
        detected_symptoms, causes, meds, emergencies = analyze_symptoms(user_input)

        if emergencies:
            for alert in emergencies:
                st.markdown(f"""
                <div class="alert-box">
                    <div class="alert-title">⚠️ High Priority Alert</div>
                    <div style="color: #b91c1c;">{alert}</div>
                </div>
                """, unsafe_allow_html=True)

        if detected_symptoms:
            grid_c1, grid_c2 = st.columns(2)
            
            with grid_c1:
                st.markdown("""
                <div class="clinical-card">
                    <div style="font-weight: 600; margin-bottom: 1rem;">Potential Etiology</div>
                """, unsafe_allow_html=True)
                
                if causes:
                    for cause in causes:
                        st.markdown(f"<div style='margin-bottom: 0.25rem; font-size: 0.95rem; border-bottom: 1px dashed #e2e8f0; padding-bottom: 0.25rem;'>• {cause}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='font-style: italic; color: #94a3b8;'>No specific match found.</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

            with grid_c2:
                st.markdown("""
                <div class="clinical-card">
                    <div style="font-weight: 600; margin-bottom: 1rem;">Therapeutic Suggestions</div>
                """, unsafe_allow_html=True)
                
                if meds:
                    for m in meds:
                        st.markdown(f"<div style='margin-bottom: 0.25rem; font-size: 0.95rem; border-bottom: 1px dashed #e2e8f0; padding-bottom: 0.25rem;'>• {m}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='font-style: italic; color: #94a3b8;'>No specific recommendations.</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

        elif not emergencies:
            st.markdown("""
            <div class="info-box">
                <div style="font-weight: 600; margin-bottom: 0.5rem; color: #1e40af;">No Keywords Detected</div>
                <div style="color: #1e3a8a;">The input text did not trigger any specific rules in the current database. Please verify the terminology.</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Awaiting input data to proceed with analysis.")
