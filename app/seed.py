"""
Ce fichier est un script d'import de jeu de données pour le test
"""
from app.database import Base, SessionLocal, engine
from app.models import Author, Book, Borrow, LibraryCard, Reader


def run_seed():
    # Crée les tables si elles n'existent pas encore.
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Évite d'insérer plusieurs fois les mêmes données.
        if db.query(Author).first():
            print("Seed déjà exécuté : des données existent déjà.")
            return

        authors = [
            Author(name="Victor Hugo", nationality="Française", birth_year=1802),
            Author(name="George Orwell", nationality="Britannique", birth_year=1903),
            Author(name="Jules Verne", nationality="Française", birth_year=1828),
            Author(name="Agatha Christie", nationality="Britannique", birth_year=1890),
            Author(name="Albert Camus", nationality="Française", birth_year=1913),
        ]

        db.add_all(authors)
        db.commit()
        for author in authors:
            db.refresh(author)

        books = [
            Book(
                title="Les Misérables",
                isbn="9782070409228",
                publication_year=1862,
                available_copies=3,
                author_id=authors[0].id,
            ),
            Book(
                title="1984",
                isbn="9782070368228",
                publication_year=1949,
                available_copies=2,
                author_id=authors[1].id,
            ),
            Book(
                title="Le Tour du monde en quatre-vingts jours",
                isbn="9782253006326",
                publication_year=1872,
                available_copies=4,
                author_id=authors[2].id,
            ),
            Book(
                title="Le Crime de l'Orient-Express",
                isbn="9782253240843",
                publication_year=1934,
                available_copies=2,
                author_id=authors[3].id,
            ),
            Book(
                title="L'Étranger",
                isbn="9782070360024",
                publication_year=1942,
                available_copies=3,
                author_id=authors[4].id,
            ),
        ]

        readers = [
            Reader(first_name="Amina", last_name="Diallo", email="amina@example.com"),
            Reader(first_name="Lucas", last_name="Martin", email="lucas@example.com"),
            Reader(first_name="Nadia", last_name="Benali", email="nadia@example.com"),
            Reader(first_name="Hugo", last_name="Petit", email="hugo@example.com"),
            Reader(first_name="Inès", last_name="Moreau", email="ines@example.com"),
        ]

        db.add_all(books + readers)
        db.commit()
        for item in books + readers:
            db.refresh(item)

        cards = [
            LibraryCard(card_number="CARD-001", reader_id=readers[0].id),
            LibraryCard(card_number="CARD-002", reader_id=readers[1].id),
            LibraryCard(card_number="CARD-003", reader_id=readers[2].id),
            LibraryCard(card_number="CARD-004", reader_id=readers[3].id),
            LibraryCard(card_number="CARD-005", reader_id=readers[4].id),
        ]

        # Chaque lecteur emprunte un livre différent pour tester les relations et les stocks.
        borrows = []
        for reader, book in zip(readers, books):
            borrows.append(Borrow(reader_id=reader.id, book_id=book.id))
            book.available_copies -= 1

        db.add_all(cards + borrows)
        db.commit()
        print("Données de test insérées avec succès.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()