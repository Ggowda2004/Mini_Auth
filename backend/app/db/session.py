from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

db_url="postgresql://postgres:kmggPOSTgrekmgg@localhost:5432/auth_db"

engine = create_engine(db_url)
sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db()->Generator:
    db=sessionLocal
    try:
        yield db
    finally:
        db.close()

#we have give url,create engine,sessionmaker and get_db function to get the db session for our application.