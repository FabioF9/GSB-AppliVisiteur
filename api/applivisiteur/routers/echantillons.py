from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..hashing import Hash

router = APIRouter(
    tags=['Echantillons']
)
get_db = database.get_db


@router.get('/echantillons', response_model=List[schemas.Echantillons])
def all(db: Session = Depends(get_db)):
    """
    Récupère tous les échantillons.

    Params:
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        List[schemas.Echantillons]: Liste des échantillons.
    """
    echantillons = db.query(models.Echantillons).all()
    if not echantillons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Aucun échantillon trouvé")
    return echantillons


@router.get('/echantillons/{id}', response_model=List[schemas.Echantillons])
def get_group(id: int, db: Session = Depends(get_db)):
    """
    Récupère un groupe d'échantillons par ID.

    Params:
        id (int): ID de groupe d'échantillons.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        List[schemas.Echantillons]: Liste des échantillons du groupe.
    """
    echantillons = db.query(models.Echantillons).filter(
        models.Echantillons.RAP_NUM == id).all()
    
    if not echantillons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Groupe d'échantillons avec l'ID {id} non disponible")
    return echantillons


@router.post('/add_echantillon', response_model=schemas.Echantillons)
def create_rapport(request: schemas.Echantillons, db: Session = Depends(get_db)):
    """
    Crée un nouvel échantillon.

    Params:
        request (schemas.Echantillons): Données de l'échantillon à créer.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        schemas.Echantillons: L'échantillon créé.
    """
    new_echantillon = models.Echantillons(ECH_NOMBRE=request.ECH_NOMBRE, RAP_NUM=request.RAP_NUM,
                                          MEDI_ID=request.MEDI_ID)
    db.add(new_echantillon)
    db.commit()
    db.refresh(new_echantillon)
    return new_echantillon


@router.put('/update_echantillon/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Echantillons, db: Session = Depends(get_db)):
    """
    Met à jour un échantillon existant.

    Params:
        id (int): ID de l'échantillon à mettre à jour.
        request (schemas.Echantillons): Données mises à jour de l'échantillon.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        str: Message indiquant la mise à jour effectuée.
    """
    echantillon = db.query(models.Echantillons).filter(models.Echantillons.RAP_NUM == id)
    if not echantillon.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport avec l'ID {id} non trouvé")
    echantillon.update(request.model_dump())
    db.commit()
    return 'done'


@router.get('/medicaments', response_model=List[schemas.Medicaments])
def all_medicaments(db: Session = Depends(get_db)):
    """
    Récupère tous les médicaments.

    Params:
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        List[schemas.Medicaments]: Liste des médicaments.
    """
    medicaments = db.query(models.Medicaments).all()
    if not medicaments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Aucun médicament trouvé")
    return medicaments
