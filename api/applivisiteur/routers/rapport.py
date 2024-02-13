from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from typing import List

router = APIRouter(
    tags=['Rapport de visite']
)
get_db = database.get_db


@router.get('/rapports', response_model=List[schemas.showRapport])
def all(db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    medecins = db.query(models.Rapport_Visite).all()
    if not medecins:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error")
    return medecins


@router.get('/rapport/{id}', response_model=schemas.Rapport)
def get_rapport(id: int, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    rapport = db.query(models.Rapport_Visite).filter(
        models.Rapport_Visite.RAP_NUM == id).first()
    if not rapport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport with the id {id} is not available")
    return rapport


@router.get('/rapport/visiteur/{vis_id}', response_model=List[schemas.showRapport])
def get_rapport_by_vis_matricule(vis_id: int, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    rapport = db.query(models.Rapport_Visite).filter(
        models.Rapport_Visite.VIS_MATRICULE == vis_id)
    if not rapport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport created by {vis_id} is not available")
    return rapport


@router.post('/create_rapport', response_model=schemas.Rapport)
def create_rapport(request: schemas.Rapport, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    new_rapport = models.Rapport_Visite(RAP_DATE=request.RAP_DATE, RAP_BILAN=request.RAP_BILAN,
                                        RAP_MOTIF=request.RAP_MOTIF, RAP_COMMENTAIRE=request.RAP_COMMENTAIRE, MED_ID=request.MED_ID ,VIS_MATRICULE=request.VIS_MATRICULE)
    db.add(new_rapport)
    db.commit()
    db.refresh(new_rapport)
    return new_rapport


@router.delete('/delete_rapport/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    rapport = db.query(models.Rapport_Visite).filter(models.Rapport_Visite.RAP_NUM == id)

    if not rapport.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    rapport.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/update_rapport/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Rapport, db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    rapport = db.query(models.Rapport_Visite).filter(models.Rapport_Visite.RAP_NUM == id)
    if not rapport.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport with the id {id} not found")
    rapport.update(request.model_dump())
    db.commit()
    return 'done'

@router.get('/maxrapport', response_model=int)
def max_rapport(db: Session = Depends(get_db),current_user: schemas.Visiteur = Depends(oauth2.get_current_user)):
    max_rapport = db.query(func.max(models.Rapport_Visite.RAP_NUM)).scalar()
    if max_rapport is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Aucun rapport trouvé")
    return max_rapport