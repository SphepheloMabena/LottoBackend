from ..Database import Base
from sqlalchemy import ARRAY, DATE, Integer, Column


class DailyLotto(Base):
    __tablename_ = 'daily_lotto'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DATE),
    winNumbers = Column(ARRAY(Integer))
