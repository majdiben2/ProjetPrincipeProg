from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import authors, books, borrows, cards, readers

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestion de bibliothèque",
    description="API REST pour gérer une bibliothèque avec des lecteurs, cartes, auteurs, livres et emprunts.",
    version="1.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", tags=["Interface"], include_in_schema=False)
def afficher_page_accueil():
    return FileResponse("app/static/index.html")


@app.get("/api", tags=["État"])
def accueil_api():
    return {
        "message": "Bienvenue sur l'API de gestion de bibliothèque",
        "interface": "/",
        "swagger": "/docs",
    }


@app.get("/health", tags=["État"])
def verifier_api():
    return {"status": "ok"}


app.include_router(readers.router)
app.include_router(cards.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(borrows.router)
