from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, Text
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    active_book = Column(VARCHAR(125), nullable=True)
    page = Column(Integer, default=1)
    bookmarks = relationship("Bookmark", back_populates='user')
    contents_page = Column(Integer, default=0)

    def __str__(self):
        return f'<User:{self.user_id}>'


class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates='bookmarks')
    book = Column(VARCHAR(125))
    page = Column(Integer)

    def __str__(self):
        return f'<Bookmark:{self.book} - {self.page}'


class Book(Base):
    __tablename__ = 'books'
    title = Column(VARCHAR(125), primary_key=True)
    content = Column(Text)
    author = Column(VARCHAR(125))

    def __eq__(self, other):
        if isinstance(other, Book):
            return (
                    self.title == other.title and
                    self.content == other.content and
                    self.author == other.author
            )
        return False

