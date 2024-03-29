from sys import modules

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app import settings

db_connection_str = settings.db_connection_str
if "pytest" in modules:
    db_connection_str = settings.db_test_connection_str

engine = create_engine(db_connection_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    """
    Responsible to return db session
    Returns:

    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
