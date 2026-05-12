"""
Ce fichier sert à déclarer l'application.
L'application est ensuite lancé par uvicorn.
"""
# importation de fastAPI
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import authors, books, borrows, cards, readers

# On demande à SQLAlchimy de créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

#Crée une application FastAPI avec un titre, une description et une version.
app = FastAPI(
    title="Gestion de bibliothèque",
    description="API REST pour gérer une bibliothèque avec des lecteurs, cartes, auteurs, livres et emprunts.",
    version="1.1.0",
)

# On rend accessibles les fichiers du dossier app/static via l'URL /static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Quand quelqu'un visite GET /,
# on lui renvoie le fichier HTML de l'interface
@app.get("/", tags=["Interface"], include_in_schema=False)
def afficher_page_accueil():
    return FileResponse("app/static/index.html")


# Ajoute les differente routes
app.include_router(readers.router)
app.include_router(cards.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(borrows.router)
