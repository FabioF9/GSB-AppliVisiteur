from fastapi import APIRouter, Depends, status, HTTPException
from .. import database , schemas, models, oauth2
from sqlalchemy.orm import Session
from typing import List
from ..hashing import Hash

router = APIRouter(
    tags=['Visiteur']
)
get_db = database.get_db

@router.get('/visiteurs', response_model=List[schemas.showVisiteur] )
def all(db: Session = Depends(get_db)):
    visiteurs = db.query(models.Visiteur).all()
    if not visiteurs :
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error")
    return visiteurs

@router.post('/create_visiteur', response_model=schemas.Visiteur)
def create_visiteur(request: schemas.Visiteur, db: Session = Depends(get_db)):
    new_user = models.Visiteur(VIS_NOM=request.VIS_NOM, VIS_ADRESSE=request.VIS_ADRESSE, VIS_CP=request.VIS_CP, VIS_VILLE=request.VIS_VILLE, VIS_DATEEMBAUCHE = request.VIS_DATEEMBAUCHE, LOG_LOGIN=request.LOG_LOGIN, LOG_MDP=Hash.bcrypt(request.LOG_MDP), SEC_CODE = 1, VIS_ADMIN = 1)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 