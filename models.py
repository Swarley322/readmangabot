from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()


class Manga(Base):
    __tablename__ = 'manga'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    url = Column(String)
    img_url = Column(String)

    def __repr__(self):
        return "<Manga(title='{}')>" \
            .format(self.title)


class Subscribers(Base):
    __tablename__ = 'subscribers'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    user_id = Column(Integer, unique=True)
    chat_id = Column(Integer, unique=True)
    tracking_list = Column(JSON)
    active = Column(Boolean)

    def __repr__(self):
        return "<User(chat_id='{}', manga_tracking={})>" \
            .format(self.chat_id, self.tracking_list)


class Tracking(Base):
    __tablename__ = 'tracking'
    id = Column(Integer, primary_key=True)
    manga_id = Column(
            Integer,
            ForeignKey("manga.id", ondelete="CASCADE"),
            index=True
    )
    update_date = Column(Date)
    chapters = Column(JSON)
    number_of_chapters = Column(Integer)
    new_chapters = Column(Boolean)

    manga = relationship("Manga", backref="tracking")

    def __repr__(self):
        return "<Manga tracking(manga_id='{}', chapters={})>" \
            .format(self.manga_id, self.number_of_chapters)
