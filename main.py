import streamlit as st
import xml.etree.ElementTree as ET
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Expertise Auto - Extracteur DARVA", layout="wide")


class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.cell(
            0,
            10,
            "ORDRE DE MISSION - RÉPARATION COLLISION",
            border=True,
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(5)

    def section_title(self, label):
        self.set_font("helvetica", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, label, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)


# --- LOGIQUE D'EXTRACTION CIBLÉE ---
def extract_darva_data(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Helper pour extraire le texte sans erreur si la balise manque
    def get_txt(path, default="N/C"):
        node = root.find(path)
        return node.text if node is not None and node.text else default

    return {
        "Ref Dossier": get_txt(".//NumeroDossierAssureur"),
        "Date Sinistre": get_txt(".//DateSinistre"),
        "Nature": get_txt(".//NatureSinistre"),
        "Nom Assuré": f"{get_txt('.//Prenom')} {get_txt('.//Nom')}",
        "Ville": get_txt(".//Ville"),
        "Téléphone": get_txt(".//Telephone"),
        "Immatriculation": get_txt(".//Immatriculation"),
        "Marque/Modèle": f"{get_txt('.//Marque')} {get_txt('.//Modele')}",
        "Version": get_txt(".//Version"),
        "Franchise": f"{get_txt('.//Franchise/Montant')} EUR",
        "Instructions": get_txt(".//Instructions"),
        "Expert": get_txt(".//RaisonSociale"),
    }


def create_professional_pdf(data):
    pdf = PDF()
    pdf.add_page()

    # --- BLOC DOSSIER & SINISTRE ---
    pdf.section_title("1. INFORMATIONS DOSSIER")
    pdf.set_font("helvetica", size=10)
    col_width = 95
    pdf.cell(col_width, 7, f"N° Dossier Assureur : {data['Ref Dossier']}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Date du Sinistre : {data['Date Sinistre']}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(col_width, 7, f"Nature du choc : {data['Nature']}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Cabinet Expert : {data['Expert']}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(5)

    # --- BLOC CLIENT ---
    pdf.section_title("2. INFORMATIONS CLIENT / ASSURÉ")
    pdf.cell(col_width, 7, f"Nom : {data['Nom Assuré']}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Téléphone : {data['Téléphone']}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(
        0,
        7,
        f"Localisation : {data['Ville']}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(5)

    # --- BLOC VÉHICULE ---
    pdf.section_title("3. VÉHICULE")
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(
        0,
        8,
        f"Immatriculation : {data['Immatriculation']}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.set_font("helvetica", size=10)
    pdf.cell(col_width, 7, f"Marque/Modèle : {data['Marque/Modèle']}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Finition : {data['Version']}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(5)

    # --- CONDITIONS & INSTRUCTIONS ---
    pdf.section_title("4. CONDITIONS DE RÉPARATION")
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(
        0,
        7,
        f"FRANCHISE APPLICABLE : {data['Franchise']}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(2)
    pdf.set_font("helvetica", "I", 9)
    pdf.multi_cell(
        0, 6, f"Instructions particulières : {data['Instructions']}", border=1
    )

    return bytes(pdf.output())


# --- INTERFACE ---
st.title("🛡️ Connecteur Optimum / DARVA v2")
st.info(
    "Ce prototype extrait les données métier d'un flux XML et génère un PDF conforme pour l'atelier."
)

uploaded_file = st.file_uploader("Déposez le fichier XML (Norme Darva)", type=["xml"])

if uploaded_file:
    data = extract_darva_data(uploaded_file)

    # Affichage en colonnes pour un look pro
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

    # Génération du PDF
    pdf_output = create_professional_pdf(data)

    st.download_button(
        label="📄 Générer l'Ordre de Mission PDF",
        data=pdf_output,
        file_name=f"OM_{data['Immatriculation']}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
