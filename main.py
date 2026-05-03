import streamlit as st
import xml.etree.ElementTree as ET
from fpdf import FPDF
import io

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Passerelle XML Optimum vers PDF", page_icon="📄")

# --- FONCTIONS UTILES ---
def parse_optimum_xml(uploaded_file):
    """
    Parse le fichier XML.
    Dans un vrai cas 'Optimum', on ciblerait des balises spécifiques
    (ex: <Vehicule>, <Dossier>, <MontantTTC>).
    Ici, on extrait génériquement les balises contenant du texte pour le prototype.
    """
    tree = ET.parse(uploaded_file)
    root = tree.getroot()

    extracted_data = {}
    # Parcours générique pour trouver les données (feuilles de l'arbre XML)
    for elem in root.iter():
        if elem.text and elem.text.strip() and len(elem) == 0:
            # On nettoie le nom de la balise (qui peut contenir des namespaces)
            tag_name = elem.tag.split('}')[-1]
            extracted_data[tag_name] = elem.text.strip()

    return extracted_data

def generate_pdf_template(data_dict):
    """
    Génère un PDF formaté avec les données extraites.
    Ceci est le 'template' que le système cible attend.
    """
    pdf = FPDF()
    pdf.add_page()

    # En-tête
    pdf.set_font("helvetica", style="B", size=16)
    pdf.cell(0, 10, "Fiche d'Exportation - Données Assureur", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)

    # Informations de traitement
    pdf.set_font("helvetica", style="I", size=10)
    pdf.cell(0, 10, "Ce document a été généré automatiquement depuis un flux XML Optimum.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Corps du document (Template dynamique basique)
    for key, value in data_dict.items():
        pdf.set_font("helvetica", style="B", size=10)
        # Nom du champ
        pdf.cell(60, 8, f"{key} : ", border=1)
        # Valeur du champ
        pdf.set_font("helvetica", size=10)
        # Multi_cell permet de gérer les textes longs
        pdf.multi_cell(0, 8, str(value), border=1, new_x="LMARGIN", new_y="NEXT")

    # Retourne le PDF sous forme d'octets (bytes)
    return bytes(pdf.output())

# --- INTERFACE UTILISATEUR STREAMLIT ---
st.title("📄 Export Optimum (XML) vers PDF")
st.markdown("Chargez le flux XML de votre assureur pour visualiser les données et générer le PDF normalisé.")

# 1. Zone de téléchargement du fichier XML
uploaded_file = st.file_uploader("Importer un fichier XML", type=["xml"])

if uploaded_file is not None:
    st.success("Fichier chargé avec succès !")

    try:
        # 2. Parsing et Affichage
        st.subheader("📊 Aperçu des données extraites")
        data = parse_optimum_xml(uploaded_file)

        if data:
            # Affichage sous forme de tableau interactif dans Streamlit
            st.dataframe([data], use_container_width=True)

            # 3. Bouton d'exportation PDF
            st.subheader("🖨️ Exportation vers le système cible")
            st.markdown("Générez le PDF respectant le template attendu par le système aval.")

            # Génération du PDF en mémoire
            pdf_bytes = generate_pdf_template(data)

            # Bouton de téléchargement natif Streamlit
            st.download_button(
                label="📥 Télécharger le PDF rempli",
                data=pdf_bytes,
                file_name="export_assureur_template.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Aucune donnée lisible n'a pu être extraite de ce fichier XML.")

    except Exception as e:
        st.error(f"Une erreur est survenue lors de la lecture du fichier XML : {e}")