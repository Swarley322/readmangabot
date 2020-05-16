from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI

engine = create_engine(DATABASE_URI)

session = sessionmaker(bind=engine)

s = session()

# alembic revision --autogenerate -m ""
# alembic upgrade head