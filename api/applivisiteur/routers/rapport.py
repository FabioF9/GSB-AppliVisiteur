from fastapi import APIRouter, Depends, status, HTTPException
from .. import database , schemas, models, oauth2
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    tags=['Rapport de visite']
)
get_db = database.get_db

@router.get('/rapports', response_model=List[schemas.Rapport] )
def all(db: Session = Depends(get_db)):
    medecins = db.query(models.Rapport_Visite).all()
    if not medecins :
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error")
    return medecins

@router.post('/create_rapport', response_model=schemas.Rapport)
def create_medecin(request: schemas.Rapport, db: Session = Depends(get_db)):
    new_rapport = models.Rapport_Visite(RAP_DATE=request.RAP_DATE, RAP_BILAN=request.RAP_BILAN, RAP_MOTIF=request.RAP_MOTIF, RAP_COMMENTAIRE=request.RAP_COMMENTAIRE,user_id=1)
    db.add(new_rapport)
    db.commit()
    db.refresh(new_rapport)
    return new_rapport 