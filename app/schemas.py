from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReaderBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=80)
    last_name: str = Field(..., min_length=1, max_length=80)
    email: str = Field(..., max_length=120)


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=80)
    last_name: Optional[str] = Field(None, min_length=1, max_length=80)
    email: Optional[str] = Field(None, max_length=120)


class ReaderResponse(ReaderBase):
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


class MessageResponse(BaseModel):
    message: str
