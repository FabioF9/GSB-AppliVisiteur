from typing import List
from datetime import datetime, date
from pydantic import BaseModel


class Medecin(BaseModel):
    MED_NOM: str
    MED_PRENOM: str
    MED_ADRESSE: str
    MED_CP: str
    MED_VILLE: str

class showMedecin(BaseModel):
    MED_ID : int
    MED_NOM: str
    MED_PRENOM: str
    MED_ADRESSE: str
    MED_CP: str
    MED_VILLE: str


class Rapport(BaseModel):
    # RAP_NUM : int
    RAP_DATE: date
    RAP_BILAN: str
    RAP_MOTIF: str
    RAP_COMMENTAIRE: str
    MED_ID : int
    VIS_MATRICULE : int


class Visiteur (BaseModel):

    VIS_NOM: str
    VIS_ADRESSE: str
    VIS_CP: int
    VIS_VILLE: str
    VIS_DATEEMBAUCHE: date
    LOG_LOGIN: str
    LOG_MDP: str


class showVisiteur(BaseModel):
    LOG_LOGIN: str
    rapport: List[Rapport] = []


class showRapportCreator(BaseModel):

    VIS_MATRICULE: int
    VIS_NOM: str
    VIS_ADRESSE: str
    VIS_CP: int
    VIS_VILLE: str
    VIS_DATEEMBAUCHE: date

class showRapportMedecin(BaseModel):
    MED_NOM: str

class showRapport (BaseModel):
    RAP_NUM: int
    RAP_DATE: date
    RAP_BILAN: str
    RAP_MOTIF: str
    RAP_COMMENTAIRE: str

    creator: showRapportCreator
    affiliate_med : showRapportMedecin


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
