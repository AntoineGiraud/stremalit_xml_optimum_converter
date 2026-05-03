from pydantic import BaseModel, Field, field_validator
from typing import Optional


class OrdreMission(BaseModel):
    ref_dossier: str = Field(..., description="Numéro de dossier de l'assureur")
    date_sinistre: str
    nature: str
    nom_assure: str
    ville: str
    telephone: str
    immatriculation: str
    marque_modele: str
    version: str
    franchise: str
    instructions: Optional[str] = "Aucune instruction particulière"
    expert: str

    # Exemple de validateur Pydantic : on s'assure que la plaque est en majuscules
    @field_validator("immatriculation")
    @classmethod
    def clean_immatriculation(cls, v: str) -> str:
        return v.upper().strip()
