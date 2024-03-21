from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLACLHEMY_DATABASE_URL = 'postgresql://koyeb-adm:P1k9ehfYAOul@ep-weathered-cloud-a2w0wacj.eu-central-1.pg.koyeb.app/koyebdb'

engine = create_engine(SQLACLHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
