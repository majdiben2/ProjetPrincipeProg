from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    card = relationship(
        "LibraryCard",
        back_populates="reader",
        uselist=False,
        cascade="all, delete-orphan",
    )
    borrows = relationship("Borrow", back_populates="reader", cascade="all, delete-orphan")
    books = relationship("Book", secondary="borrows", viewonly=True)


class LibraryCard(Base):
    __tablename__ = "library_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String(50), unique=True, index=True, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), unique=True, nullable=False)

    reader = relationship("Reader", back_populates="card")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    nationality = Column(String(80), nullable=True)
    birth_year = Column(Integer, nullable=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    isbn = Column(String(30), unique=True, index=True, nullable=False)
    publication_year = Column(Integer, nullable=True)
    available_copies = Column(Integer, default=1, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", back_populates="book", cascade="all, delete-orphan")
    readers = relationship("Reader", secondary="borrows", viewonly=True)


class Borrow(Base):
    __tablename__ = "borrows"
    __table_args__ = (
        UniqueConstraint("reader_id", "book_id", "borrow_date", name="uq_reader_book_borrow_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="borrowed", nullable=False)

    reader = relationship("Reader", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")
