from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt, JWTError 
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

Books = []

USERNAME= "Admin"
PASSWORD= "password123"
SECRET_KEY = "this-is-my-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class LoginRequest(BaseModel):
    username: str
    password: str

class Book(BaseModel):
    BookID: int
    BookName: str
    Author: str
    Year: int


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    return verify_token(token)

# Endpoint 1 - Create a Book
@app.post("/books")
def create_book(book: Book, current_user: str = Depends(get_current_user)):
    for existing_book in Books:
        if book.BookID == existing_book.BookID:
            raise HTTPException(status_code=409, detail="Book ID already exists")

    Books.append(book)

    return {
        "message": "Book added successfully",
        "book": book
    }


# Endpoint 2 - Get all books by an author
@app.get("/books")
def display_books(author: str):
    author_books = []

    for book in Books:
        if book.Author == author:
            author_books.append(book)

    if not author_books:
        raise HTTPException(status_code=404, detail="Author not found")

    return author_books


# Endpoint 3 - Get a specific book by ID
@app.get("/books/{book_id}")
def specific_book(book_id: int):
    for existing_book in Books:
        if existing_book.BookID == book_id:
            return existing_book

    raise HTTPException(status_code=404, detail="Book ID does not exist")


# Endpoint 4 - Update an entire book
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book, current_user: str = Depends(get_current_user)):
    for existing_book in Books:
        if existing_book.BookID == book_id:
            existing_book.BookName = book.BookName
            existing_book.Author = book.Author
            existing_book.Year = book.Year
            return {
                "message": "Book updated successfully",
                "book": existing_book
            }

    raise HTTPException(status_code=404, detail="Book ID does not exist")


# Endpoint 5 - Update only the book name
@app.patch("/books/{book_id}")
def name_change(book_id: int, bookname: str, current_user: str = Depends(get_current_user)):
    for existing_book in Books:
        if existing_book.BookID == book_id:
            existing_book.BookName = bookname
            return {
                "message": "Book name updated successfully",
                "book": existing_book
            }

    raise HTTPException(status_code=404, detail="Book ID does not exist")


# Endpoint 6 - Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int, current_user: str = Depends(get_current_user)):
    for existing_book in Books:
        if existing_book.BookID == book_id:
            Books.remove(existing_book)
            return {"message": "Deletion successful"}

    raise HTTPException(status_code=404, detail="Book ID does not exist")

@app.post("/login")
def login(credentials: LoginRequest):
        if credentials.username == USERNAME and credentials.password == PASSWORD:
            token = create_access_token(
              {
                 "sub": credentials.username
              }  )
            return {
                       "access_token": token,
                       "token_type": "bearer"
                    }
        raise HTTPException(status_code=401, detail="Invalid username or password")
 