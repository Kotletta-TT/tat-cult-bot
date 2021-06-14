import sys
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

sys.path.insert(0, '..')
from config import DB_DRIVER, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

url = URL(drivername=DB_DRIVER, username=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_NAME,
          query={"charset": "utf8mb4"})

#url = 'sqlite:///main.db'

engine = create_engine(url, echo=True)


Session = sessionmaker(bind=engine)