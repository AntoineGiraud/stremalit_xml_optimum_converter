import streamlit as st
from pathlib import Path

# Import de notre logique métier modularisée
from src.xml_parser import extract_darva_data
from src.pdf_gen import create_professional_pdf

# --- CONFIGURATION ---
st.set_page_config(page_title="Expertise Auto - Extracteur", layout="wide")

DEMO_FILE_PATH = "input/demo_optimum.xml"

# --- INTERFACE ---
st.title("🛡️ Connecteur Optimum / DARVA v2")
st.info(
    "Ce prototype extrait les données métier d'un flux XML et génère un PDF conforme pour l'atelier."
)

# --- SÉLECTION DE LA SOURCE DE DONNÉES ---
use_demo = st.toggle("🧪 Utiliser le fichier XML de démonstration", value=False)

xml_source = None
raw_xml_text = ""

if use_demo:
    # Mode DÉMO
    if Path(DEMO_FILE_PATH).exists():
        xml_source = DEMO_FILE_PATH
        # Lecture du texte brut pour l'affichage debug
        with open(DEMO_FILE_PATH, "r", encoding="utf-8", errors="ignore") as f:
            raw_xml_text = f.read()
    else:
        st.error(
            f"Fichier de démonstration introuvable à l'emplacement : {DEMO_FILE_PATH}"
        )
else:
    # Mode UPLOAD
    uploaded_file = st.file_uploader(
        "Déposez le fichier XML (Norme Darva)", type=["xml"]
    )
    if uploaded_file:
        xml_source = uploaded_file
        # Lecture du texte brut pour l'affichage debug (getvalue() extrait les bytes)
        raw_xml_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")

# --- TRAITEMENT ET AFFICHAGE ---
if xml_source:
    # Nouvel élément : L'expander pour le debug
    with st.expander("🛠️ Afficher le code XML brut (Debug)"):
        st.code(raw_xml_text, language="xml")

    try:
        # 1. Traitement Métier : Appel au parseur
        data = extract_darva_data(xml_source)
        # 2. Affichage UI (accès via l'objet Pydantic)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🚗 Véhicule & Sinistre")
            st.write(f"**Immat :** {data.immatriculation}")
            st.write(f"**Modèle :** {data.marque_modele}")
            st.write(f"**Dossier :** {data.ref_dossier}")

        with col2:
            st.subheader("👤 Client & Assurance")
            st.write(f"**Assuré :** {data.nom_assure}")
            st.write(f"**Franchise :** :red[{data.franchise}]")
            st.write(f"**Expert :** {data.expert}")

        st.divider()

        # 3. Traitement Métier
        pdf_output = create_professional_pdf(data)

        st.download_button(
            label="📄 Générer l'Ordre de Mission PDF",
            data=pdf_output,
            file_name=f"OM_{data.immatriculation}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    except Exception as e:
        st.error(f"Une erreur est survenue lors de l'analyse du XML : {e}")
