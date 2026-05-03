from fpdf import FPDF
from typing import Dict


class PDF(FPDF):
    """Classe héritée pour surcharger l'en-tête du document."""

    def header(self) -> None:
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

    def section_title(self, label: str) -> None:
        self.set_font("helvetica", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, label, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)


def create_professional_pdf(data: Dict[str, str]) -> bytes:
    """
    Génère un PDF structuré à partir d'un dictionnaire de données.

    Args:
        data: Dictionnaire contenant les informations de la mission.

    Returns:
        Les octets (bytes) constituant le fichier PDF.
    """
    pdf = PDF()
    pdf.add_page()

    # --- BLOC DOSSIER & SINISTRE ---
    pdf.section_title("1. INFORMATIONS DOSSIER")
    pdf.set_font("helvetica", size=10)
    col_width = 95
    pdf.cell(
        col_width, 7, f"N° Dossier Assureur : {data.get('Ref Dossier', '')}", border="B"
    )
    pdf.cell(
        col_width,
        7,
        f"Date du Sinistre : {data.get('Date Sinistre', '')}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(col_width, 7, f"Nature du choc : {data.get('Nature', '')}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Cabinet Expert : {data.get('Expert', '')}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(5)

    # --- BLOC CLIENT ---
    pdf.section_title("2. INFORMATIONS CLIENT / ASSURÉ")
    pdf.cell(col_width, 7, f"Nom : {data.get('Nom Assuré', '')}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Téléphone : {data.get('Téléphone', '')}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(
        0,
        7,
        f"Localisation : {data.get('Ville', '')}",
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
        f"Immatriculation : {data.get('Immatriculation', '')}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.set_font("helvetica", size=10)
    pdf.cell(
        col_width, 7, f"Marque/Modèle : {data.get('Marque/Modèle', '')}", border="B"
    )
    pdf.cell(
        col_width,
        7,
        f"Finition : {data.get('Version', '')}",
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
        f"FRANCHISE APPLICABLE : {data.get('Franchise', '')}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(2)
    pdf.set_font("helvetica", "I", 9)
    pdf.multi_cell(
        0, 6, f"Instructions particulières : {data.get('Instructions', '')}", border=1
    )

    return bytes(pdf.output())
