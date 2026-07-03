from fastapi import FastAPI
from .books import router as books_router
from .auth import router as auth_router

app=FastAPI()

app.include_router(books_router)
app.include_router(auth_router)