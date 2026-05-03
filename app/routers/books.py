from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/books", tags=["Livres"])


@router.get("", response_model=list[schemas.BookResponse])
def lister_livres(session: Session = Depends(get_db)):
    return session.query(models.Book).order_by(models.Book.id).all()


@router.get("/available", response_model=list[schemas.BookResponse])
def lister_livres_disponibles(session: Session = Depends(get_db)):
    return (
        session.query(models.Book)
        .filter(models.Book.available_copies > 0)
        .order_by(models.Book.id)
        .all()
    )


@router.get("/{livre_id}", response_model=schemas.BookResponse)
def recuperer_livre(livre_id: int, session: Session = Depends(get_db)):
    livre = session.get(models.Book, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return livre


@router.post("", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def creer_livre(donnees: schemas.BookCreate, session: Session = Depends(get_db)):
    auteur = session.get(models.Author, donnees.author_id)
    if not auteur:
        raise HTTPException(status_code=404, detail="Auteur introuvable")

    livre_existant = session.query(models.Book).filter(models.Book.isbn == donnees.isbn).first()
    if livre_existant:
        raise HTTPException(status_code=409, detail="Un livre avec cet ISBN existe déjà")

    livre = models.Book(**donnees.model_dump())
    session.add(livre)
    session.commit()
    session.refresh(livre)
    return livre


@router.put("/{livre_id}", response_model=schemas.BookResponse)
def modifier_livre(livre_id: int, donnees: schemas.BookUpdate, session: Session = Depends(get_db)):
    livre = session.get(models.Book, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable")

    modifications = donnees.model_dump(exclude_unset=True)

    if "author_id" in modifications and not session.get(models.Author, modifications["author_id"]):
        raise HTTPException(status_code=404, detail="Auteur introuvable")

    if "isbn" in modifications:
        livre_existant = (
            session.query(models.Book)
            .filter(models.Book.isbn == modifications["isbn"], models.Book.id != livre_id)
            .first()
        )
        if livre_existant:
            raise HTTPException(status_code=409, detail="Un livre avec cet ISBN existe déjà")

    for champ, valeur in modifications.items():
        setattr(livre, champ, valeur)

    session.commit()
    session.refresh(livre)
    return livre


@router.delete("/{livre_id}", response_model=schemas.MessageResponse)
def supprimer_livre(livre_id: int, session: Session = Depends(get_db)):
    livre = session.get(models.Book, livre_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable")

    session.delete(livre)
    session.commit()
    return {"message": "Livre supprimé"}
