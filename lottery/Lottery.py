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
from statistics import multimode, mode
import random

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
                winFour=model.winFour,
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


@router.get("/predict_powerball_numbers", status_code=status.HTTP_200_OK)
async def predict(db: db_dependency, user: user_dependency):
    winningNumbers = []
    predict = []
    powerballs = []

    try:
        username = user.get("username")
        if username != "":
            result = db.query(Powerball.Powerball).all()
            for item in result:
                winningNumbers.append(item.winOne)
                winningNumbers.append(item.winTwo)
                winningNumbers.append(item.winThree)
                winningNumbers.append(item.winFour)
                winningNumbers.append(item.winFive)
                powerballs.append(item.powerball)

    finally:
        popular = multimode(winningNumbers)
        dummy_popular = popular
        while len(popular) < 5:
            for number in dummy_popular:
                winningNumbers.remove(number)
                dummy_popular.remove(number)
            second_popular = multimode(winningNumbers)
            popular += second_popular
            dummy_popular = second_popular

        powerball_num = multimode(powerballs)
        dummy_powerball_num = powerball_num
        while len(powerball_num) < 3:
            for number in dummy_powerball_num:
                dummy_powerball_num.remove(number)
                powerballs.remove(number)
            second_popular_powerball = multimode(powerballs)
            powerball_num += second_popular_powerball

            dummy_powerball_num = second_popular_powerball

        predict += popular
        predict.append(random.choice(powerball_num))
        return {"numbers": predict
                }
