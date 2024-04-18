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
def all(db: Session = Depends(get_db)):
    """
    Récupère tous les rapports de visite.

    Params:
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        List[schemas.showRapport]: Liste de tous les rapports de visite.
    """
    rapports = db.query(models.Rapport_Visite).all()
    if not rapports:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Aucun rapport trouvé")
    return rapports


@router.get('/rapport/{id}', response_model=schemas.Rapport)
def get_rapport(id: int, db: Session = Depends(get_db)):
    """
    Récupère un rapport de visite par ID.

    Params:
        id (int): ID du rapport de visite à récupérer.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        schemas.Rapport: Détails du rapport de visite.
    """
    rapport = db.query(models.Rapport_Visite).filter(
        models.Rapport_Visite.RAP_NUM == id).first()
    if not rapport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport avec l'ID {id} non disponible")
    return rapport


@router.get('/rapport/visiteur/{vis_id}', response_model=List[schemas.showRapport])
def get_rapport_by_vis_matricule(vis_id: int, db: Session = Depends(get_db)):
    """
    Récupère les rapports de visite créés par un visiteur par son matricule.

    Params:
        vis_id (int): Matricule du visiteur.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        List[schemas.showRapport]: Liste des rapports de visite créés par le visiteur.
    """
    rapports = db.query(models.Rapport_Visite).filter(
        models.Rapport_Visite.VIS_MATRICULE == vis_id)
    if not rapports.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapports créés par {vis_id} non disponibles")
    return rapports


@router.post('/create_rapport', response_model=schemas.Rapport)
def create_rapport(request: schemas.Rapport, db: Session = Depends(get_db)):
    """
    Crée un nouveau rapport de visite.

    Params:
        request (schemas.Rapport): Données du rapport de visite à créer.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        schemas.Rapport: Le rapport de visite créé.
    """
    new_rapport = models.Rapport_Visite(RAP_DATE=request.RAP_DATE, RAP_BILAN=request.RAP_BILAN,
                                         RAP_MOTIF=request.RAP_MOTIF, RAP_COMMENTAIRE=request.RAP_COMMENTAIRE, MED_ID=request.MED_ID ,VIS_MATRICULE=request.VIS_MATRICULE)
    db.add(new_rapport)
    db.commit()
    db.refresh(new_rapport)
    return new_rapport


@router.delete('/delete_rapport/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    """
    Supprime un rapport de visite.

    Params:
        id (int): ID du rapport de visite à supprimer.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        str: Message de confirmation de la suppression.
    """
    rapport = db.query(models.Rapport_Visite).filter(models.Rapport_Visite.RAP_NUM == id)

    if not rapport.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport avec l'ID {id} non trouvé")
    rapport.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/update_rapport/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Rapport, db: Session = Depends(get_db)):
    """
    Met à jour un rapport de visite.

    Params:
        id (int): ID du rapport de visite à mettre à jour.
        request (schemas.Rapport): Données mises à jour du rapport de visite.
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        str: Message indiquant que la mise à jour a été effectuée.
    """
    rapport = db.query(models.Rapport_Visite).filter(models.Rapport_Visite.RAP_NUM == id)
    if not rapport.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Rapport avec l'ID {id} non trouvé")
    rapport.update(request.model_dump())
    db.commit()
    return 'done'

@router.get('/maxrapport', response_model=int)
def max_rapport(db: Session = Depends(get_db)):
    """
    Récupère le numéro maximum de rapport de visite.

    Params:
        db (Session): Session de la base de données.
        current_user (schemas.Visiteur): Utilisateur actuel.

    Returns:
        int: Numéro maximum de rapport de visite.
    """
    max_rapport = db.query(func.max(models.Rapport_Visite.RAP_NUM)).scalar()
    if max_rapport is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Aucun rapport trouvé")
    return max_rapport
