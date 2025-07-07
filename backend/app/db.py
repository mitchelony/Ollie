from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for SQLite
DATABASE_URL = "sqlite:///./ollie.db"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
    )

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

# Create a base class for declarative models
Base = declarative_base()

# DB Session Function
def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()