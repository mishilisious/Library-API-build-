from fastapi import FastAPI
from .books import router as books_router
from .auth import router as auth_router
from .database import engine
from . import models
from .borrowings import router as borrowings_router
from .reviews import router as reviews_router

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(books_router)
app.include_router(auth_router)
app.include_router(borrowings_router)
app.include_router(reviews_router)