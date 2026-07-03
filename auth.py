from fastapi import APIRouter, Depends,HTTPException
from jose import jwt, JWTError 
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .models import LoginRequest

router=APIRouter()

USERNAME= "Admin"
PASSWORD= "password123"
SECRET_KEY = "this-is-my-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



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
    token: str = Depends(oauth2_scheme)):
      return verify_token(token)

@router.post("/login")
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
