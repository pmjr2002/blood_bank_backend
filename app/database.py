from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Replace these values with your actual Aiven credentials


DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
# Use the mariadb connector
SQLALCHEMY_DATABASE_URL = f"{DATABASE_URL}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
