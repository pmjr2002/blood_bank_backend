from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace these values with your actual Aiven credentials
USERNAME = "avnadmin"
PASSWORD = "AVNS_N0-Z5xRbW2mOOoW9Kg7"
HOST = "mysql-bbms-blood-bank-management-system.h.aivencloud.com"
PORT = "26445"
DATABASE = "defaultdb"

# Use the mariadb connector
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

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
