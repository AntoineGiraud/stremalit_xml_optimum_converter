from fpdf import FPDF
from src.models import OrdreMission


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


def create_professional_pdf(data: OrdreMission) -> bytes:
    """Génère un PDF structuré à partir du modèle Pydantic."""
    pdf = PDF()
    pdf.add_page()

    pdf.section_title("1. INFORMATIONS DOSSIER")
    pdf.set_font("helvetica", size=10)
    col_width = 95
    pdf.cell(col_width, 7, f"N° Dossier Assureur : {data.ref_dossier}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Date du Sinistre : {data.date_sinistre}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(col_width, 7, f"Nature du choc : {data.nature}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Cabinet Expert : {data.expert}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(5)

    pdf.section_title("2. INFORMATIONS CLIENT / ASSURÉ")
    pdf.cell(col_width, 7, f"Nom : {data.nom_assure}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Téléphone : {data.telephone}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(
        0, 7, f"Localisation : {data.ville}", border="B", new_x="LMARGIN", new_y="NEXT"
    )
    pdf.ln(5)

    pdf.section_title("3. VÉHICULE")
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(
        0, 8, f"Immatriculation : {data.immatriculation}", new_x="LMARGIN", new_y="NEXT"
    )
    pdf.set_font("helvetica", size=10)
    pdf.cell(col_width, 7, f"Marque/Modèle : {data.marque_modele}", border="B")
    pdf.cell(
        col_width,
        7,
        f"Finition : {data.version}",
        border="B",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(5)

    pdf.section_title("4. CONDITIONS DE RÉPARATION")
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(
        0, 7, f"FRANCHISE APPLICABLE : {data.franchise}", new_x="LMARGIN", new_y="NEXT"
    )
    pdf.ln(2)
    pdf.set_font("helvetica", "I", 9)
    pdf.multi_cell(0, 6, f"Instructions : {data.instructions}", border=1)

    return bytes(pdf.output())
