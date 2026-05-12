from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/cards", tags=["Cartes"])


@router.get("", response_model=list[schemas.LibraryCardResponse])
def lister_cartes(session: Session = Depends(get_db)):
    return session.query(models.LibraryCard).order_by(models.LibraryCard.id).all()


@router.get("/{carte_id}", response_model=schemas.LibraryCardResponse)
def recuperer_carte(carte_id: int, session: Session = Depends(get_db)):
    carte = session.get(models.LibraryCard, carte_id)
    if not carte:
        raise HTTPException(status_code=404, detail="Carte introuvable")
    return carte


@router.post("", response_model=schemas.LibraryCardResponse, status_code=status.HTTP_201_CREATED)
def creer_carte(donnees: schemas.LibraryCardCreate, session: Session = Depends(get_db)):
    # La carte doit obligatoirement être associée à un lecteur existant.
    lecteur = session.get(models.Reader, donnees.reader_id)
    if not lecteur:
        raise HTTPException(status_code=404, detail="Lecteur introuvable")

    # Relation one-to-one : un lecteur ne peut avoir qu'une seule carte.
    if lecteur.card:
        raise HTTPException(status_code=409, detail="Ce lecteur possède déjà une carte")

    # Le numéro de carte est unique dans toute la bibliothèque.
    numero_existant = (
        session.query(models.LibraryCard)
        .filter(models.LibraryCard.card_number == donnees.card_number)
        .first()
    )
    if numero_existant:
        raise HTTPException(status_code=409, detail="Ce numéro de carte existe déjà")

    carte = models.LibraryCard(**donnees.model_dump())
    session.add(carte)
    session.commit()
    session.refresh(carte)
    return carte


@router.put("/{carte_id}", response_model=schemas.LibraryCardResponse)
def modifier_carte(carte_id: int, donnees: schemas.LibraryCardUpdate, session: Session = Depends(get_db)):
    carte = session.get(models.LibraryCard, carte_id)
    if not carte:
        raise HTTPException(status_code=404, detail="Carte introuvable")

    modifications = donnees.model_dump(exclude_unset=True)
    if "card_number" in modifications:
        # On vérifie que le nouveau numéro n'est pas déjà utilisé par une autre carte.
        numero_existant = (
            session.query(models.LibraryCard)
            .filter(
                models.LibraryCard.card_number == modifications["card_number"],
                models.LibraryCard.id != carte_id,
            )
            .first()
        )
        if numero_existant:
            raise HTTPException(status_code=409, detail="Ce numéro de carte existe déjà")

    if "reader_id" in modifications:
        lecteur = session.get(models.Reader, modifications["reader_id"])
        if not lecteur:
            raise HTTPException(status_code=404, detail="Lecteur introuvable")
        # Même en modification, on conserve la règle : une seule carte par lecteur.
        carte_existante = (
            session.query(models.LibraryCard)
            .filter(
                models.LibraryCard.reader_id == modifications["reader_id"],
                models.LibraryCard.id != carte_id,
            )
            .first()
        )
        if carte_existante:
            raise HTTPException(status_code=409, detail="Ce lecteur possède déjà une carte")

    for champ, valeur in modifications.items():
        setattr(carte, champ, valeur)

    session.commit()
    session.refresh(carte)
    return carte


@router.delete("/{carte_id}", response_model=schemas.MessageResponse)
def supprimer_carte(carte_id: int, session: Session = Depends(get_db)):
    carte = session.get(models.LibraryCard, carte_id)
    if not carte:
        raise HTTPException(status_code=404, detail="Carte introuvable")

    session.delete(carte)
    session.commit()
    return {"message": "Carte supprimée"}
