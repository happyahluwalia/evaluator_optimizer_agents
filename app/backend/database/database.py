from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.backend.database.dbmodels import Base


DATABASE_URL = "sqlite:///./AgentsDatabase.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# TODO: Check if the params of sessionmake needs to be changed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
