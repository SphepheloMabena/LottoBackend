import array
import datetime
from typing import List

from pydantic import BaseModel


class LottoModel(BaseModel):
    date: datetime.date
    winOne: int
    winTwo: int
    winThree: int
    winFour: int
    winFive: int
    powerball: int
