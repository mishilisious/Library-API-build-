from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .schemas import BookCreate, BookUpdate
from .auth import get_current_admin
from .database import get_db
from .models import Book as BookModel

router = APIRouter()


# Endpoint 1 - Create a Book
@router.post("/books")
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    new_book = BookModel(
        book_name=book.BookName,
        author=book.Author,
        year=book.Year
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {
        "message": "Book added successfully",
        "book": {
            "BookID": new_book.bookid,
            "BookName": new_book.book_name,
            "Author": new_book.author,
            "Year": new_book.year
        }
    }


# Endpoint 2 - Get all books by an author
@router.get("/books")
def display_books(author: str, db: Session = Depends(get_db)):

    books = db.query(BookModel).filter(
        BookModel.author == author
    ).all()

    if not books:
          return { "Message": " Error 404  Author not found."   }
    return [
        {
            "BookID": book.bookid,
            "BookName": book.book_name,
            "Author": book.author,
            "Year": book.year
        }
        for book in books
    ]


# Endpoint 3 - Get a specific book by ID
@router.get("/books/{book_id}")
def specific_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(BookModel).filter(
        BookModel.bookid == book_id
    ).first()

    if not book:
          return { "Message": " Error 404  Book ID does not exist."   }

    return {
        "BookID": book.bookid,
        "BookName": book.book_name,
        "Author": book.author,
        "Year": book.year
    }


# Endpoint 4 - Update an entire book
@router.put("/books/{book_id}")
def update_book(
    book_id: int,
    book: BookCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    existing_book = db.query(BookModel).filter(
        BookModel.bookid == book_id
    ).first()

    if not existing_book:
          return { "Message": " Error 404  Book ID does not exist."   }
    
    existing_book.book_name = book.BookName
    existing_book.author = book.Author
    existing_book.year = book.Year

    db.commit()
    db.refresh(existing_book)

    return {
        "message": "Book updated successfully",
        "book": {
            "BookID": existing_book.bookid,
            "BookName": existing_book.book_name,
            "Author": existing_book.author,
            "Year": existing_book.year
        }
    }


# Endpoint 5 - Partial book updation
@router.patch("/books/{book_id}")
def update_book_partial(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    existing_book = (
        db.query(BookModel)
        .filter(BookModel.bookid == book_id)
        .first()
    )

    if not existing_book:
          return { "Message": " Error 404  Book ID does not exist."   }

    if book.BookName is not None:
        existing_book.book_name = book.BookName

    if book.Author is not None:
        existing_book.author = book.Author

    if book.Year is not None:
        existing_book.year = book.Year

    db.commit()
    db.refresh(existing_book)

    return {
        "message": "Book updated successfully",
        "book": {
            "BookID": existing_book.bookid,
            "BookName": existing_book.book_name,
            "Author": existing_book.author,
            "Year": existing_book.year
        }
    }


# Endpoint 6 - Delete a book
@router.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    existing_book = db.query(BookModel).filter(
        BookModel.bookid == book_id
    ).first()

    if not existing_book:
          return { "Message": " Error 404  Book ID does not exist."   }
    
    db.delete(existing_book)
    db.commit()

    return {
        "message": "Deletion successful"
    }