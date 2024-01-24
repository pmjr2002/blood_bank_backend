from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# **Update database URL for PostgreSQL**
SQLALCHEMY_DATABASE_URL = "postgresql://avnadmin:AVNS_GxNqi95MDuVFYgFEyev@blood-db-wic-f.a.aivencloud.com:15185/defaultdb"

# **Create engine for PostgreSQL**
engine = create_engine(SQLALCHEMY_DATABASE_URL)  # Remove "connect_args" for PostgreSQL

# **Create session factory**
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# **Base for models remains unchanged**
Base = declarative_base()

# **Dependency function remains unchanged**
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
