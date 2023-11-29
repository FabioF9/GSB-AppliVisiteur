from typing import List
from pydantic import BaseModel


class Medecin(BaseModel):
    MED_NOM : str
    MED_PRENOM : str
    MED_ADRESSE : str
    MED_CP : str
    MED_VILLE : str

class Rapport(BaseModel):
    # RAP_NUM : int
    RAP_DATE : str
    RAP_BILAN : str
    RAP_MOTIF : str
    RAP_COMMENTAIRE : str
    # user_id : int

class Visiteur (BaseModel):

    VIS_NOM : str
    VIS_ADRESSE : str 
    VIS_CP : int
    VIS_VILLE : str
    LOG_LOGIN : str
    LOG_MDP : str

class showVisiteur(BaseModel):
    LOG_LOGIN : str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None