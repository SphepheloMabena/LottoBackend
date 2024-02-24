from ..Database import Base
from sqlalchemy import ARRAY, DATE, Integer, Column


class Powerball(Base):
    __tablename__ = 'powerball'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DATE)
    winOne = Column(Integer)
    winTwo = Column(Integer)
    winThree = Column(Integer)
    winFour = Column(Integer)
    winFive = Column(Integer)
    powerball = Column(Integer)
