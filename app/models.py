"""
Ce fichier définit les tables de la base de données sous forme de classes Python.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Reader(Base):
    __tablename__ = "readers" # nom de la table

    id = Column(Integer, primary_key=True, index=True) # Clé primaire + index pour facilité la recherche
    first_name = Column(String(80), nullable=False) #nullable=false => obligatoire
    last_name = Column(String(80), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False) # date/heurre actuelle par default



  # Déclare des relations
    
    card = relationship(
        "LibraryCard",
        back_populates="reader",
        uselist=False, # Le lecteur n'a qu'une seul carte one to one (pas une liste)
        cascade="all, delete-orphan", # si on supprime un lecteur sa carte est automatiquemeent supprimé
    )
    borrows = relationship("Borrow", back_populates="reader", cascade="all, delete-orphan")  # le lecteur peut faire plusieur empreunt one to many
    books = relationship("Book", secondary="borrows", viewonly=True) # sert juste à la lecture on veut voir les livre empreunté.


class LibraryCard(Base):
    __tablename__ = "library_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String(50), unique=True, index=True, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False) # Date d'emission de la carte
    reader_id = Column(Integer, ForeignKey("readers.id"), unique=True, nullable=False)

    reader = relationship("Reader", back_populates="card") #  Depuis une carte, on peut récupérer le lecteur avec card.reader


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    nationality = Column(String(80), nullable=True)
    birth_year = Column(Integer, nullable=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan") # un auteur peut avoir plusieur livre
    # cascade)'all' signifique toutes les opération effectuer sur le parent sont propagé a ses enfants 

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
    __table_args__ = ( # contraintes spéciales appliquées a la table
        UniqueConstraint("reader_id", "book_id", "borrow_date", name="uq_reader_book_borrow_date"), # empeche d'avoir deux ligne identique avec le meme lecteur
    )

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="borrowed", nullable=False)

    reader = relationship("Reader", back_populates="borrows") # Depuis un emprunt, on peut récupérer le lecteur avec emprunt.reader
    book = relationship("Book", back_populates="borrows")
