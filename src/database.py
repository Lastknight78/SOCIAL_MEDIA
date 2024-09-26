from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os, dotenv
dotenv.load_dotenv()
class Base(DeclarativeBase):
    pass

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(url = DATABASE_URL)

sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    try:
        session = sessionLocal()
        yield session
    finally:
        session.close()
