from SQLManager.Configure.DB_Setting import DB_URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

db_engine = create_engine(DB_URL, max_overflow=5)

Base = declarative_base()
