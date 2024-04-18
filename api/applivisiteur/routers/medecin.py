from fastapi import APIRouter, Depends, status, HTTPException
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    tags=['medecin']
)
get_db = database.get_db


@router.post('/create_medecin', response_model=schemas.Medecin)
def create_medecin(request: schemas.Medecin, db: Session = Depends(get_db)):
    """
    Crée un nouveau médecin.

    Params:
        request (schemas.Medecin): Données du médecin à créer.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        schemas.Medecin: Le médecin créé.
    """
    new_medecin = models.Medecin(MED_NOM=request.MED_NOM, MED_PRENOM=request.MED_PRENOM,
                                 MED_ADRESSE=request.MED_ADRESSE, MED_CP=request.MED_CP, MED_VILLE=request.MED_VILLE)
    db.add(new_medecin)
    db.commit()
    db.refresh(new_medecin)
    return new_medecin


@router.get('/medecin/{id}', response_model=schemas.showMedecin)
def get_user(id: int, db: Session = Depends(get_db)):
    """
    Récupère un médecin par ID.

    Params:
        id (int): ID du médecin à récupérer.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        schemas.showMedecin: Les détails du médecin.
    """
    medecin = db.query(models.Medecin).filter(
        models.Medecin.MED_ID == id).first()
    if not medecin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Médecin avec l'ID {id} non disponible")
    return medecin


@router.get('/medecins', response_model=List[schemas.showMedecin])
def all(db: Session = Depends(get_db)):
    """
    Récupère tous les médecins.

    Params:
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        List[schemas.showMedecin]: Liste de tous les médecins.
    """
    medecins = db.query(models.Medecin).all()
    if not medecins:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Aucun médecin trouvé")
    return medecins


@router.delete('/delete_medecin/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    """
    Supprime un médecin.

    Params:
        id (int): ID du médecin à supprimer.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        str: Message de confirmation de la suppression.
    """
    medecin = db.query(models.Medecin).filter(models.Medecin.MED_ID == id)

    if not medecin.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Médecin avec l'ID {id} non trouvé")
    medecin.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.put('/update_medecin/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Medecin, db: Session = Depends(get_db)):
    """
    Met à jour les informations d'un médecin.

    Params:
        id (int): ID du médecin à mettre à jour.
        request (schemas.Medecin): Données mises à jour du médecin.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        str: Message indiquant que la mise à jour a été effectuée.
    """
    medecin = db.query(models.Medecin).filter(models.Medecin.MED_ID == id)
    if not medecin.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Médecin avec l'ID {id} non trouvé")
    medecin.update(request.model_dump())
    db.commit()
    return 'updated'
