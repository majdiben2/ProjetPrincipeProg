from app.database import Base, SessionLocal, engine
from app.models import Author, Book, Borrow, LibraryCard, Reader


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(Author).first():
            print("Seed déjà exécuté : des données existent déjà.")
            return

        author_1 = Author(name="Victor Hugo", nationality="Française", birth_year=1802)
        author_2 = Author(name="George Orwell", nationality="Britannique", birth_year=1903)

        db.add_all([author_1, author_2])
        db.commit()
        db.refresh(author_1)
        db.refresh(author_2)

        book_1 = Book(
            title="Les Misérables",
            isbn="9782070409228",
            publication_year=1862,
            available_copies=3,
            author_id=author_1.id,
        )
        book_2 = Book(
            title="1984",
            isbn="9782070368228",
            publication_year=1949,
            available_copies=2,
            author_id=author_2.id,
        )

        reader_1 = Reader(first_name="Amina", last_name="Diallo", email="amina@example.com")
        reader_2 = Reader(first_name="Lucas", last_name="Martin", email="lucas@example.com")

        db.add_all([book_1, book_2, reader_1, reader_2])
        db.commit()
        db.refresh(reader_1)
        db.refresh(reader_2)
        db.refresh(book_1)

        card_1 = LibraryCard(card_number="CARD-001", reader_id=reader_1.id)
        card_2 = LibraryCard(card_number="CARD-002", reader_id=reader_2.id)

        borrow_1 = Borrow(reader_id=reader_1.id, book_id=book_1.id)
        book_1.available_copies -= 1

        db.add_all([card_1, card_2, borrow_1])
        db.commit()
        print("Données de test insérées avec succès.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
