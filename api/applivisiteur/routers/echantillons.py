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
def all(db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    echantillons = db.query(models.Echantillons).all()
    if not echantillons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error")
    return echantillons

@router.get('/echantillons/{id}', response_model=List[schemas.Echantillons])
def get_group(id: int, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    echantillons = db.query(models.Echantillons).filter(
        models.Echantillons.RAP_NUM == id).all()
    
    if not echantillons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Echantillon Group with the id {id} is not available")
    return echantillons

@router.post('/add_echantillon', response_model=schemas.Echantillons)
def create_rapport(request: schemas.Echantillons, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    new_echantillon = models.Echantillons(ECH_NOMBRE=request.ECH_NOMBRE, RAP_NUM=request.RAP_NUM,
                                        MEDI_ID=request.MEDI_ID)
    db.add(new_echantillon)
    db.commit()
    db.refresh(new_echantillon)
    return new_echantillon

@router.put('/update_echantillon/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Echantillons, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    echantillon = db.query(models.Echantillons).filter(models.Echantillons.RAP_NUM == id)
    if not echantillon.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport with the id {id} not found")
    echantillon.update(request.model_dump())
    db.commit()
    return 'done'


@router.get('/medicaments', response_model=List[schemas.Medicaments])
def all_medicaments(db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    medicaments = db.query(models.Medicaments).all()
    if not medicaments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error")
    return medicaments
