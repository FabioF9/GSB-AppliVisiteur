from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..hashing import Hash

router = APIRouter(
    tags=['Visiteur']
)
get_db = database.get_db


@router.get('/visiteurs', response_model=List[schemas.showVisiteur])
def all(db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    visiteurs = db.query(models.Visiteur).all()
    if not visiteurs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error")
    return visiteurs

@router.get('/visiteur/{id}', response_model=schemas.showVisiteur)
def get_user(id: int, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    visiteur = db.query(models.Visiteur).filter(
        models.Visiteur.VIS_MATRICULE == id).first()
    if not visiteur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Visiteur with the id {id} is not available")

    # Compte le nombre de rapports associés à ce visiteur
    rapport_count = db.query(func.count(models.Rapport_Visite.RAP_NUM)).filter(
        models.Rapport_Visite.VIS_MATRICULE == id).scalar()

    # Ajoute le compte des rapports à l'objet visiteur
    visiteur.RAPPORT_COUNT = rapport_count

    return visiteur


@router.post('/create_visiteur', response_model=schemas.Visiteur)
def create_visiteur(request: schemas.Visiteur, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    new_user = models.Visiteur(VIS_NOM=request.VIS_NOM, VIS_ADRESSE=request.VIS_ADRESSE, VIS_CP=request.VIS_CP, VIS_VILLE=request.VIS_VILLE,
                               VIS_DATEEMBAUCHE=request.VIS_DATEEMBAUCHE, LOG_LOGIN=request.LOG_LOGIN, LOG_MDP=Hash.bcrypt(request.LOG_MDP), SEC_CODE=1, VIS_ADMIN=1)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/visiteurgroup/{id}', response_model=List[schemas.showVisiteurGroup])
def get_group(id: int, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    visiteurs = db.query(models.Visiteur).filter(
        models.Visiteur.VIS_ADMINR_ID == id).all()
    
    if not visiteurs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Visiteur Group with the id {id} is not available")

    # Compte le nombre total de rapports pour tous les visiteurs du groupe
    total_rapport_count = db.query(func.count(models.Rapport_Visite.RAP_NUM)).filter(
        models.Rapport_Visite.VIS_MATRICULE.in_([v.VIS_MATRICULE for v in visiteurs])
    ).scalar()

    # Ajoute le compte des rapports à chaque objet visiteur du groupe
    for visiteur in visiteurs:
        rapport_count = db.query(func.count(models.Rapport_Visite.RAP_NUM)).filter(
            models.Rapport_Visite.VIS_MATRICULE == visiteur.VIS_MATRICULE
        ).scalar()
        visiteur.RAPPORT_COUNT = rapport_count

    # Ajoute le total des rapports au résultat pour le groupe
    for visiteur in visiteurs:
        visiteur.TOTAL_RAPPORT_COUNT = total_rapport_count

    return visiteurs