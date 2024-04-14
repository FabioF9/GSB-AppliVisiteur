from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, models, token
from ..hashing import Hash
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Permet la connexion à l'api, afin d'être authentifier pour pouvoir utiliser les différentes routes de l'api.
    Si l'utilisateur n'est pas trouvé dans la base de donnée une exception 404 est levée
    Si le hash du mot de passe ne correspond pas à celui en base de donnée une exception 404 est levée
    Si l'utilisateur et le mot de passe sont corrects, création d'un token/jeton qui permet ensuite d'être authentifier par l'API
    """
    user = db.query(models.Visiteur).filter(
        models.Visiteur.LOG_LOGIN == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.LOG_MDP, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    # generate jwt token and return
    access_token_expires = token.timedelta(
        minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.LOG_LOGIN}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}, user.VIS_MATRICULE
