from fastapi import APIRouter, Depends, status, HTTPException
from .. import database , schemas, models, oauth2
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    tags=['medecin']
)
get_db = database.get_db

@router.post('/create_medecin', response_model=schemas.Medecin )
# def create_medecin(request: schemas.Medecin, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
def create_medecin(request: schemas.Medecin, db: Session = Depends(get_db)):
    new_medecin = models.Medecin(nom=request.nom, spe=request.spe, ville=request.ville)
    db.add(new_medecin)
    db.commit()
    db.refresh(new_medecin)
    return new_medecin 

@router.get('/medecin/{id}', response_model=schemas.Medecin )
def get_user(id:int, db : Session = Depends(get_db)):
    medecin = db.query(models.Medecin).filter(models.Medecin.id == id).first()
    if not medecin :
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Medecin with the id {id} is not available")
    return medecin 


@router.get('/medecins', response_model=List[schemas.Medecin] )
def all(db: Session = Depends(get_db)):
    medecins = db.query(models.Medecin).all()
    if not medecins :
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error")
    return medecins


@router.delete('/delete_medecin/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:Session = Depends(get_db)):
    medecin = db.query(models.Medecin).filter(models.Medecin.id ==id)

    if not medecin.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    medecin.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/update_medecin/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Medecin, db: Session = Depends(get_db)):
    medecin = db.query(models.Medecin).filter(models.Medecin.id == id)
    if not medecin.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found")
    medecin.update(request.model_dump())
    db.commit()
    return 'updated'