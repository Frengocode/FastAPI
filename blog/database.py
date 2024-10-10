from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import models
from . import database



SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:pasword@localhost/ApiDb'


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush=False)

Base = declarative_base()





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


database.Base.metadata.create_all(engine)
