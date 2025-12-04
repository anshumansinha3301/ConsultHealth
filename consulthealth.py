import streamlit as st
import time
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional

# -----------------------------------------------------------------------------
# 1. CONFIGURATION & THEME
# -----------------------------------------------------------------------------
@dataclass
class AppConfig:
    APP_TITLE: str = "Consult Health"
    APP_ICON: str = "⚕️"
    VERSION: str = "2.5.0 (Massive DB)"

def inject_css():
    """
    Injects CSS that is adaptable to both light and dark modes.
    Note: We use a standard string (not an f-string) to avoid conflicts with CSS curly braces.
    """
    st.markdown("""
    <style>
        /* Main container typography */
        .stApp {
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        
        /* Clean Sidebar - uses default theme colors */
        [data-testid="stSidebar"] {
            border-right: 1px solid var(--secondary-background-color);
        }
        
        /* Professional Typography */
        h1, h2, h3, h4 {
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-color);
        }
        
        /* Card Component - adaptive background and border */
        .medical-card {
            background-color: var(--secondary-background-color);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid var(--secondary-background-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
            transition: transform 0.2s;
        }
        .medical-card:hover {
            border-color: #2563eb;
        }
        
        /* Alert Component */
        .alert-box {
            background-color: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #ef4444;
            padding: 1rem;
            border-radius: 6px;
            margin-bottom: 1rem;
            color: var(--text-color);
        }
        
        /* Custom Button Styling */
        /* Force specific styling to ensure visibility in all modes */
        div.stButton > button[kind="primary"] {
            background-color: #2563eb !important; 
            color: white !important;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
            height: auto;
            min-height: 45px;
            white-space: nowrap;
            transition: all 0.2s;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #1d4ed8 !important;
            box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.3);
        }
        
        div.stButton > button[kind="secondary"] {
            background-color: transparent;
            border: 1px solid var(--text-color);
            color: var(--text-color);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            height: auto;
            min-height: 45px;
            transition: all 0.2s;
        }
        div.stButton > button[kind="secondary"]:hover {
            border-color: #2563eb;
            color: #2563eb;
            background-color: rgba(37, 99, 235, 0.05);
        }
        
        /* Ensure text areas have correct colors */
        .stTextArea textarea {
            background-color: var(--secondary-background-color);
            color: var(--text-color);
        }

        /* Footer */
        .footer {
            text-align: center;
            font-size: 0.75rem;
            color: var(--text-color);
            opacity: 0.8;
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid var(--secondary-background-color);
        }
        
        /* Fix for small button text wrapping */
        [data-testid="stHorizontalBlock"] > div:first-child button {
             width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA MODELS & KNOWLEDGE BASE
# -----------------------------------------------------------------------------
@dataclass
class ClinicalData:
    """Store for static medical knowledge."""
    
    SYMPTOMS: Dict[str, List[str]] = None
    ALERTS: Dict[str, str] = None
    MEDS: Dict[str, str] = None

    def __post_init__(self):
        self.SYMPTOMS = {
            # -----------------------------------------------------------------
            # SECTION 1: GENERAL / CONSTITUTIONAL / SYSTEMIC
            # -----------------------------------------------------------------
            "fever": [
                "Infectious Pathology (Viral/Bacterial)", 
                "Systemic Inflammatory Response Syndrome (SIRS)", 
                "Autoimmune Etiology (Lupus, RA)", 
                "Malignancy (Lymphoma, Leukemia)", 
                "Drug Fever (Antibiotics, Anticonvulsants)",
                "Neuroleptic Malignant Syndrome",
                "Thyroid Storm"
            ],
            "high fever": [
                "Sepsis",
                "Meningitis",
                "Pyelonephritis",
                "Influenza",
                "Malaria"
            ],
            "low grade fever": [
                "Tuberculosis",
                "Lymphoma",
                "Chronic Infection",
                "Sinusitis"
            ],
            "chills": [
                "Bacteremia", 
                "Sepsis Alert", 
                "Acute Febrile Illness", 
                "Malaria", 
                "Influenza",
                "Pyelonephritis",
                "Pneumonia"
            ],
            "rigors": [
                "Severe Sepsis",
                "Biliary Tract Infection",
                "Malaria"
            ],
            "fatigue": [
                "Anemia (Iron Deficiency, B12)", 
                "Hypothyroidism", 
                "Chronic Fatigue Syndrome", 
                "Depression", 
                "Diabetes Mellitus", 
                "Sleep Apnea", 
                "Mononucleosis",
                "Adrenal Insufficiency",
                "Congestive Heart Failure",
                "Chronic Kidney Disease"
            ],
            "weight loss": [
                "Hyperthyroidism (Graves')", 
                "Type 1 Diabetes Mellitus", 
                "Malignancy Screening Needed", 
                "Malabsorption (Celiac, Crohn's)", 
                "Chronic Infection (TB/HIV)",
                "Anorexia Nervosa"
            ],
            "weight gain": [
                "Hypothyroidism", 
                "Cushing's Syndrome", 
                "Heart Failure (Edema)", 
                "Polycystic Ovary Syndrome (PCOS)", 
                "Medication Side Effect (Steroids, Antipsychotics)",
                "Liver Failure (Ascites)"
            ],
            "night sweats": [
                "Tuberculosis", 
                "Lymphoma (Hodgkin's)", 
                "Menopause", 
                "HIV/AIDS", 
                "Brucellosis", 
                "Infective Endocarditis",
                "Osteomyelitis"
            ],
            "dehydration": [
                "Gastroenteritis", 
                "Heat Exhaustion", 
                "Hyperglycemia (DKA/HHS)", 
                "Diuretic Overuse", 
                "Diabetes Insipidus"
            ],
            "weakness": [
                "Electrolyte Imbalance (Hypokalemia)", 
                "Stroke", 
                "Guillain-Barre Syndrome", 
                "Myasthenia Gravis", 
                "Anemia",
                "Polymyositis"
            ],
            "malaise": [
                "Viral Prodrome", 
                "Chronic Disease", 
                "Depression", 
                "Autoimmune Flares",
                "Hepatitis"
            ],
            "swollen lymph nodes": [
                "Infection (Local/Systemic)", 
                "Lymphoma", 
                "Leukemia", 
                "Metastatic Cancer", 
                "Sarcoidosis",
                "Tuberculosis (Scrofula)"
            ],
            "pallor": [
                "Anemia", 
                "Shock", 
                "Vasoconstriction", 
                "Hypoglycemia",
                "Internal Bleeding"
            ],

            # -----------------------------------------------------------------
            # SECTION 2: RESPIRATORY SYSTEM
            # -----------------------------------------------------------------
            "cough": [
                "Respiratory Infection (Viral/Bacterial)", 
                "Bronchitis", 
                "Pneumonia", 
                "Asthma/COPD", 
                "GERD (Reflux)", 
                "ACE Inhibitor Induced", 
                "Post-nasal Drip",
                "Heart Failure"
            ],
            "dry cough": [
                "Viral URI",
                "Asthma",
                "Interstitial Lung Disease",
                "ACE Inhibitor side effect",
                "COVID-19"
            ],
            "productive cough": [
                "Pneumonia",
                "Chronic Bronchitis",
                "Bronchiectasis",
                "Lung Abscess"
            ],
            "barking cough": [
                "Croup",
                "Tracheitis"
            ],
            "shortness of breath": [
                "Dyspnea", 
                "Congestive Heart Failure", 
                "Pneumonia", 
                "Pulmonary Embolism", 
                "Anemia", 
                "Anxiety/Panic Attack", 
                "Pneumothorax",
                "Pleural Effusion"
            ],
            "dyspnea on exertion": [
                "Angina",
                "COPD",
                "Heart Failure",
                "Pulmonary Hypertension"
            ],
            "orthopnea": [
                "Congestive Heart Failure",
                "Obesity Hypoventilation",
                "Diaphragmatic Paralysis"
            ],
            "wheezing": [
                "Asthma", 
                "COPD Exacerbation", 
                "Anaphylaxis", 
                "Bronchiolitis", 
                "Foreign Body Aspiration"
            ],
            "sore throat": [
                "Pharyngitis (Viral)", 
                "Tonsillitis", 
                "Strep Throat (Group A Strep)", 
                "Mononucleosis", 
                "Epiglottitis", 
                "Peritonsillar Abscess",
                "Gonococcal Pharyngitis"
            ],
            "hoarseness": [
                "Laryngitis", 
                "Vocal Cord Nodules", 
                "GERD", 
                "Thyroid Malignancy", 
                "Laryngeal Nerve Palsy (Recurrent)",
                "Lung Cancer (Pancoast Tumor)"
            ],
            "coughing blood": [
                "Tuberculosis", 
                "Lung Cancer", 
                "Pulmonary Embolism", 
                "Bronchiectasis", 
                "Severe Bronchitis", 
                "Goodpasture Syndrome",
                "Wegener's Granulomatosis"
            ],
            "nasal congestion": [
                "Rhinitis (Allergic/Viral)", 
                "Sinusitis", 
                "Nasal Polyps", 
                "Deviated Septum",
                "Rhinitis Medicamentosa"
            ],
            "sneezing": [
                "Allergic Rhinitis", 
                "Viral URI", 
                "Irritant Exposure"
            ],
            "stridor": [
                "Croup", 
                "Epiglottitis", 
                "Foreign Body", 
                "Laryngomalacia", 
                "Anaphylaxis",
                "Retropharyngeal Abscess"
            ],
            "pleuritic pain": [
                "Pleurisy", 
                "Pneumonia", 
                "Pulmonary Embolism", 
                "Pericarditis",
                "Pneumothorax"
            ],

            # -----------------------------------------------------------------
            # SECTION 3: CARDIOVASCULAR SYSTEM
            # -----------------------------------------------------------------
            "chest pain": [
                "Acute Coronary Syndrome (MI)", 
                "Stable/Unstable Angina", 
                "GERD (Esophageal Spasm)", 
                "Costochondritis (Musculoskeletal)", 
                "Pericarditis", 
                "Aortic Dissection", 
                "Panic Attack", 
                "Pneumothorax"
            ],
            "substernal chest pain": [
                "Myocardial Infarction",
                "Angina Pectoris",
                "Esophageal Spasm"
            ],
            "tearing chest pain": [
                "Aortic Dissection"
            ],
            "palpitations": [
                "Sinus Tachycardia", 
                "Atrial Fibrillation", 
                "Anxiety", 
                "Thyrotoxicosis", 
                "Anemia", 
                "PVCs/PACs", 
                "Caffeine/Stimulant Use",
                "Electrolyte Imbalance"
            ],
            "swollen legs": [
                "Congestive Heart Failure", 
                "Deep Vein Thrombosis (DVT)", 
                "Chronic Venous Insufficiency", 
                "Kidney Disease (Nephrotic Syndrome)", 
                "Lymphedema", 
                "Calcium Channel Blockers side effect",
                "Liver Failure (Low Albumin)"
            ],
            "unilateral leg swelling": [
                "Deep Vein Thrombosis (DVT)",
                "Baker's Cyst Rupture",
                "Cellulitis"
            ],
            "cyanosis": [
                "Hypoxia", 
                "Congenital Heart Defect", 
                "Pulmonary Embolism", 
                "Severe Asthma", 
                "Methemoglobinemia"
            ],
            "claudication": [
                "Peripheral Artery Disease", 
                "Spinal Stenosis", 
                "Deep Vein Thrombosis"
            ],
            "syncope": [
                "Vasovagal Syncope", 
                "Orthostatic Hypotension", 
                "Arrhythmia (V-Tach/Heart Block)", 
                "Aortic Stenosis", 
                "Seizure",
                "Pulmonary Embolism"
            ],
            "lightheadedness": [
                "Dehydration",
                "Hypotension",
                "Anemia",
                "Hypoglycemia"
            ],
            "irregular heartbeat": [
                "Atrial Fibrillation", 
                "Arrhythmia", 
                "Electrolyte Imbalance (K/Mg)"
            ],
            "bradycardia": [
                "Hypothyroidism",
                "Sick Sinus Syndrome",
                "Heart Block",
                "Athlete's Heart",
                "Beta-blocker overdose"
            ],
            "tachycardia": [
                "Fever",
                "Anemia",
                "Hyperthyroidism",
                "Dehydration",
                "Shock",
                "Anxiety"
            ],

            # -----------------------------------------------------------------
            # SECTION 4: NEUROLOGICAL SYSTEM
            # -----------------------------------------------------------------
            "headache": [
                "Migraine", 
                "Tension Type Headache", 
                "Intracranial Issue (Tumor/Bleed)", 
                "Sinusitis", 
                "Cluster Headache", 
                "Temporal Arteritis", 
                "Meningitis", 
                "Subarachnoid Hemorrhage"
            ],
            "thunderclap headache": [
                "Subarachnoid Hemorrhage",
                "Reversible Cerebral Vasoconstriction Syndrome"
            ],
            "morning headache": [
                "Sleep Apnea",
                "Increased Intracranial Pressure",
                "Hypertension"
            ],
            "dizziness": [
                "Vertigo (BPPV)", 
                "Orthostatic Hypotension", 
                "Arrhythmia", 
                "Anemia", 
                "Inner Ear Infection (Labyrinthitis)", 
                "Meniere's Disease", 
                "Stroke (Posterior Circulation)"
            ],
            "room spinning": [
                "Benign Paroxysmal Positional Vertigo (BPPV)",
                "Meniere's Disease",
                "Vestibular Neuritis"
            ],
            "numbness": [
                "Peripheral Neuropathy (Diabetes)", 
                "Stroke", 
                "Multiple Sclerosis", 
                "Radiculopathy (Pinched Nerve)", 
                "Carpal Tunnel Syndrome", 
                "Vitamin B12 Deficiency"
            ],
            "unilateral numbness": [
                "Stroke",
                "TIA",
                "Multiple Sclerosis"
            ],
            "tremors": [
                "Parkinson's Disease", 
                "Essential Tremor", 
                "Hyperthyroidism", 
                "Anxiety", 
                "Alcohol Withdrawal", 
                "Lithium Toxicity"
            ],
            "confusion": [
                "Delirium", 
                "Dementia (Alzheimer's)", 
                "Stroke", 
                "Sepsis", 
                "Hypoglycemia", 
                "Electrolyte Imbalance (Na/Ca)", 
                "Hepatic Encephalopathy", 
                "Wernicke's Encephalopathy"
            ],
            "double vision": [
                "Cranial Nerve Palsy", 
                "Myasthenia Gravis", 
                "Stroke", 
                "Multiple Sclerosis", 
                "Graves' Disease", 
                "Orbital Cellulitis"
            ],
            "seizure": [
                "Epilepsy", 
                "Febrile Seizure (Pediatric)", 
                "Alcohol Withdrawal", 
                "Brain Tumor", 
                "Hyponatremia", 
                "Eclampsia",
                "Trauma"
            ],
            "memory loss": [
                "Alzheimer's Disease", 
                "Dementia", 
                "Hypothyroidism", 
                "Vitamin B12 Deficiency", 
                "Depression (Pseudodementia)"
            ],
            "slurred speech": [
                "Stroke (CVA)", 
                "TIA", 
                "Alcohol Intoxication", 
                "ALS", 
                "Multiple Sclerosis",
                "Sedative Overdose"
            ],
            "facial drooping": [
                "Bell's Palsy", 
                "Stroke", 
                "Lyme Disease", 
                "Parotid Tumor"
            ],
            "loss of balance": [
                "Cerebellar Ataxia", 
                "Vestibular Neuritis", 
                "Stroke", 
                "Parkinson's Disease", 
                "Normal Pressure Hydrocephalus"
            ],
            "fainting": [
                "Vasovagal Syncope",
                "Orthostatic Hypotension",
                "Cardiac Arrhythmia"
            ],
            "tingling": [
                "Paresthesia",
                "Neuropathy",
                "Hyperventilation",
                "Hypocalcemia"
            ],

            # -----------------------------------------------------------------
            # SECTION 5: GASTROINTESTINAL SYSTEM
            # -----------------------------------------------------------------
            "abdominal pain": [
                "Appendicitis", 
                "Cholecystitis", 
                "Gastritis", 
                "Bowel Obstruction", 
                "Pancreatitis", 
                "Diverticulitis", 
                "IBS", 
                "Mesenteric Ischemia"
            ],
            "right lower quadrant pain": [
                "Appendicitis",
                "Crohn's Disease",
                "Ectopic Pregnancy",
                "Ovarian Torsion"
            ],
            "right upper quadrant pain": [
                "Cholecystitis",
                "Biliary Colic",
                "Hepatitis",
                "Liver Abscess"
            ],
            "left lower quadrant pain": [
                "Diverticulitis",
                "Ovarian Cyst",
                "Ulcerative Colitis"
            ],
            "epigastric pain": [
                "GERD",
                "Peptic Ulcer Disease",
                "Pancreatitis",
                "Myocardial Infarction"
            ],
            "nausea": [
                "Gastroenteritis", 
                "Pregnancy", 
                "Vestibular Neuritis", 
                "Medication Side Effect", 
                "Migraine", 
                "Increased ICP"
            ],
            "vomiting": [
                "Gastroenteritis", 
                "Food Poisoning", 
                "Gastritis", 
                "Increased Intracranial Pressure", 
                "Cyclic Vomiting Syndrome", 
                "DKA",
                "Bowel Obstruction"
            ],
            "projectile vomiting": [
                "Pyloric Stenosis (Infants)",
                "Increased Intracranial Pressure"
            ],
            "diarrhea": [
                "Viral Gastroenteritis", 
                "Food Poisoning", 
                "IBS", 
                "Inflammatory Bowel Disease (Crohn's/UC)", 
                "Celiac Disease", 
                "Malabsorption",
                "Clostridium difficile"
            ],
            "bloody diarrhea": [
                "Ulcerative Colitis",
                "Crohn's Disease",
                "Dysentery (Shigella/Campylobacter)",
                "Ischemic Colitis"
            ],
            "constipation": [
                "Functional Constipation", 
                "IBS-C", 
                "Hypothyroidism", 
                "Opioid Use", 
                "Hypercalcemia", 
                "Colorectal Cancer",
                "Dehydration"
            ],
            "heartburn": [
                "GERD", 
                "Hiatal Hernia", 
                "Peptic Ulcer Disease", 
                "Gastritis", 
                "Esophagitis"
            ],
            "bloating": [
                "IBS", 
                "Lactose Intolerance", 
                "Small Bowel Obstruction", 
                "Ascites", 
                "SIBO", 
                "Ovarian Cancer"
            ],
            "difficulty swallowing": [
                "Esophagitis", 
                "Esophageal Stricture", 
                "Stroke", 
                "Achalasia", 
                "Esophageal Cancer", 
                "Zenker's Diverticulum"
            ],
            "rectal bleeding": [
                "Hemorrhoids", 
                "Anal Fissure", 
                "Colorectal Cancer", 
                "Diverticulosis", 
                "IBD", 
                "Angiodysplasia"
            ],
            "jaundice": [
                "Hepatitis (A/B/C)", 
                "Liver Cirrhosis", 
                "Gallstones (Choledocholithiasis)", 
                "Hemolytic Anemia", 
                "Pancreatic Cancer", 
                "Gilbert's Syndrome"
            ],
            "black stools": [
                "Upper GI Bleed (Melena)", 
                "Peptic Ulcer", 
                "Gastritis", 
                "Iron Supplements", 
                "Bismuth Subsalicylate"
            ],
            "loss of appetite": [
                "Malignancy", 
                "Depression", 
                "Chronic Infection", 
                "Gastroparesis", 
                "Liver Failure",
                "Kidney Failure"
            ],
            "belching": [
                "GERD",
                "Aerophagia",
                "Gastritis"
            ],
            "gas": [
                "Lactose Intolerance",
                "IBS",
                "High Fiber Diet",
                "Celiac Disease"
            ],

            # -----------------------------------------------------------------
            # SECTION 6: MUSCULOSKELETAL / RHEUMATOLOGY
            # -----------------------------------------------------------------
            "back pain": [
                "Muscle Strain", 
                "Herniated Nucleus Pulposus", 
                "Sciatica", 
                "Renal Colic (Kidney Stone)", 
                "Osteoporosis", 
                "Spinal Stenosis", 
                "Ankylosing Spondylitis", 
                "Metastatic Disease"
            ],
            "low back pain": [
                "Lumbar Strain",
                "Degenerative Disc Disease",
                "Spondylolisthesis"
            ],
            "joint pain": [
                "Osteoarthritis", 
                "Rheumatoid Arthritis", 
                "Bursitis", 
                "Gout", 
                "Septic Arthritis", 
                "Lupus (SLE)", 
                "Psoriatic Arthritis"
            ],
            "knee pain": [
                "Meniscal Tear",
                "ACL Injury",
                "Osteoarthritis",
                "Patellofemoral Syndrome"
            ],
            "muscle weakness": [
                "Myasthenia Gravis", 
                "Polymyositis", 
                "Hypokalemia", 
                "Stroke", 
                "ALS", 
                "Muscular Dystrophy"
            ],
            "neck pain": [
                "Cervical Spondylosis", 
                "Muscle Strain", 
                "Meningitis", 
                "Whiplash", 
                "Torticollis"
            ],
            "muscle cramps": [
                "Dehydration", 
                "Electrolyte Imbalance (Mg/K/Ca)", 
                "Venous Insufficiency", 
                "Statins side effect"
            ],
            "joint swelling": [
                "Arthritis", 
                "Gout", 
                "Trauma", 
                "Septic Arthritis", 
                "Hemarthrosis"
            ],
            "shoulder pain": [
                "Rotator Cuff Injury", 
                "Frozen Shoulder (Adhesive Capsulitis)", 
                "Bursitis", 
                "Referred Pain (Gallbladder/Heart)"
            ],
            "wrist pain": [
                "Carpal Tunnel Syndrome",
                "De Quervain's Tenosynovitis",
                "Ganglion Cyst",
                "Fracture"
            ],
            "heel pain": [
                "Plantar Fasciitis",
                "Calcaneal Spur",
                "Achilles Tendonitis"
            ],
            "hip pain": [
                "Osteoarthritis",
                "Trochanteric Bursitis",
                "Hip Fracture",
                "Labral Tear"
            ],
            "morning stiffness": [
                "Rheumatoid Arthritis",
                "Polymyalgia Rheumatica",
                "Ankylosing Spondylitis"
            ],

            # -----------------------------------------------------------------
            # SECTION 7: DERMATOLOGY
            # -----------------------------------------------------------------
            "rash": [
                "Contact Dermatitis", 
                "Viral Exanthem", 
                "Drug Reaction", 
                "Urticaria", 
                "Psoriasis", 
                "Scabies", 
                "Lyme Disease (Erythema Migrans)",
                "Syphilis (Secondary)"
            ],
            "petechiae": [
                "Thrombocytopenia",
                "Meningococcemia",
                "Vasculitis",
                "Leukemia"
            ],
            "itching": [
                "Allergic Reaction", 
                "Eczema (Atopic Dermatitis)", 
                "Liver Disease (Cholestasis)", 
                "Kidney Failure (Uremia)", 
                "Lymphoma", 
                "Scabies"
            ],
            "hair loss": [
                "Alopecia Areata", 
                "Telogen Effluvium", 
                "Hypothyroidism", 
                "Iron Deficiency", 
                "PCOS", 
                "Fungal Infection (Tinea Capitis)"
            ],
            "bruising": [
                "Thrombocytopenia", 
                "Trauma", 
                "Vitamin K Deficiency", 
                "Leukemia", 
                "Cushing's Syndrome", 
                "Von Willebrand Disease"
            ],
            "hives": [
                "Allergic Reaction", 
                "Stress", 
                "Viral Infection", 
                "Autoimmune Disease"
            ],
            "dry skin": [
                "Xerosis", 
                "Hypothyroidism", 
                "Eczema", 
                "Sjogren's Syndrome"
            ],
            "acne": [
                "Acne Vulgaris", 
                "Hormonal Imbalance", 
                "Rosacea", 
                "Folliculitis"
            ],
            "skin lesions": [
                "Melanoma", 
                "Basal Cell Carcinoma", 
                "Squamous Cell Carcinoma", 
                "Seborrheic Keratosis"
            ],
            "yellow skin": [
                "Jaundice", 
                "Carotenemia"
            ],
            "blisters": [
                "Herpes Simplex",
                "Shingles (Varicella Zoster)",
                "Pemphigus Vulgaris",
                "Bullous Pemphigoid",
                "Burn"
            ],
            "nail changes": [
                "Psoriasis",
                "Fungal Infection (Onychomycosis)",
                "Iron Deficiency (Koilonychia)",
                "Lung Disease (Clubbing)"
            ],

            # -----------------------------------------------------------------
            # SECTION 8: ENT / DENTAL
            # -----------------------------------------------------------------
            "ear pain": [
                "Otitis Media", 
                "Otitis Externa (Swimmer's Ear)", 
                "Eustachian Tube Dysfunction", 
                "TMJ Disorder", 
                "Mastoiditis"
            ],
            "ear discharge": [
                "Otitis Externa",
                "Ruptured Eardrum",
                "CSF Leak (Trauma)"
            ],
            "toothache": [
                "Dental Caries", 
                "Pulpitis", 
                "Periapical Abscess", 
                "Dental Trauma", 
                "Sinusitis (referred pain)"
            ],
            "nosebleed": [
                "Epistaxis", 
                "Trauma", 
                "Hypertension", 
                "Coagulopathy", 
                "Dry Mucosa", 
                "Nasal Tumor"
            ],
            "ringing in ears": [
                "Tinnitus", 
                "Hearing Loss", 
                "Meniere's Disease", 
                "Acoustic Neuroma", 
                "Salicylate Toxicity"
            ],
            "hearing loss": [
                "Presbycusis", 
                "Cerumen Impaction", 
                "Noise Exposure", 
                "Otosclerosis", 
                "Sudden Sensorineural Hearing Loss"
            ],
            "mouth ulcers": [
                "Aphthous Stomatitis (Canker Sore)", 
                "Herpes Simplex (Cold Sore)", 
                "Behcet's Disease", 
                "Vitamin Deficiency (B12/Iron)", 
                "Oral Cancer"
            ],
            "bad breath": [
                "Halitosis", 
                "Gingivitis", 
                "GERD", 
                "Sinusitis", 
                "Tonsilloliths"
            ],
            "swollen glands": [
                "Infection (Strep/Viral)", 
                "Lymphoma", 
                "Mononucleosis", 
                "Dental Abscess"
            ],
            "white patches in mouth": [
                "Thrush (Candidiasis)",
                "Leukoplakia",
                "Lichen Planus"
            ],
            "loss of smell": [
                "COVID-19",
                "Sinusitis",
                "Nasal Polyps",
                "Head Trauma"
            ],

            # -----------------------------------------------------------------
            # SECTION 9: MENTAL HEALTH / PSYCHIATRY
            # -----------------------------------------------------------------
            "anxiety": [
                "Generalized Anxiety Disorder", 
                "Panic Attack", 
                "Acute Stress Reaction", 
                "Hyperthyroidism", 
                "Caffeine Intoxication", 
                "Pheochromocytoma"
            ],
            "insomnia": [
                "Sleep Hygiene Issue", 
                "Stress-related Insomnia", 
                "Sleep Apnea", 
                "Depression", 
                "Restless Leg Syndrome", 
                "Circadian Rhythm Disorder"
            ],
            "depression": [
                "Major Depressive Disorder", 
                "Bipolar Disorder", 
                "Hypothyroidism", 
                "Vitamin D Deficiency", 
                "Anemia", 
                "Chronic Pain"
            ],
            "hallucinations": [
                "Schizophrenia", 
                "Drug Toxicity", 
                "Delirium", 
                "Severe Depression", 
                "Lewy Body Dementia"
            ],
            "mood swings": [
                "Bipolar Disorder", 
                "Borderline Personality Disorder", 
                "PMS/PMDD", 
                "Hormonal Imbalance",
                "Substance Abuse"
            ],
            "suicidal thoughts": [
                "Major Depression", 
                "Crisis State", 
                "Psychosis", 
                "Substance Abuse"
            ],
            "panic": [
                "Panic Disorder", 
                "Phobia", 
                "PTSD", 
                "Hyperthyroidism"
            ],
            "irritability": [
                "Depression",
                "Anxiety",
                "Bipolar Disorder",
                "Sleep Deprivation",
                "Graves' Disease"
            ],
            "social withdrawal": [
                "Depression",
                "Schizophrenia",
                "Social Anxiety Disorder",
                "Autism Spectrum Disorder"
            ],

            # -----------------------------------------------------------------
            # SECTION 10: GENITOURINARY / NEPHROLOGY / MALE REPRODUCTIVE
            # -----------------------------------------------------------------
            "painful urination": [
                "Urinary Tract Infection (UTI)", 
                "STI (Chlamydia/Gonorrhea)", 
                "Kidney Stones", 
                "Prostatitis", 
                "Interstitial Cystitis", 
                "Urethritis"
            ],
            "blood in urine": [
                "UTI", 
                "Kidney Stones", 
                "Bladder Cancer", 
                "Glomerulonephritis", 
                "Trauma", 
                "Prostate Cancer", 
                "Polycystic Kidney Disease"
            ],
            "frequent urination": [
                "Diabetes Mellitus", 
                "UTI", 
                "Benign Prostatic Hyperplasia (BPH)", 
                "Overactive Bladder", 
                "Diuretics", 
                "Diabetes Insipidus"
            ],
            "incontinence": [
                "Stress Incontinence", 
                "Urge Incontinence", 
                "Neurogenic Bladder", 
                "Overflow Incontinence (BPH)"
            ],
            "flank pain": [
                "Kidney Stones (Renal Colic)", 
                "Pyelonephritis", 
                "Hydronephrosis", 
                "Renal Infarction",
                "Musculoskeletal Strain"
            ],
            "testicular pain": [
                "Testicular Torsion", 
                "Epididymitis", 
                "Orchitis", 
                "Inguinal Hernia", 
                "Varicocele"
            ],
            "testicular lump": [
                "Testicular Cancer",
                "Hydrocele",
                "Spermatocele",
                "Varicocele"
            ],
            "erectile dysfunction": [
                "Vascular Disease",
                "Diabetes",
                "Medication Side Effect",
                "Psychogenic",
                "Low Testosterone"
            ],

            # -----------------------------------------------------------------
            # SECTION 11: REPRODUCTIVE HEALTH (FEMALE)
            # -----------------------------------------------------------------
            "pelvic pain": [
                "Pelvic Inflammatory Disease (PID)", 
                "Endometriosis", 
                "Ovarian Cysts", 
                "Ectopic Pregnancy", 
                "Fibroids"
            ],
            "vaginal discharge": [
                "Bacterial Vaginosis", 
                "Candidiasis (Yeast)", 
                "Trichomoniasis", 
                "Chlamydia/Gonorrhea"
            ],
            "irregular periods": [
                "PCOS", 
                "Thyroid Dysfunction", 
                "Menopause", 
                "Stress", 
                "Prolactinoma",
                "Eating Disorders"
            ],
            "menstrual cramps": [
                "Dysmenorrhea", 
                "Endometriosis", 
                "Adenomyosis", 
                "Fibroids"
            ],
            "hot flashes": [
                "Menopause", 
                "Carcinoid Syndrome", 
                "Medication Side Effect (Tamoxifen)"
            ],
            "breast lump": [
                "Fibroadenoma", 
                "Breast Cyst", 
                "Breast Cancer", 
                "Mastitis",
                "Abscess"
            ],
            "nipple discharge": [
                "Intraductal Papilloma",
                "Galactorrhea (Prolactinoma)",
                "Breast Cancer",
                "Mammary Duct Ectasia"
            ],
            "vaginal itching": [
                "Yeast Infection",
                "Contact Dermatitis",
                "Lichen Sclerosus",
                "Pinworms"
            ],

            # -----------------------------------------------------------------
            # SECTION 12: OPHTHALMOLOGY
            # -----------------------------------------------------------------
            "red eye": [
                "Conjunctivitis (Pink Eye)", 
                "Subconjunctival Hemorrhage", 
                "Uveitis", 
                "Glaucoma (Acute Angle Closure)", 
                "Corneal Abrasion"
            ],
            "eye pain": [
                "Corneal Abrasion", 
                "Glaucoma", 
                "Optic Neuritis", 
                "Uveitis", 
                "Scleritis",
                "Foreign Body"
            ],
            "blurred vision": [
                "Refractive Error", 
                "Cataract", 
                "Macular Degeneration", 
                "Diabetic Retinopathy", 
                "Glaucoma"
            ],
            "vision loss": [
                "Retinal Detachment", 
                "Central Retinal Artery Occlusion", 
                "Stroke", 
                "Glaucoma", 
                "Temporal Arteritis"
            ],
            "floaters": [
                "Posterior Vitreous Detachment", 
                "Retinal Tear", 
                "Uveitis"
            ],
            "dry eyes": [
                "Dry Eye Syndrome", 
                "Sjogren's Syndrome", 
                "Blepharitis", 
                "Medication Side Effect"
            ],
            "light sensitivity": [
                "Migraine", 
                "Meningitis", 
                "Uveitis", 
                "Corneal Abrasion"
            ],
            "excessive tearing": [
                "Blocked Tear Duct",
                "Allergies",
                "Dry Eye (Reflex Tearing)",
                "Conjunctivitis"
            ],
            "night blindness": [
                "Vitamin A Deficiency",
                "Retinitis Pigmentosa",
                "Cataracts"
            ],

            # -----------------------------------------------------------------
            # SECTION 13: ENDOCRINOLOGY / METABOLIC
            # -----------------------------------------------------------------
            "excessive thirst": [
                "Diabetes Mellitus", 
                "Diabetes Insipidus", 
                "Psychogenic Polydipsia", 
                "Dehydration", 
                "Hypercalcemia"
            ],
            "heat intolerance": [
                "Hyperthyroidism", 
                "Menopause", 
                "Dysautonomia"
            ],
            "cold intolerance": [
                "Hypothyroidism", 
                "Anorexia Nervosa", 
                "Raynaud's Phenomenon"
            ],
            "excessive hair growth": [
                "Hirsutism", 
                "PCOS", 
                "Cushing's Syndrome", 
                "Adrenal Tumor"
            ],
            "moon face": [
                "Cushing's Syndrome",
                "Steroid Use"
            ],
            "salt craving": [
                "Addison's Disease",
                "Dehydration",
                "Bartter Syndrome"
            ],
            
            # -----------------------------------------------------------------
            # SECTION 14: HEMATOLOGY / ONCOLOGY
            # -----------------------------------------------------------------
            "easy bleeding": [
                "Thrombocytopenia", 
                "Hemophilia", 
                "Von Willebrand Disease", 
                "Liver Disease", 
                "Vitamin K Deficiency"
            ],
            "gum bleeding": [
                "Gingivitis",
                "Vitamin C Deficiency (Scurvy)",
                "Leukemia",
                "Thrombocytopenia"
            ],
            "enlarged spleen": [
                "Mononucleosis",
                "Leukemia",
                "Lymphoma",
                "Malaria",
                "Liver Cirrhosis (Portal Hypertension)"
            ],

            # -----------------------------------------------------------------
            # SECTION 15: PEDIATRICS SPECIFIC
            # -----------------------------------------------------------------
            "failure to thrive": [
                "Malnutrition", 
                "Celiac Disease", 
                "Cystic Fibrosis", 
                "Congenital Heart Defect",
                "Metabolic Disorders"
            ],
            "bedwetting": [
                "Enuresis", 
                "UTI", 
                "Diabetes", 
                "Stress"
            ],
            "croup cough": [
                "Croup (Laryngotracheobronchitis)", 
                "Foreign Body"
            ],
            "colic": [
                "Infant Colic", 
                "Cow's Milk Protein Allergy", 
                "Reflux"
            ],
            "floppy baby": [
                "Botulism",
                "Spinal Muscular Atrophy",
                "Hypothyroidism",
                "Down Syndrome"
            ],
            "delayed milestones": [
                "Autism Spectrum Disorder",
                "Cerebral Palsy",
                "Global Developmental Delay",
                "Hearing Loss"
            ],
            "rash in baby": [
                "Diaper Dermatitis",
                "Roseola",
                "Fifth Disease",
                "Hand Foot Mouth Disease"
            ],

            # -----------------------------------------------------------------
            # SECTION 16: TRAUMA / INJURY / ENVIRONMENTAL
            # -----------------------------------------------------------------
            "burn": [
                "Thermal Burn", 
                "Chemical Burn", 
                "Electrical Burn", 
                "Sunburn"
            ],
            "laceration": [
                "Cut", 
                "Wound Infection", 
                "Tetanus Risk"
            ],
            "head injury": [
                "Concussion", 
                "Subdural Hematoma", 
                "Epidural Hematoma", 
                "Skull Fracture"
            ],
            "fracture": [
                "Bone Break", 
                "Osteoporosis", 
                "Stress Fracture", 
                "Pathologic Fracture"
            ],
            "frostbite": [
                "Cold Exposure",
                "Vascular Compromise"
            ],
            "hypothermia": [
                "Environmental Exposure",
                "Sepsis",
                "Hypothyroidism"
            ],
            "snake bite": [
                "Venomous Envenomation",
                "Local Tissue Necrosis",
                "Anaphylaxis"
            ],
            "insect bite": [
                "Local Reaction",
                "Lyme Disease",
                "West Nile Virus",
                "Zika Virus",
                "Anaphylaxis"
            ],

            # -----------------------------------------------------------------
            # SECTION 17: RARE / MISCELLANEOUS
            # -----------------------------------------------------------------
            "blue urine": [
                "Hartnup Disease",
                "Medication (Methylene Blue)",
                "Pseudomonas Infection"
            ],
            "green urine": [
                "Propofol Infusion",
                "Pseudomonas Infection"
            ],
            "copper ring in eye": [
                "Wilson's Disease"
            ],
            "strawberry tongue": [
                "Kawasaki Disease",
                "Scarlet Fever",
                "Toxic Shock Syndrome"
            ],
            "cafe au lait spots": [
                "Neurofibromatosis",
                "McCune-Albright Syndrome"
            ],
            "port wine stain": [
                "Sturge-Weber Syndrome",
                "Klippel-Trenaunay Syndrome"
            ]
        }
        
        self.ALERTS = {
            "chest pain": "CRITICAL: Rule out Cardiac Ischemia/MI/Dissection immediately.",
            "substernal chest pain": "CRITICAL: High suspicion for Myocardial Infarction.",
            "tearing chest pain": "EMERGENCY: Immediate CT Angio for Aortic Dissection.",
            "shortness of breath": "URGENT: Assess O2 saturation, airway patency, rule out PE/Pneumothorax.",
            "unconscious": "EMERGENCY: Initiate Code Blue / resuscitation protocols. Check Glucose.",
            "slurred speech": "EMERGENCY: Stroke Protocol (FAST). Time last known well?",
            "facial drooping": "EMERGENCY: Stroke Protocol Activation.",
            "severe headache": "URGENT: Rule out intracranial hemorrhage (Thunderclap) / Meningitis.",
            "thunderclap headache": "EMERGENCY: Rule out Subarachnoid Hemorrhage.",
            "worst headache of life": "EMERGENCY: Rule out Aneurysm Rupture/SAH.",
            "suicidal": "PSYCHIATRIC EMERGENCY: Immediate safety observation required. 1:1 Sitter.",
            "blood in vomit": "URGENT: GI Bleed Protocol - Monitor Hemodynamics, Large bore IV.",
            "seizure": "EMERGENCY: Protect airway, time duration, administer benzodiazepines if >5 min.",
            "coughing blood": "URGENT: Hemoptysis Assessment - Rule out TB/PE/Malignancy.",
            "stiff neck": "URGENT: Rule out Meningitis if accompanied by fever/photophobia.",
            "vision loss": "EMERGENCY: Sudden vision loss requires immediate ophthalmologic eval (Retinal Detachment/Stroke).",
            "confusion": "HIGH PRIORITY: Assess for Delirium/Stroke/Hypoglycemia/Sepsis.",
            "rectal bleeding": "URGENT: Assess volume - Rule out lower GI bleed. Check Hemoglobin.",
            "black stools": "URGENT: Assess for Upper GI Bleeding (Melena).",
            "difficulty swallowing": "HIGH PRIORITY: Risk of Aspiration/Malnutrition. Rule out malignancy.",
            "hallucinations": "URGENT: Psychiatric/Neurologic Evaluation needed. Rule out withdrawals.",
            "blood in urine": "URGENT: Rule out malignancy/infection/stones/glomerulonephritis.",
            "testicular pain": "EMERGENCY: Rule out Testicular Torsion (Time sensitive).",
            "eye pain": "URGENT: Rule out Acute Angle Closure Glaucoma if accompanied by halo/nausea.",
            "head injury": "URGENT: Glasgow Coma Scale assessment. Rule out intracranial bleed.",
            "burn": "URGENT: Assess %BSA, Airway involvement, Fluid resuscitation if severe.",
            "fever in infant": "EMERGENCY: Sepsis workup required if < 3 months old.",
            "snake bite": "EMERGENCY: Antivenom assessment if indicated. Monitor airway.",
            "overdose": "EMERGENCY: Contact Poison Control. Administer antidote if available.",
            "stridor": "EMERGENCY: Protect Airway. Prepare for intubation.",
            "anaphylaxis": "EMERGENCY: Administer Epinephrine immediately.",
            "floppy baby": "URGENT: Neurologic assessment for hypotonia (Botulism/SMA).",
            "projectile vomiting": "URGENT: Rule out Pyloric Stenosis in infants."
        }
        
        self.MEDS = {
            # General
            "fever": "Antipyretics (Acetaminophen/Ibuprofen), Hydration, Tepid sponging",
            "high fever": "Aggressive cooling, Antipyretics, Treat Sepsis source",
            "chills": "Warm blankets, Treat underlying infection, Antipyretics",
            "fatigue": "Sleep hygiene, Treat underlying cause (Iron, Thyroid), Exercise",
            "pain": "Acetaminophen, NSAIDs, Topical analgesics, Opioids (severe/acute only)",
            "dehydration": "Oral Rehydration Solutions (ORS), IV Normal Saline (if severe)",
            
            # Respiratory
            "cough": "Antitussives (Dextromethorphan), Expectorants (Guaifenesin), Honey",
            "dry cough": "Cough Suppressants, Lozenges, Humidifier",
            "productive cough": "Expectorants, Mucolytics, Chest Physiotherapy",
            "wheezing": "Bronchodilators (Albuterol), Inhaled Corticosteroids (Budesonide)",
            "sore throat": "Saltwater gargle, Lozenges, Analgesics, Antibiotics (if Strep +)",
            "nasal congestion": "Decongestants (Pseudoephedrine), Saline spray, Intranasal steroids",
            "croup cough": "Dexamethasone, Nebulized Epinephrine (if stridor)",
            "sneezing": "Antihistamines (Loratadine/Cetirizine)",
            
            # Cardiovascular
            "chest pain": "Aspirin, Nitroglycerin (if angina), Oxygen (if hypoxic), Morphine",
            "palpitations": "Beta-blockers (if indicated), Vagal maneuvers, Magnesium",
            "swollen legs": "Diuretics (Furosemide), Compression stockings, Elevation",
            "high blood pressure": "Antihypertensives (ACEi/ARB/CCB/Thiazide)",
            
            # Gastrointestinal
            "nausea": "Antiemetics (Ondansetron/Promethazine/Metoclopramide), Ginger",
            "heartburn": "PPIs (Omeprazole), H2 Blockers (Famotidine), Antacids (Calcium Carbonate)",
            "diarrhea": "Loperamide (if non-infectious), Oral Rehydration Salts, Probiotics, Zinc",
            "constipation": "Fiber, Osmotic laxatives (PEG), Stool softeners (Docusate), Senna",
            "vomiting": "Antiemetics, IV Fluids, bowel rest",
            "hemorrhoids": "Sitz baths, Topical hydrocortisone, Fiber diet",
            "gas": "Simethicone, Alpha-galactosidase",
            "bloating": "Low FODMAP diet, Probiotics, Simethicone",
            
            # Neurological
            "headache": "NSAIDs, Triptans (migraine), Oxygen (cluster), Caffeine",
            "migraine": "Sumatriptan, NSAIDs, Antiemetics, Dark room",
            "dizziness": "Meclizine, Epley maneuver (BPPV), Hydration",
            "numbness": "Gabapentin (neuropathic), Vitamin B12 supplementation",
            "seizure": "Lorazepam/Diazepam (acute), Levetiracetam/Valproate (maintenance)",
            "vertigo": "Betahistine, Vestibular Rehabilitation",
            
            # Musculoskeletal
            "back pain": "NSAIDs, Muscle relaxants (Cyclobenzaprine), Heat/Ice, PT",
            "low back pain": "Physical Therapy, NSAIDs, Activity Modification",
            "joint pain": "Topical NSAIDs (Diclofenac), Oral NSAIDs, Steroid injections",
            "muscle cramps": "Magnesium, Potassium, Hydration, Stretching",
            "gout": "Indomethacin, Colchicine, Allopurinol (preventative)",
            "neck pain": "Heat, Massage, NSAIDs, Ergonomic adjustment",
            
            # Dermatology
            "rash": "Topical Corticosteroids (Hydrocortisone), Antihistamines, Moisturizers",
            "itching": "Antihistamines (Cetirizine/Diphenhydramine), Calamine, Cool compress",
            "acne": "Benzoyl Peroxide, Topical Retinoids, Doxycycline",
            "burn": "Cool water, Silver Sulfadiazine, Bacitracin, Aloe Vera",
            "fungal rash": "Topical Antifungals (Clotrimazole/Terbinafine)",
            "hives": "Antihistamines, Steroids (if severe)",
            "dandruff": "Ketoconazole shampoo, Selenium sulfide",
            
            # ENT / Dental
            "ear pain": "Analgesics, Otic drops (Ofloxacin/Ciprodex), Warm compress",
            "toothache": "NSAIDs, Clove oil, Urgent Dental Referral, Antibiotics (Amoxicillin)",
            "nosebleed": "Oxymetazoline spray, Compression, Silver Nitrate cautery",
            "mouth ulcers": "Triamcinolone paste, Magic Mouthwash, Saltwater rinse",
            
            # Mental Health
            "anxiety": "SSRI/SNRI, Benzodiazepines (short term), Therapy (CBT), Hydroxyzine",
            "insomnia": "Melatonin, Trazodone, Sleep hygiene, Doxepin",
            "depression": "SSRI (Sertraline/Fluoxetine), Therapy, Bupropion",
            "panic": "Breathing exercises, Benzodiazepines (acute), SSRI (chronic)",
            
            # GU / Repro
            "painful urination": "Antibiotics (Nitrofurantoin/Trimethoprim), Phenazopyridine",
            "yeast infection": "Fluconazole (oral), Miconazole (topical)",
            "menstrual cramps": "NSAIDs (Ibuprofen/Naproxen), Heat, OCPs",
            "ED": "Phosphodiesterase inhibitors (Sildenafil/Tadalafil)",
            "bph": "Tamsulosin, Finasteride",
            
            # Ophthalmology
            "red eye": "Artificial tears, Antibiotic drops (Erythromycin) if bacterial, Antihistamine drops",
            "dry eyes": "Artificial tears, Cyclosporine drops, Warm compress",
            "conjunctivitis": "Hygiene, Antibiotic drops (bacterial), Cool compress (viral)",
            
            # Endocrinology
            "hypoglycemia": "Oral Glucose, Glucagon, Dextrose IV",
            "hyperglycemia": "Insulin, Hydration",
            
            # Trauma
            "cut": "Clean with soap/water, Antibiotic ointment, Bandage, Tetanus shot",
            "sprain": "RICE (Rest, Ice, Compression, Elevation)",
            "strain": "RICE, NSAIDs"
        }

# -----------------------------------------------------------------------------
# 3. LOGIC ENGINE
# -----------------------------------------------------------------------------
class ClinicalEngine:
    """Handles logic for symptom analysis and triage."""
    
    def __init__(self, data: ClinicalData):
        self.data = data

    def analyze(self, text: str) -> Tuple[List[str], List[str], List[str], List[str]]:
        text_lower = text.lower()
        
        detected_symptoms = []
        etiologies = set()
        alerts = []
        treatments = []

        # Check for Critical Alerts
        for key, msg in self.data.ALERTS.items():
            if key in text_lower:
                alerts.append(msg)

        # Check for General Symptoms & Etiologies
        for symptom, causes in self.data.SYMPTOMS.items():
            if symptom in text_lower:
                detected_symptoms.append(symptom)
                etiologies.update(causes)
                
                # Check for Meds
                if symptom in self.data.MEDS:
                    treatments.append(f"**{symptom.title()}**: {self.data.MEDS[symptom]}")

        return (detected_symptoms, sorted(list(etiologies)), treatments, alerts)

# -----------------------------------------------------------------------------
# 4. UI COMPONENTS
# -----------------------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        # Use standard markdown for theme-adaptive text colors
        st.markdown(f"### {AppConfig.APP_ICON} {AppConfig.APP_TITLE}")
        st.caption(f"Version: {AppConfig.VERSION}")
        st.markdown("---")
        
        st.markdown("##### 📋 Triage Mode")
        st.info("System is ready for input.\nDatabase updated: current.")
        
        # REMOVED: Settings section as requested
        
def render_header():
    # Use standard elements that adapt to the theme
    st.title(AppConfig.APP_TITLE)
    st.markdown("Differential Diagnosis & Triage Protocol")

def render_results(symptoms, etiologies, treatments, alerts):
    # 1. Critical Alerts Section
    if alerts:
        st.subheader("🚨 Critical Notifications")
        for alert in alerts:
            st.markdown(f"""
            <div class="alert-box">
                <strong>ACTION REQUIRED</strong><br>
                {alert}
            </div>
            """, unsafe_allow_html=True)
            
    # 2. Main Grid
    if symptoms:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="medical-card">
                <h4>🔍 Differential Diagnosis</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if etiologies:
                for item in etiologies:
                    st.markdown(f"• {item}")
            else:
                st.caption("No specific etiology match found in local DB.")

        with col2:
            st.markdown("""
            <div class="medical-card">
                <h4>💊 Pharmacological Guide</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if treatments:
                for item in treatments:
                    st.markdown(f"• {item}")
            else:
                st.caption("No specific protocol available.")
            
    elif not alerts:
        st.warning("No clinical keywords detected. Please refine the description.")

# -----------------------------------------------------------------------------
# 5. MAIN APPLICATION
# -----------------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title=AppConfig.APP_TITLE,
        page_icon=AppConfig.APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject theme-adaptive CSS
    inject_css()
    
    # Initialize Engine
    kb = ClinicalData()
    engine = ClinicalEngine(kb)
    
    # Render Layout
    render_sidebar()
    render_header()
    
    # Session State for Clear Functionality
    if 'clinical_note' not in st.session_state:
        st.session_state.clinical_note = ""

    # Input Area
    st.markdown("### 📝 Patient Assessment")
    
    # Full width input area, removed metadata column
    user_text = st.text_area(
        "Clinical Notes", 
        value=st.session_state.clinical_note,
        height=150, 
        placeholder="Type symptoms here (e.g., patient presents with severe chest pain, sore throat, and dizziness...)",
        label_visibility="collapsed"
    )
    
    # Adjusted column ratios for buttons
    action_col1, action_col2 = st.columns([1, 6])
    with action_col1:
        # Use type="primary" for main action
        analyze_btn = st.button("Analyze Case", type="primary", use_container_width=True)
    with action_col2:
        if st.button("Reset Form", type="secondary"):
            st.session_state.clinical_note = ""
            st.rerun()

    st.markdown("---")

    # Processing Logic
    if analyze_btn and user_text:
        with st.spinner("Processing clinical tokens..."):
            time.sleep(0.5) # UX: Simulate computation time
            
            # Logic
            symptoms, causes, meds, alerts = engine.analyze(user_text)
            
            # Render
            render_results(symptoms, causes, meds, alerts)
            
            # Update state to keep text
            st.session_state.clinical_note = user_text

    # Professional Footer
    st.markdown("""
    <div class="footer">
        <strong>DISCLAIMER:</strong> This system is a demonstration tool for educational and development purposes only. 
        It is not a medical device and should not be used for actual diagnosis or treatment. 
        Always consult a qualified healthcare provider.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
