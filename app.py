import streamlit as st

# Import de notre logique métier modularisée
from src.xml_parser import extract_darva_data
from src.pdf_gen import create_professional_pdf

# --- CONFIGURATION ---
st.set_page_config(page_title="Expertise Auto - Extracteur", layout="wide")

# --- INTERFACE ---
st.title("🛡️ Connecteur Optimum / DARVA v2")
st.info(
    "Ce prototype extrait les données métier d'un flux XML et génère un PDF conforme pour l'atelier."
)

# Zone d'upload
uploaded_file = st.file_uploader("Déposez le fichier XML (Norme Darva)", type=["xml"])

if uploaded_file:
    # 1. Traitement Métier : Appel au parseur
    data = extract_darva_data(uploaded_file)

    # 2. Affichage UI
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚗 Véhicule & Sinistre")
        st.write(f"**Immat :** {data['Immatriculation']}")
        st.write(f"**Modèle :** {data['Marque/Modèle']}")
        st.write(f"**Dossier :** {data['Ref Dossier']}")

    with col2:
        st.subheader("👤 Client & Assurance")
        st.write(f"**Assuré :** {data['Nom Assuré']}")
        st.write(f"**Franchise :** :red[{data['Franchise']}]")
        st.write(f"**Expert :** {data['Expert']}")

    st.divider()

    # 3. Traitement Métier : Appel au générateur PDF
    pdf_output = create_professional_pdf(data)

    # Bouton de téléchargement
    st.download_button(
        label="📄 Générer l'Ordre de Mission PDF",
        data=pdf_output,
        file_name=f"OM_{data['Immatriculation']}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
