import streamlit as st

# 100+ symptom database (keyword: [suggested causes])
COMMON_SYMPTOM_GROUPS = {
    "fever": ["Infection (e.g. Flu, COVID-19, Malaria, Typhoid)", "Heat stroke", "Autoimmune disorders"],
    "chills": ["Infection", "Cold exposure", "Sepsis"],
    "cough": ["Common cold", "COVID-19", "Asthma", "Bronchitis", "Allergy", "Pneumonia"],
    "sore throat": ["Pharyngitis", "Tonsillitis", "Allergy", "Viral infection"],
    "runny nose": ["Common cold", "Allergic rhinitis", "Sinusitis"],
    "stuffy nose": ["Sinusitis", "Allergic rhinitis", "Common cold"],
    "headache": ["Migraine", "Tension headache", "Sinusitis", "Dehydration", "Eye strain"],
    "migraine": ["Migraine disorder", "Food triggers", "Stress"],
    "dizziness": ["Low blood pressure", "Vertigo", "Anemia", "Dehydration", "Inner ear infection"],
    "lightheadedness": ["Low blood sugar", "Dehydration", "Low blood pressure"],
    "fatigue": ["Anemia", "Hypothyroid", "Depression", "Chronic fatigue syndrome", "Sleep deprivation"],
    "weakness": ["Anemia", "Muscle fatigue", "Infection", "Electrolyte imbalance"],
    "shortness of breath": ["Asthma", "COPD", "Heart failure", "Pneumonia", "Anxiety"],
    "chest pain": ["Heart attack", "Angina", "Gastric reflux", "Anxiety", "Muscle strain"],
    "palpitations": ["Anxiety", "Arrhythmia", "Caffeine", "Hyperthyroid"],
    "fainting": ["Low blood pressure", "Heart problem", "Vasovagal syncope"],
    "sweating": ["Fever", "Anxiety", "Hypoglycemia"],
    "nausea": ["Gastroenteritis", "Pregnancy", "Migraine", "Food poisoning", "Medication side-effect"],
    "vomiting": ["Gastroenteritis", "Migraine", "Motion sickness", "Food poisoning"],
    "diarrhea": ["Infection", "Food intolerance", "IBS", "Food poisoning"],
    "constipation": ["Low fiber diet", "Dehydration", "IBS", "Hypothyroid"],
    "abdominal pain": ["Indigestion", "Gastritis", "Gallstones", "Appendicitis", "Constipation"],
    "stomach pain": ["Indigestion", "Gastritis", "Peptic ulcer", "Intestinal infection"],
    "bloated": ["Indigestion", "IBS", "Food intolerance"],
    "gas": ["Indigestion", "Lactose intolerance", "IBS"],
    "heartburn": ["GERD", "Stomach ulcer", "Hiatus hernia"],
    "loss of appetite": ["Infection", "Depression", "Liver disease"],
    "weight loss": ["Hyperthyroid", "Diabetes", "Cancer", "Chronic infection"],
    "weight gain": ["Hypothyroid", "Overeating", "Fluid retention"],
    "back pain": ["Muscle strain", "Slip disc", "Arthritis", "Kidney stone"],
    "neck pain": ["Muscle strain", "Spondylosis"],
    "joint pain": ["Arthritis", "Injury", "Infection", "Bursitis"],
    "swollen joints": ["Arthritis", "Infection", "Gout"],
    "muscle cramps": ["Electrolyte imbalance", "Dehydration", "Overuse"],
    "tingling": ["Nerve compression", "Vitamin deficiency", "Diabetes neuropathy"],
    "numbness": ["Nerve compression", "Stroke", "Diabetes neuropathy"],
    "rash": ["Allergy", "Viral infection", "Eczema", "Psoriasis"],
    "itchy skin": ["Allergy", "Eczema", "Fungal infection"],
    "dry skin": ["Dehydration", "Eczema", "Hypothyroid"],
    "red eyes": ["Conjunctivitis", "Allergy", "Infection"],
    "watery eyes": ["Allergy", "Viral infection", "Irritation"],
    "blurred vision": ["Glasses needed", "Diabetes", "Cataract", "Eye infection"],
    "eye pain": ["Infection", "Glaucoma", "Eye strain"],
    "ear pain": ["Ear infection", "Ear wax", "Injury"],
    "hearing loss": ["Wax impaction", "Ear infection", "Age-related loss"],
    "ringing in ears": ["Tinnitus", "Noise exposure", "Ear infection"],
    "tooth pain": ["Cavity", "Gum disease", "Infection"],
    "bleeding gums": ["Gum disease", "VIT C deficiency", "Improper brushing"],
    "mouth ulcers": ["Stress", "Trauma", "Vitamin deficiency", "Viral infection"],
    "sore tongue": ["Trauma", "Burn", "Vitamin deficiency"],
    "thirst": ["Dehydration", "Diabetes", "High salt intake"],
    "frequent urination": ["Diabetes", "UTI", "Pregnancy"],
    "burning urination": ["UTI", "STD", "Dehydration"],
    "blood in urine": ["UTI", "Stone", "Kidney infection"],
    "urinary incontinence": ["Old age", "Nerve disease", "UTI"],
    "missed period": ["Pregnancy", "PCOS", "Stress", "Thyroid"],
    "heavy periods": ["Fibroids", "Hormonal imbalance"],
    "painful periods": ["Dysmenorrhea", "Endometriosis"],
    "erectile dysfunction": ["Vascular disease", "Diabetes", "Anxiety"],
    "decreased libido": ["Depression", "Hormonal", "Relationship issues"],
    "sweats at night": ["Tuberculosis", "Cancers", "Menopause"],
    "hot flashes": ["Menopause", "Hormonal imbalance"],
    "cold hands": ["Poor circulation", "Raynaud's"],
    "swollen feet": ["Heart failure", "Kidney disease", "Injury"],
    "difficulty swallowing": ["Throat infection", "GERD", "Oesophageal growth"],
    "hoarseness": ["Laryngitis", "Vocal strain", "Smoking"],
    "memory loss": ["Dementia", "Depression", "Head injury", "Hypothyroid"],
    "confusion": ["Low sodium", "Infection", "Stroke", "Dehydration"],
    "anxiety": ["Generalized Anxiety Disorder", "Caffeine", "Thyroid disease"],
    "depression": ["Major depression", "Bipolar disorder", "Thyroid", "Life stress"],
    "insomnia": ["Anxiety", "Caffeine", "Depression", "Chronic pain"],
    "sleepiness": ["Sleep apnea", "Narcolepsy", "Sedative medication"],
    "bad breath": ["Oral hygiene", "Dental caries", "Sinusitis"],
    "snoring": ["Nasal blockage", "Obesity", "Sleep apnea"],
    "night sweats": ["TB", "Infection", "Cancer", "Menopause"],
    "hair loss": ["Alopecia", "Thyroid", "Stress", "Iron deficiency"],
    "bruising": ["Platelet disorder", "Blood thinner drugs", "Injury"],
    "nosebleed": ["Dry air", "Injury", "Nose picking", "Platelet disorder"],
    "yellow skin": ["Jaundice", "Liver disease", "Hemolysis"],
    "pale skin": ["Anemia", "Shock", "Blood loss"],
    "purple spots": ["Purpura", "Bleeding disorder", "Infection"],
    "leg swelling": ["Heart failure", "Varicose veins", "Injury"],
    "lump": ["Benign tumor", "Cancer", "Infection"],
    "weight change": ["Diet", "Thyroid", "Diabetes"],
    "loss of smell": ["COVID-19", "Sinus infection"],
    "loss of taste": ["COVID-19", "Mouth infection", "Zinc deficiency"],
    "difficulty breathing": ["Asthma", "COPD", "Heart failure", "Pneumonia"],
    "wheezing": ["Asthma", "Bronchitis", "Allergy"],
    "joint stiffness": ["Osteoarthritis", "RA", "Injury"],
    "abdominal mass": ["Hernia", "Tumor", "Cyst"],
    "change in bowel habits": ["Colon cancer", "IBS", "Infection"],
    "lumps in breast": ["Benign cyst", "Breast cancer", "Hormonal changes"],
    "nipple discharge": ["Hormonal", "Infection", "Tumor"],
    "hiccups": ["Gastric distension", "Neurological", "Liver disease"],
    "difficulty walking": ["Stroke", "Ataxia", "Muscle weakness"],
    "balance problems": ["Vertigo", "Ear infection", "Neuropathy"],
    "loss of coordination": ["Cerebellar disease", "Stroke", "Medication side effect"],
    "slurred speech": ["Stroke", "Alcohol", "Muscle disease"],
    "vision loss": ["Glaucoma", "Retinal detachment", "Optic neuritis"],
    "difficulty concentrating": ["ADHD", "Anxiety", "Lack of sleep", "Stress"],
    "muscle weakness": ["Nerve injury", "Polio", "Muscle disease"],
    "rapid heartbeat": ["Arrhythmia", "Anxiety", "Thyroid disease"],
}

# Emergency alert rules (symptom keyword: message)
EMERGENCY_SYMBOLS = {
    "chest pain": "⚠️ Chest pain can indicate heart attack. Call emergency services immediately!",
    "severe headache": "⚠️ Sudden severe headache may signal brain bleed. Urgent care needed!",
    "shortness of breath": "⚠️ Severe breathing difficulty: Call emergency or visit ER.",
    "weakness on one side": "⚠️ Possible stroke detected. Call emergency services now!",
    "unconscious": "⚠️ Unconsciousness is a medical emergency. Seek immediate help!",
    "slurred speech": "⚠️ Sudden slurred speech: Possible stroke – call emergency!",
    "blood in stool": "⚠️ Blood in stool: Seek urgent medical evaluation.",
    "blood in vomit": "⚠️ Vomiting blood: Go to the ER now.",
    "blood in urine": "⚠️ Blood in urine may be kidney/urinary issue. See a doctor soon.",
    "loss of vision": "⚠️ Sudden vision loss: See a doctor now.",
    "seizure": "⚠️ Seizure/fits: Seek urgent medical attention.",
    "suicidal thoughts": "⚠️ Mental health emergency. Seek urgent professional help or helpline.",
    "high fever": "⚠️ High fever over 104F (40C) – seek care now.",
    "difficulty breathing": "⚠️ Severe breathing issue can be life-threatening. Seek urgent help!",
}

# OTC advice
OTC_MED_GUIDE = {
    "fever": "Paracetamol (acetaminophen) as directed. Drink fluids. If high or persistent, seek doctor.",
    "cough": "Steam inhalation, honey, lozenges. See doctor if severe, persistent, or with blood.",
    "runny nose": "Decongestants, saline nasal spray, rest.",
    "sore throat": "Warm fluids, saltwater gargle, lozenges.",
    "headache": "Paracetamol, ibuprofen if not allergic. Avoid screens, hydrate.",
    "migraine": "Rest in a dark room, paracetamol, use migraine prescription if diagnosed.",
    "back pain": "Rest, gentle stretching, hot pack, over-the-counter pain relief.",
    "muscle cramps": "Stretch, hydrate, electrolyte solutions.",
    "heartburn": "Antacids after meals, avoid spicy/fatty food.",
    "allergy": "Antihistamines (cetirizine, loratadine), avoid triggers.",
    "constipation": "Increase fiber, drink water, OTC laxatives.",
    "diarrhea": "ORS (oral rehydration), bananas, rice. Seek care if blood or dehydration.",
    "itchy skin": "Moisturizer, anti-itch creams, antihistamine for allergy.",
    "dry skin": "Fragrance-free moisturizer. Use mild soap.",
    "rash": "Apply calamine, avoid scratching, keep clean.",
    "ear pain": "Warm compress. OTC pain medication.",
    "mouth ulcers": "Gargle, topical analgesic gels.",
    "tooth pain": "Painkillers, clove oil. See dentist.",
    "stomach pain": "Antacids, avoid spicy/fatty food.",
    "indigestion": "Antacid, small frequent meals.",
    "nausea": "Ginger, rest, avoid oily food.",
    "vomiting": "Hydrate with small sips. Seek care if persistent.",
    "bloating": "Peppermint, gentle walk, antacids.",
    "gas": "OTC anti-gas meds, avoid carbonated drinks.",
    "nasal congestion": "Steam inhalation, saline drops.",
    "dizziness": "Sit/lie down, fluids, avoid sudden standing.",
    "minor swelling": "Rest, ice, elevate, compression.",
    "sneezing": "Antihistamine, avoid allergens.",
    "bruising": "Ice packs, elevate area.",
    "bad breath": "Brush, floss, mouthwash.",
    # ... extend as needed
}

WELLNESS_TIPS = (
    "• Drink 2–3 liters of water daily.\n"
    "• Get 7–8 hours of sleep every night.\n"
    "• Eat a balanced diet with fruits, vegetables, proteins, and whole grains.\n"
    "• Exercise at least 150 minutes per week.\n"
    "• Manage stress with mindfulness or hobbies.\n"
    "• Foster social connections.\n"
    "• Avoid smoking and limit alcohol.\n"
)

st.title("🩺 Health Consultation")
st.markdown(
    """
    **Describe your symptoms below** (write multiple symptoms separated with commas or in a sentence),<br>
    and get basic health advice, likely causes, OTC suggestions, and triage guidance.<br>
    <br>
    :red[**Important:**] This tool does *not* diagnose, nor replace professional medical care.
    If in doubt or if symptoms worsen, **consult a healthcare provider**.
    """,
    unsafe_allow_html=True
)

user_input = st.text_area(
    "Describe your symptoms:",
    placeholder="e.g. chest pain and sweating, cough and fever, joint pain"
)

def analyze_symptoms(text):
    text = text.lower()
    detected = []
    potential_causes = set()
    emergency_msgs = []
    otc_recommendations = []
    # Detect emergency symptoms first (promptly display those)
    for symptom, alert in EMERGENCY_SYMBOLS.items():
        if symptom in text:
            emergency_msgs.append(alert)
    # Detect recognized symptoms (for cause/OTC/advice)
    for symptom, causes in COMMON_SYMPTOM_GROUPS.items():
        if symptom in text:
            detected.append(symptom)
            for c in causes:
                potential_causes.add(c)
            # OTC med suggestion if available
            otc = OTC_MED_GUIDE.get(symptom)
            if otc:
                otc_recommendations.append(f"{symptom.title()}: {otc}")
    if not detected:
        return None, None, None, emergency_msgs
    return detected, sorted(set(potential_causes)), otc_recommendations, emergency_msgs

if st.button("Analyze Symptoms"):
    detected_symptoms, causes, meds, emergencies = analyze_symptoms(user_input)
    if emergencies:
        st.error("\n\n".join(emergencies))
    if detected_symptoms:
        st.markdown("### 🔍 Symptoms detected:")
        st.write(", ".join(sorted(detected_symptoms)))
        st.markdown("### Possible causes:")
        for cause in causes:
            st.write(f"- {cause}")
        if meds:
            st.markdown("### 💊 OTC Medication / Home Care:")
            for m in meds:
                st.write(f"- {m}")
        else:
            st.info("No OTC suggestions for detected symptoms.")
        st.markdown("### 🛡️ General Wellness Tips:")
        st.info(WELLNESS_TIPS)
    elif not emergencies:
        st.warning(
            "No recognizable symptoms found in your input. "
            "Please try different words or add more detail."
        )

st.markdown("---")
st.caption(":blue[Code by Anshuman Sinha]")
