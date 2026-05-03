import xml.etree.ElementTree as ET
from typing import IO, Union
from src.models import OrdreMission


def extract_darva_data(xml_source: Union[IO[bytes], str]) -> OrdreMission:
    """
    Extrait les données et retourne un modèle Pydantic validé.
    """
    tree = ET.parse(xml_source)
    root = tree.getroot()

    def get_txt(path: str, default: str = "N/C") -> str:
        node = root.find(path)
        return node.text if node is not None and node.text else default

    # Instanciation et validation automatique par Pydantic
    return OrdreMission(
        ref_dossier=get_txt(".//NumeroDossierAssureur"),
        date_sinistre=get_txt(".//DateSinistre"),
        nature=get_txt(".//NatureSinistre"),
        nom_assure=f"{get_txt('.//Prenom')} {get_txt('.//Nom')}",
        ville=get_txt(".//Ville"),
        telephone=get_txt(".//Telephone"),
        immatriculation=get_txt(".//Immatriculation"),
        marque_modele=f"{get_txt('.//Marque')} {get_txt('.//Modele')}",
        version=get_txt(".//Version"),
        franchise=f"{get_txt('.//Franchise/Montant')} EUR",
        instructions=get_txt(".//Instructions"),
        expert=get_txt(".//RaisonSociale"),
    )
