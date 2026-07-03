from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class Book(BaseModel):
    BookID: int
    BookName: str
    Author: str
    Year: int
