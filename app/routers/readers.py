from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/readers", tags=["Lecteurs"])


@router.get("", response_model=list[schemas.ReaderResponse])
def lister_lecteurs(session: Session = Depends(get_db)):
    return session.query(models.Reader).order_by(models.Reader.id).all()


@router.get("/{lecteur_id}", response_model=schemas.ReaderResponse)
def recuperer_lecteur(lecteur_id: int, session: Session = Depends(get_db)):
    lecteur = session.get(models.Reader, lecteur_id)
    if not lecteur:
        raise HTTPException(status_code=404, detail="Lecteur introuvable")
    return lecteur


@router.post("", response_model=schemas.ReaderResponse, status_code=status.HTTP_201_CREATED)
def creer_lecteur(donnees: schemas.ReaderCreate, session: Session = Depends(get_db)):
    # L'email identifie un lecteur : on évite les doublons avant insertion.
    lecteur_existant = session.query(models.Reader).filter(models.Reader.email == donnees.email).first()
    if lecteur_existant:
        raise HTTPException(status_code=409, detail="Un lecteur avec cet email existe déjà")

    lecteur = models.Reader(**donnees.model_dump())
    session.add(lecteur)
    session.commit()
    session.refresh(lecteur)
    return lecteur


@router.put("/{lecteur_id}", response_model=schemas.ReaderResponse)
def modifier_lecteur(lecteur_id: int, donnees: schemas.ReaderUpdate, session: Session = Depends(get_db)):
    lecteur = session.get(models.Reader, lecteur_id)
    if not lecteur:
        raise HTTPException(status_code=404, detail="Lecteur introuvable")

    modifications = donnees.model_dump(exclude_unset=True)
    if "email" in modifications:
        # On autorise le lecteur à garder son email actuel,
        # mais pas à prendre l'email d'un autre lecteur.
        lecteur_existant = (
            session.query(models.Reader)
            .filter(models.Reader.email == modifications["email"], models.Reader.id != lecteur_id)
            .first()
        )
        if lecteur_existant:
            raise HTTPException(status_code=409, detail="Un lecteur avec cet email existe déjà")

    for champ, valeur in modifications.items():
        setattr(lecteur, champ, valeur)

    session.commit()
    session.refresh(lecteur)
    return lecteur


@router.delete("/{lecteur_id}", response_model=schemas.MessageResponse)
def supprimer_lecteur(lecteur_id: int, session: Session = Depends(get_db)):
    lecteur = session.get(models.Reader, lecteur_id)
    if not lecteur:
        raise HTTPException(status_code=404, detail="Lecteur introuvable")

    # Avant de supprimer le lecteur, on remet en stock les livres de ses emprunts actifs.
    for emprunt in lecteur.borrows:
        if emprunt.status == "borrowed":
            emprunt.book.available_copies += 1

    # La carte et les emprunts du lecteur seront supprimés par cascade.
    session.delete(lecteur)
    session.commit()
    return {"message": "Lecteur supprimé"}
