from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    page = Column(Integer)
    bookmarks = Column(ARRAY(Integer))


engine = create_engine('postgresql://postgres:password@db/book_tg_users')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
