from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, \
                       Table
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Readmanga(Base):
    __tablename__ = 'readmanga'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    url = Column(String, unique=True)
    img_url = Column(String)
    update_date = Column(Date)
    chapters = Column(JSON)
    number_of_chapters = Column(Integer)
    new_chapters = Column(Boolean)

    def __repr__(self):
        return "<ReadManga(id={}, title='{}')>" \
            .format(self.id, self.title)


class Mintmanga(Base):
    __tablename__ = 'mintmanga'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    url = Column(String, unique=True)
    img_url = Column(String)
    update_date = Column(Date)
    chapters = Column(JSON)
    number_of_chapters = Column(Integer)
    new_chapters = Column(Boolean)

    def __repr__(self):
        return "<MintManga(id={}, title='{}')>" \
            .format(self.id, self.title)


subs_mintmanga = Table(
    'tracking_mintmanga', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('mintmanga_id', Integer, ForeignKey('mintmanga.id'))
)

subs_readmanga = Table(
    'tracking_readmanga', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('readmanga_id', Integer, ForeignKey('readmanga.id'))
)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    user_id = Column(Integer, unique=True)
    chat_id = Column(Integer, unique=True)
    active = Column(Boolean)

    mintmanga = relationship(
                    "Mintmanga",
                    secondary=subs_mintmanga,
                    backref="mintmanga_subscribtions")
    readmanga = relationship(
                    "Readmanga",
                    secondary=subs_readmanga,
                    backref="readmanga_subscriptions")

    def __repr__(self):
        return "<User(chat_id='{}')>" \
            .format(self.chat_id)
