from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

# Toutes les routes de ce fichier commenceront par /authors
# et seront regroupées sous le tag "Auteurs" dans Swagger.
router = APIRouter(prefix="/authors", tags=["Auteurs"])

# GET /authors
@router.get("", response_model=list[schemas.AuthorResponse])
def lister_auteurs(session: Session = Depends(get_db)):
    return session.query(models.Author).order_by(models.Author.id).all() # requte SQL sur la table auteur tri par id on recupere tous les resultats


@router.get("/{auteur_id}", response_model=schemas.AuthorResponse)
def recuperer_auteur(auteur_id: int, session: Session = Depends(get_db)):
    auteur = session.get(models.Author, auteur_id)
    if not auteur:
        raise HTTPException(status_code=404, detail="Auteur introuvable")
    return auteur


@router.post("", response_model=schemas.AuthorResponse, status_code=status.HTTP_201_CREATED)
def creer_auteur(donnees: schemas.AuthorCreate, session: Session = Depends(get_db)):
    # model_dump() transforme le schéma Pydantic en dictionnaire
    # utilisable directement par le modèle SQLAlchemy.
    auteur = models.Author(**donnees.model_dump())
    session.add(auteur)
    session.commit()
    session.refresh(auteur)
    return auteur


@router.put("/{auteur_id}", response_model=schemas.AuthorResponse)
def modifier_auteur(auteur_id: int, donnees: schemas.AuthorUpdate, session: Session = Depends(get_db)):
    auteur = session.get(models.Author, auteur_id)
    if not auteur:
        raise HTTPException(status_code=404, detail="Auteur introuvable")

    # exclude_unset=True permet de modifier uniquement les champs envoyés.
    for champ, valeur in donnees.model_dump(exclude_unset=True).items():
        setattr(auteur, champ, valeur)

    session.commit()
    session.refresh(auteur)
    return auteur


@router.delete("/{auteur_id}", response_model=schemas.MessageResponse)
def supprimer_auteur(auteur_id: int, session: Session = Depends(get_db)):
    auteur = session.get(models.Author, auteur_id)
    if not auteur:
        raise HTTPException(status_code=404, detail="Auteur introuvable")

    # Les livres liés à cet auteur sont supprimés par cascade dans le modèle.
    session.delete(auteur)
    session.commit()
    return {"message": "Auteur supprimé"}
