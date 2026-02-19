from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from app.core.config import Settings

db_url=Settings.database_url

engine = create_engine(db_url)
sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db()->Generator:
    db=sessionLocal
    try:
        yield db
    finally:
        db.close()