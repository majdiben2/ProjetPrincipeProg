from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/authors", tags=["Auteurs"])


@router.get("", response_model=list[schemas.AuthorResponse])
def lister_auteurs(session: Session = Depends(get_db)):
    return session.query(models.Author).order_by(models.Author.id).all()


@router.get("/{auteur_id}", response_model=schemas.AuthorResponse)
def recuperer_auteur(auteur_id: int, session: Session = Depends(get_db)):
    auteur = session.get(models.Author, auteur_id)
    if not auteur:
        raise HTTPException(status_code=404, detail="Auteur introuvable")
    return auteur


@router.post("", response_model=schemas.AuthorResponse, status_code=status.HTTP_201_CREATED)
def creer_auteur(donnees: schemas.AuthorCreate, session: Session = Depends(get_db)):
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

    session.delete(auteur)
    session.commit()
    return {"message": "Auteur supprimé"}
