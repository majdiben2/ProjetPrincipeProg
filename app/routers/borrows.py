from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/borrows", tags=["Emprunts"])


@router.get("", response_model=list[schemas.BorrowResponse])
def lister_emprunts(session: Session = Depends(get_db)):
    return session.query(models.Borrow).order_by(models.Borrow.id).all()


@router.get("/{emprunt_id}", response_model=schemas.BorrowResponse)
def recuperer_emprunt(emprunt_id: int, session: Session = Depends(get_db)):
    emprunt = session.get(models.Borrow, emprunt_id)
    if not emprunt:
        raise HTTPException(status_code=404, detail="Emprunt introuvable")
    return emprunt


@router.post("", response_model=schemas.BorrowResponse, status_code=status.HTTP_201_CREATED)
def creer_emprunt(donnees: schemas.BorrowCreate, session: Session = Depends(get_db)):
    # Un emprunt n'est valide que si le lecteur et le livre existent.
    lecteur = session.get(models.Reader, donnees.reader_id)
    if not lecteur:
        raise HTTPException(status_code=404, detail="Lecteur introuvable")

    livre = session.get(models.Book, donnees.book_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre introuvable")

    # La création d'un emprunt dépend du stock disponible.
    if livre.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Aucune copie disponible pour ce livre")

    emprunt = models.Borrow(reader_id=donnees.reader_id, book_id=donnees.book_id)
    # Le stock est décrémenté dans la même transaction que la création de l'emprunt.
    livre.available_copies -= 1

    session.add(emprunt)
    session.commit()
    session.refresh(emprunt)
    return emprunt


@router.patch("/{emprunt_id}/return", response_model=schemas.BorrowResponse)
def retourner_livre(emprunt_id: int, session: Session = Depends(get_db)):
    emprunt = session.get(models.Borrow, emprunt_id)
    if not emprunt:
        raise HTTPException(status_code=404, detail="Emprunt introuvable")

    if emprunt.status == "returned":
        raise HTTPException(status_code=400, detail="Ce livre a déjà été retourné")

    # Le retour du livre met à jour l'emprunt et rend une copie disponible.
    emprunt.status = "returned"
    emprunt.return_date = datetime.utcnow()
    emprunt.book.available_copies += 1

    session.commit()
    session.refresh(emprunt)
    return emprunt


@router.put("/{emprunt_id}", response_model=schemas.BorrowResponse)
def modifier_emprunt(emprunt_id: int, donnees: schemas.BorrowUpdate, session: Session = Depends(get_db)):
    emprunt = session.get(models.Borrow, emprunt_id)
    if not emprunt:
        raise HTTPException(status_code=404, detail="Emprunt introuvable")

    # Cette route permet une modification manuelle du statut ou de la date de retour.
    modifications = donnees.model_dump(exclude_unset=True)
    for champ, valeur in modifications.items():
        setattr(emprunt, champ, valeur)

    session.commit()
    session.refresh(emprunt)
    return emprunt


@router.delete("/{emprunt_id}", response_model=schemas.MessageResponse)
def supprimer_emprunt(emprunt_id: int, session: Session = Depends(get_db)):
    emprunt = session.get(models.Borrow, emprunt_id)
    if not emprunt:
        raise HTTPException(status_code=404, detail="Emprunt introuvable")

    # Si l'emprunt était encore actif, on corrige le stock avant suppression.
    if emprunt.status == "borrowed":
        emprunt.book.available_copies += 1

    session.delete(emprunt)
    session.commit()
    return {"message": "Emprunt supprimé"}
