import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "kioku.db")

engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)