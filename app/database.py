"""
Ce fichier sert à connecter l'API à la base de données PostgreSQL
à préparer SQLAlchemy
à Fournir une session de bdd aux routes API
"""
# Permet d'interagir avec l'OS
import os

#create_engine sert à créer le moteur de connexion à la base de données.
#Le moteur, c’est l’objet qui sait où est la base, comment s’y connecter, 
#et quel type de base utiliser
from sqlalchemy import create_engine

# declarative_base sert a creer une classe de base
# sessionmaker fabrique des session de bdd pour faire les requete CRUD
from sqlalchemy.orm import declarative_base, sessionmaker


# Cherche une variable d'environnement DATABASE_URL dans docker-compose🟢
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("La variable d'environnement DATABASE_URL doit être définie.")

# le moteur de base de données.
engine = create_engine(DATABASE_URL)

# fabrique une session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db # yield db donne temporairement la session db à FastAPI
    finally:
        db.close()

"""
3 object de SLQALchmy
engine : objet qui connait l'adresse de la bdd et qui sait interagir avec la bdd (connexion instrution etc...)
sessionmaker : fabrique des sessions de travail temporaire pour parler à la base (Chaque action a sa session propre.)
base : le plan général des tables

SQLAlchemy est une bibliothèque Python 
qui permet à ton code de communiquer avec une base de données relationnelle
Sert d'ORM
"""