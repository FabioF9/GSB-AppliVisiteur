from sqlalchemy import Column, Integer, String, ForeignKey, Date
from .database import Base 
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship ('Blog', back_populates="creator")
    rapportvisite = relationship('Rapport_Visite', back_populates="creator_rapvisite")

class Medecin(Base):
    __tablename__ = "medecin"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    spe = Column(String)
    ville = Column(String)

class RapportVisite(Base):
    __tablename__ = "Rapport_Visite"

    RAP_NUM = Column(Integer, primary_key=True, index=True)
    RAP_DATE = Column(Date)
    RAP_BILAN = Column(String)
    RAP_MOTIF = Column(String)
    RAP_COMMENTAIRE = Column(String)
    VIS_MATRICULE = Column (Integer,ForeignKey('users.id'))

    creator_rapvisite = relationship("User", back_populates="rapportvisite")