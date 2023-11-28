from fastapi import APIRouter, Depends, status, HTTPException
from .. import database , schemas, models
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags=['Visiteur']
)
get_db = database.get_db

@router.post('/create_visiteur', response_model=schemas.ShowVisiteur)
def create_visiteur(request: schemas.Visiteur, db: Session = Depends(get_db)):
    new_visiteur = models.Visiteur(
        VIS_NOM=request.VIS_NOM,   
        LOG_LOGIN=request.LOG_LOGIN, 
        LOG_MDP=Hash.bcrypt(request.LOG_MDP),
        VIS_ADRESSE = "test",
        VIS_CP = "83000",
        VIS_VILLE = "TEST",
        )
    db.add(new_visiteur)
    db.commit()
    db.refresh(new_visiteur)
    return new_visiteur 

@router.get('/visiteur/{id}', response_model=schemas.ShowVisiteur)
def get_visiteur(id:int, db : Session = Depends(get_db)):
    visiteur = db.query(models.Visiteur).filter(models.Visiteur.id == id).first()
    if not visiteur:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return visiteur 