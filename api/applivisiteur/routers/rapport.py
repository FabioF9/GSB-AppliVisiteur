from fastapi import APIRouter, Depends, status, HTTPException
from .. import database , schemas, models, oauth2
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    tags=['Rapport de visite']
)
get_db = database.get_db

@router.get('/rapports', response_model=List[schemas.showRapport] )
def all(db: Session = Depends(get_db)):
    medecins = db.query(models.Rapport_Visite).all()
    if not medecins :
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error")
    return medecins


@router.get('/rapport/{id}', response_model=schemas.Rapport )
def get_rapport(id:int, db : Session = Depends(get_db)):
    rapport = db.query(models.Rapport_Visite).filter(models.Rapport_Visite.RAP_NUM == id).first()
    if not rapport :
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport with the id {id} is not available")
    return rapport 

@router.get('/rapport/visiteur/{vis_id}', response_model=schemas.Rapport )
def get_rapport_by_vis_matricule(vis_id:int, db : Session = Depends(get_db)):
    rapport = db.query(models.Rapport_Visite).filter(models.Rapport_Visite.VIS_MATRICULE == vis_id).first()
    if not rapport :
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport created by {vis_id} is not available")
    return rapport 

@router.post('/create_rapport', response_model=schemas.Rapport)
def create_rapport(request: schemas.Rapport, db: Session = Depends(get_db)):
    new_rapport = models.Rapport_Visite(RAP_DATE=request.RAP_DATE, RAP_BILAN=request.RAP_BILAN, RAP_MOTIF=request.RAP_MOTIF, RAP_COMMENTAIRE=request.RAP_COMMENTAIRE,VIS_MATRICULE=1)
    db.add(new_rapport)
    db.commit()
    db.refresh(new_rapport)
    return new_rapport 