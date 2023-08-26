from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from urllib.parse import quote_plus 

encoded_password = quote_plus(settings.DATABASE_PASSWORD)

# Print settings to debug
# print("DATABASE_USERNAME:", settings.DATABASE_USERNAME)
# print("DATABASE_PASSWORD:", settings.DATABASE_PASSWORD)
# print("DATABASE_HOSTNAME:", settings.DATABASE_HOSTNAME)
# print("DATABASE_PORT:", settings.DATABASE_PORT)
# print("DATABASE_NAME:", settings.DATABASE_NAME)

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{encoded_password}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
