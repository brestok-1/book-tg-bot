from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from config_data.config import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    active_book = Column(VARCHAR(125), nullable=True)
    page = Column(Integer, nullable=True)
    bookmarks = relationship('Bookmark', back_populates='user')

    def __str__(self):
        return f'<User:{self.user_id}>'


class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    book = Column(VARCHAR(125))
    page = Column(Integer)

    def __str__(self):
        return f'<Bookmark:{self.book} - {self.page}'
