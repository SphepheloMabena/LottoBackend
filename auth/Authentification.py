from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from db.Database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from db.Tables.Users import User
from datetime import timedelta, datetime
from jose import jwt, JWTError
from models.UserModel import UserModel
from models.Token import Token

router = APIRouter()

SECRET_KEY = "bccnvhjgyvcvyucxzcnkbdcbweuhbowelcsniszcvbgxlkdcjjvfcknascrsrtjbbcedgmnbsnvcyejbs"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta, role: str):
    encode = {
        'name': username,
        'id': user_id,
        'role': role
    }
    expires = datetime.utcnow() + expires_delta
    encode.update(({'exp': expires}))
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('name')
        user_id: int = payload.get('id')
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(detail="not authorized", status_code=status.HTTP_401_UNAUTHORIZED)
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(detail="Could not validate user", status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: UserModel):
    user_model = User(
        email=user.email,
        username=user.username,
        hashed_password=bcrypt_context.hash(user.password),
        role=user.role
    )
    db.add(user_model)
    db.commit()
    return {"message": "User added successfully"}


@router.post("/token", response_model=Token)
async def Login_for_Access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        return 'Failed Authentication'

    token = create_access_token(user.username, user.id, timedelta(minutes=20), user.role)

    return {'access_token': token, 'token_type': 'bearer'}
