import xml.etree.ElementTree as ET
from typing import IO, Dict, Union


def extract_darva_data(xml_source: Union[IO[bytes], str]) -> Dict[str, str]:
    """
    Extrait les données métier d'un flux XML DARVA/Optimum.

    Args:
        xml_source: Un chemin de fichier (str) ou un objet fichier binaire (Streamlit upload).

    Returns:
        Un dictionnaire contenant les paires "Clé métier": "Valeur".
    """
    tree = ET.parse(xml_source)
    root = tree.getroot()

    # Fonction interne pour sécuriser l'extraction
    def get_txt(path: str, default: str = "N/C") -> str:
        node = root.find(path)
        return node.text if node is not None and node.text else default

    # Remarque : Pydantic viendra parfaitement remplacer ce dictionnaire plus tard !
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
        "Franchise": f"{get_txt('.//Franchise/Montant')} EUR",  # Remplacement du symbole €
        "Instructions": get_txt(".//Instructions"),
        "Expert": get_txt(".//RaisonSociale"),
    }
