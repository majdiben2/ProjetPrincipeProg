from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Les schémas Pydantic définissent ce que l'API accepte en entrée
# et ce qu'elle renvoie en sortie. Ils évitent d'exposer directement
# les modèles SQLAlchemy aux utilisateurs de l'API.
class ReaderBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=80)
    last_name: str = Field(..., min_length=1, max_length=80)
    email: str = Field(..., max_length=120)


# Création : on réutilise les champs obligatoires du schéma de base.
class ReaderCreate(ReaderBase):
    pass


# Mise à jour : tous les champs sont optionnels pour permettre
# de modifier seulement les informations envoyées par le client.
class ReaderUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=80)
    last_name: Optional[str] = Field(None, min_length=1, max_length=80)
    email: Optional[str] = Field(None, max_length=120)


class ReaderResponse(ReaderBase):
    # Autorise Pydantic à construire la réponse à partir d'un objet SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class LibraryCardBase(BaseModel):
    card_number: str = Field(..., min_length=3, max_length=50)
    reader_id: int


class LibraryCardCreate(LibraryCardBase):
    pass


class LibraryCardUpdate(BaseModel):
    card_number: Optional[str] = Field(None, min_length=3, max_length=50)
    reader_id: Optional[int] = None


class LibraryCardResponse(LibraryCardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    issued_at: datetime


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    nationality: Optional[str] = Field(None, max_length=80)
    birth_year: Optional[int] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    nationality: Optional[str] = Field(None, max_length=80)
    birth_year: Optional[int] = None


class AuthorResponse(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    isbn: str = Field(..., min_length=3, max_length=30)
    publication_year: Optional[int] = None
    # ge=0 empêche d'avoir un nombre de copies négatif. (superieur ou egal à 0)
    available_copies: int = Field(default=1, ge=0)
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, min_length=3, max_length=30)
    publication_year: Optional[int] = None
    available_copies: Optional[int] = Field(None, ge=0)
    author_id: Optional[int] = None


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# Pour créer un emprunt, le client fournit seulement les deux identifiants.
# Les dates et le statut sont gérés côté serveur.
class BorrowCreate(BaseModel):
    reader_id: int
    book_id: int


class BorrowUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=20)
    return_date: Optional[datetime] = None


class BorrowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reader_id: int
    book_id: int
    borrow_date: datetime
    return_date: Optional[datetime]
    status: str


# Réponse simple utilisée par les routes DELETE.
class MessageResponse(BaseModel):
    message: str
