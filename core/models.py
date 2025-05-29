import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv('DB_URL')
if not DB_URL:
    raise ValueError("DB_URL не найден в .env файле")

Base = declarative_base()
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


class Config(Base):
    __tablename__ = "api_config"
    id = Column(Integer, primary_key=True)
    step = Column(Integer)
    currency_code = Column(String)
    date = Column(Date)
    email = Column(String)


class Currency(Base):
    __tablename__ = "api_currency"
    id = Column(Integer, primary_key=True)
    currency_code = Column(String)
    currency_date = Column(Date)
    currency_scale = Column(Integer)
    currency_name = Column(String)
    currency_rate = Column(Numeric)
