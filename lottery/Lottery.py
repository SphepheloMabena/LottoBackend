from fastapi import APIRouter, Depends, status

from auth.Authentification import oauth2_bearer
from db.Database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from auth import Authentification
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from db.Tables import Users
from db.Tables import Powerball
from db.Database import engine
from models.LottoModel import LottoModel
from db.Tables import Powerball

router = APIRouter()

Users.Base.metadata.create_all(bind=engine)
Powerball.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(Authentification.get_current_user)]


@router.get("/Lottery")
async def lottery():
    return {"message": "Welcome To Lottery"}


class TokenModel(BaseModel):
    token: str


@router.post("/add_powerball", status_code=status.HTTP_201_CREATED)
async def powerball(db: db_dependency, user: user_dependency, model: LottoModel):
    try:
        username = user.get("username")
        if username != "":
            powerball_model = Powerball.Powerball(
                date=model.date,
                winOne=model.winOne,
                winTwo=model.winTwo,
                winThree=model.winThree,
                winFour=model.winThree,
                winFive=model.winFive,
                powerball=model.powerball
            )
            db.add(powerball_model)
            db.commit()
            return {"Message": "Powerball Added Successfully"}

    finally:
        var = {"user": "users"}


@router.get("/powerball", status_code=status.HTTP_200_OK)
async def getPowerbal(db: db_dependency, user: user_dependency):
    powerballResults = []
    try:
        username = user.get("username")
        if username != "":
            result = db.query(Powerball.Powerball).all()
            for item in result:
                winning_numbers = [item.winOne, item.winTwo, item.winThree, item.winFour, item.winFive, item.powerball]
                data = {
                    "date": item.date,
                    "numbers": winning_numbers
                }
                powerballResults.append(data)

    finally:
        return powerballResults
