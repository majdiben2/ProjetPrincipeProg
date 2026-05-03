
INSERT INTO authors (id, name, nationality, birth_year)
VALUES
  (1, 'Victor Hugo', 'Française', 1802),
  (2, 'George Orwell', 'Britannique', 1903)
ON CONFLICT DO NOTHING;

INSERT INTO books (id, title, isbn, publication_year, available_copies, author_id)
VALUES
  (1, 'Les Misérables', '9782070409228', 1862, 3, 1),
  (2, '1984', '9782070368228', 1949, 2, 2)
ON CONFLICT DO NOTHING;

INSERT INTO readers (id, first_name, last_name, email, created_at)
VALUES
  (1, 'Amina', 'Diallo', 'amina@example.com', NOW()),
  (2, 'Lucas', 'Martin', 'lucas@example.com', NOW())
ON CONFLICT DO NOTHING;

INSERT INTO library_cards (id, card_number, issued_at, reader_id)
VALUES
  (1, 'CARD-001', NOW(), 1),
  (2, 'CARD-002', NOW(), 2)
ON CONFLICT DO NOTHING;

INSERT INTO borrows (id, reader_id, book_id, borrow_date, status)
VALUES
  (1, 1, 1, NOW(), 'borrowed')
ON CONFLICT DO NOTHING;
