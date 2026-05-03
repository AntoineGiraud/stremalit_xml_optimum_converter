import pytest
import io
from pydantic import ValidationError

from src.models import OrdreMission
from src.xml_parser import extract_darva_data
from src.pdf_gen import create_professional_pdf

# --- FIXTURES (Données de test) ---


@pytest.fixture
def mock_xml_content() -> str:
    """Un XML minimaliste respectant les chemins XPath de notre parseur."""
    return """<?xml version="1.0" encoding="ISO-8859-1"?>
    <FluxDarva>
        <NumeroDossierAssureur>DOS-2026-TEST</NumeroDossierAssureur>
        <DateSinistre>2026-05-01</DateSinistre>
        <NatureSinistre>CHOC_AVANT</NatureSinistre>
        <Prenom>Jean</Prenom>
        <Nom>Testeur</Nom>
        <Ville>BORDEAUX</Ville>
        <Telephone>0612345678</Telephone>
        <Immatriculation>ab-123-cd</Immatriculation>
        <Marque>PEUGEOT</Marque>
        <Modele>308</Modele>
        <Version>ALLURE</Version>
        <Franchise><Montant>250.00</Montant></Franchise>
        <Instructions>Faire vite</Instructions>
        <RaisonSociale>CABINET EXPERT</RaisonSociale>
    </FluxDarva>
    """


@pytest.fixture
def valid_mission_data() -> OrdreMission:
    """Un objet OrdreMission valide pour tester le générateur PDF."""
    return OrdreMission(
        ref_dossier="DOS-123",
        date_sinistre="2026-01-01",
        nature="TEST",
        nom_assure="Jean Dupont",
        ville="Paris",
        telephone="0600000000",
        immatriculation="XX-999-YY",
        marque_modele="Renault Clio",
        version="Zen",
        franchise="200 EUR",
        expert="Expertise Auto",
    )


# --- TESTS : MODÈLES PYDANTIC ---


def test_ordre_mission_validation_immatriculation():
    """Vérifie que la plaque est bien mise en majuscules par le validateur."""
    mission = OrdreMission(
        ref_dossier="123",
        date_sinistre="2026",
        nature="Choc",
        nom_assure="Doe",
        ville="Bdx",
        telephone="06",
        immatriculation=" yy-123-zz ",  # Minuscules + espaces
        marque_modele="Test",
        version="V1",
        franchise="0",
        expert="Exp",
    )
    assert mission.immatriculation == "YY-123-ZZ"


def test_ordre_mission_missing_field():
    """Vérifie que Pydantic lève une erreur si un champ obligatoire manque."""
    with pytest.raises(ValidationError):
        # Il manque volontairement 'ref_dossier'
        OrdreMission(
            date_sinistre="2026",
            nature="Choc",
            nom_assure="Doe",
            ville="Bdx",
            telephone="06",
            immatriculation="XX-123-YY",
            marque_modele="Test",
            version="V1",
            franchise="0",
            expert="Exp",
        )


# --- TESTS : PARSER XML ---


def test_extract_darva_data(mock_xml_content):
    """Vérifie que le parseur lit correctement le XML et retourne le bon modèle."""
    # On simule un fichier avec io.StringIO
    xml_file_like = io.StringIO(mock_xml_content)

    result = extract_darva_data(xml_file_like)

    assert isinstance(result, OrdreMission)
    assert result.ref_dossier == "DOS-2026-TEST"
    assert result.nom_assure == "Jean Testeur"
    # Vérification que le nettoyage de plaque a bien opéré pendant le parsing
    assert result.immatriculation == "AB-123-CD"
    assert result.franchise == "250.00 EUR"


# --- TESTS : GÉNÉRATION PDF ---


def test_create_professional_pdf(valid_mission_data):
    """Vérifie que la fonction retourne bien des octets au format PDF."""
    pdf_bytes = create_professional_pdf(valid_mission_data)

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # Le "Magic Number" d'un fichier PDF est "%PDF-"
    assert pdf_bytes.startswith(b"%PDF-")
