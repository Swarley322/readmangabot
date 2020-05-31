from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI

engine = create_engine(DATABASE_URI, echo=False)

Session = sessionmaker(bind=engine)

s = Session()
