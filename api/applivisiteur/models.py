from sqlalchemy import Column, Integer, String, ForeignKey, Date
from .database import Base 
from sqlalchemy.orm import relationship


class Visiteur(Base):
    __tablename__ = "Visiteur"

    VIS_MATRICULE = Column(Integer, primary_key=True, index=True)
    VIS_NOM = Column(String)
    VIS_ADRESSE = Column(String)
    VIS_CP = Column(Integer)
    VIS_VILLE = Column(String)
    VIS_DATEEMBAUCHE = Column(Date)
    SEC_CODE = Column(String)
    LOG_LOGIN = Column(String)
    LOG_MDP = Column(String)
    VIS_ADMIN = Column(Integer)

class Secteur(Base):
    __tablename__ = "Secteur"

    SEC_CODE = Column(Integer, primary_key=True, index=True)
    SEC_LIBELLE = Column(String)

class Region(Base):
    __tablename__ = "Region"

    REG_CODE = Column(Integer, primary_key=True, index=True)
    REG_NOM = Column(String)
    SEC_CODE = Column(Integer, ForeignKey('Secteur.SEC_CODE'))

class Medecin(Base):
    __tablename__ = "Medecin"

    MED_ID = Column(Integer, primary_key=True, index=True)
    MED_NOM = Column(String)
    MED_PRENOM = Column(String)
    MED_ADRESSE = Column(String)
    MED_CP = Column(String)
    MED_VILLE = Column(String)
    TYP_ID = Column(String, ForeignKey('Type_Medecin.TYP_ID'))

    type = relationship('Type_Medecin',back_populates="medecin")

class Type_Medecin(Base):
    __tablename__ = "Type_Medecin"

    TYP_ID = Column(Integer, primary_key=True, index=True)
    TYP_LIBELLE = Column(String)
    TYP_LIEU = Column(String)

    medecin = relationship('Medecin', back_populates="type")

class Rapport_Visite(Base):
    __tablename__ = "Rapport_Visite"

    RAP_NUM = Column(Integer, primary_key=True, index=True)
    RAP_DATE = Column(String)
    RAP_BILAN = Column(String)
    RAP_MOTIF = Column(String)
    RAP_COMMENTAIRE = Column(String)
    VIS_MATRICULE = Column(String, ForeignKey('Visiteur.VIS_MATRICULE'))
    MED_ID = Column(Integer, ForeignKey('Medecin.MED_ID'))


class Medicaments(Base):
    __tablename__ = "Medicaments"

    MEDI_ID = Column(Integer, primary_key=True, index=True)
    MEDI_LABEL = Column(String)
    MEDI_Date = Column(Date)
    MEDI_COMPOSITION = Column(String)
    MEDI_EFFETS = Column(String)
    MEDI_CONTREINDIC = Column(String)
    MEDI_PRIX = Column(Integer)
    MEDI_STOCK = Column(String)

class Echantillons(Base):
    __tablename__ = "Echantillons"
    
    id = Column(Integer, primary_key=True, index=True)
    ECH_NOMBRE = Column(Integer)
    RAP_NUM = Column(Integer, ForeignKey('Rapport_Visite.RAP_NUM'))
    MEDI_ID = Column(Integer, ForeignKey('Medicaments.MEDI_ID'))