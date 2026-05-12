# Gestion de bibliothèque

Projet réalisé dans le cadre de la SAE **Développement et Déploiement d’une Application Web RESTful Conteneurisée**.

## Auteurs

- Daizer Bercy
- Ben Younes Majdi

## Présentation

Ce projet est une application de gestion de bibliothèque. Elle permet de gérer les auteurs, les livres, les lecteurs, les cartes de bibliothèque et les emprunts.

L’application contient une API REST avec FastAPI et une petite interface web pour rendre la démonstration plus simple pendant la soutenance.

## Technologies utilisées

| Élément | Technologie |
|---|---|
| Backend | FastAPI |
| Langage | Python |
| ORM | SQLAlchemy |
| Base de données | PostgreSQL |
| Documentation | Swagger |
| Interface web | HTML, CSS, JavaScript |
| Conteneurisation | Docker |
| Lancement complet | Docker Compose |

## Relations dans la base de données

### One-to-One

Un lecteur possède une seule carte de bibliothèque.

```txt
Reader 1 ─── 1 LibraryCard
```

### One-to-Many

Un auteur peut avoir plusieurs livres.

```txt
Author 1 ─── * Book
```

### Many-to-Many

Un lecteur peut emprunter plusieurs livres, et un livre peut être emprunté par plusieurs lecteurs au fil du temps.

La relation passe par la table `Borrow`.

```txt
Reader * ─── * Book
       via Borrow
```

## Structure du projet

```txt
library-api-web/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   ├── routers/
│   │   ├── authors.py
│   │   ├── books.py
│   │   ├── borrows.py
│   │   ├── cards.py
│   │   └── readers.py
│   └── static/
│       ├── index.html
│       ├── styles.css
│       └── app.js
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Lancer le projet

Il faut avoir Docker installé sur la machine.

Depuis le dossier du projet :

```bash
docker compose up --build
```

Interface web :

```txt
http://localhost:8000
```

Swagger :

```txt
http://localhost:8000/docs
```

## Ajouter des données de test

Quand les conteneurs sont lancés, ouvrir un deuxième terminal et exécuter :

```bash
docker compose exec api python -m app.seed
```

Cela ajoute quelques auteurs, livres, lecteurs, cartes et emprunts pour tester plus rapidement l’application.

## Routes principales de l’API

### Auteurs

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/authors` | Lister les auteurs |
| GET | `/authors/{id}` | Afficher un auteur |
| POST | `/authors` | Ajouter un auteur |
| PUT | `/authors/{id}` | Modifier un auteur |
| DELETE | `/authors/{id}` | Supprimer un auteur |

Exemple :

```json
{
  "name": "Victor Hugo",
  "nationality": "Française",
  "birth_year": 1802
}
```

### Livres

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/books` | Lister les livres |
| GET | `/books/available` | Lister les livres disponibles |
| GET | `/books/{id}` | Afficher un livre |
| POST | `/books` | Ajouter un livre |
| PUT | `/books/{id}` | Modifier un livre |
| DELETE | `/books/{id}` | Supprimer un livre |

Exemple :

```json
{
  "title": "Les Misérables",
  "isbn": "9782070409228",
  "publication_year": 1862,
  "available_copies": 3,
  "author_id": 1
}
```

### Lecteurs

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/readers` | Lister les lecteurs |
| GET | `/readers/{id}` | Afficher un lecteur |
| POST | `/readers` | Ajouter un lecteur |
| PUT | `/readers/{id}` | Modifier un lecteur |
| DELETE | `/readers/{id}` | Supprimer un lecteur |

Exemple :

```json
{
  "first_name": "Nadia",
  "last_name": "Benali",
  "email": "nadia@example.com"
}
```

### Cartes de bibliothèque

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/cards` | Lister les cartes |
| GET | `/cards/{id}` | Afficher une carte |
| POST | `/cards` | Créer une carte |
| PUT | `/cards/{id}` | Modifier une carte |
| DELETE | `/cards/{id}` | Supprimer une carte |

Exemple :

```json
{
  "card_number": "CARD-001",
  "reader_id": 1
}
```

### Emprunts

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/borrows` | Lister les emprunts |
| GET | `/borrows/{id}` | Afficher un emprunt |
| POST | `/borrows` | Créer un emprunt |
| PUT | `/borrows/{id}` | Modifier un emprunt |
| PATCH | `/borrows/{id}/return` | Retourner un livre |
| DELETE | `/borrows/{id}` | Supprimer un emprunt |

Exemple :

```json
{
  "reader_id": 1,
  "book_id": 1
}
```

## Persistance des données

La base PostgreSQL utilise un volume Docker nommé `postgres_data`. Les données restent donc présentes même si les conteneurs sont arrêtés.

Pour tout supprimer et repartir de zéro :

```bash
docker compose down -v
```

Puis relancer :

```bash
docker compose up --build
```
