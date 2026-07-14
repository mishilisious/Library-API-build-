from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .schemas import LoginRequest, UserSignup
from .hash_password import ( hash_password, verify_password )
from .database import get_db
from .models import User

router = APIRouter()

SECRET_KEY = "this-is-my-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

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
        role = payload.get("role")

        if username is None:
            return { "Message": " Error 401  Invalid or expr token"   }

        return {
            "username": username,
            "role": role
        }

    except JWTError:
          return { "Message": " Error 401  Invalid or expired token"   }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    token_data = verify_token(token)

    user = (
        db.query(User)
        .filter(User.username == token_data["username"])
        .first()
    )

    if user is None:
          return { "Message": " Error 401 User not found."   }

    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return current_user

    return { "Message": " Error 403  Admin access required."   }


@router.post("/signup")
def signup(
    user: UserSignup,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.username == user.Username)
        .first()
    )

    if existing_user:
        return {
                 "Message": "Error 400 Username already exists."
            }

    new_user = User(
        username=user.Username,
        hashed_password=hash_password(user.Password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully.",
        "user": {
            "userid": new_user.userid,
            "username": new_user.username,
            "role": new_user.role
        }
    }

@router.post("/login")
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == credentials.username
    ).first()

    if user is None:
          return { "Message": " Error 401  Invalid username or password. "   }

    if not verify_password(
        credentials.password,
        user.hashed_password
    ):
        return { "Message": " Error 401  Invalid username or password."   }

    token = create_access_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }