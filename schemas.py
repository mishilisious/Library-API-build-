from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class BookCreate(BaseModel):
    BookName: str
    Author: str
    Year: int


class BookResponse(BaseModel):
    BookID: int
    BookName: str
    Author: str
    Year: int

class BookUpdate(BaseModel):
    BookName: str | None = None
    Author: str | None = None
    Year: int | None = None

class ReviewCreate(BaseModel):
    rating: int
    comment: str


class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None