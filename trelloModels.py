from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import DatabaseConnection


Base = declarative_base()
engine = create_engine('sqlite:///trello.db')
#Base.metadata.create_all(engine)
db_connection = DatabaseConnection('sqlite:///trello.db')

class Board(Base):
    __tablename__ = 'boards'

    id = Column(String, primary_key=True)
    name = Column(String)

    lists = relationship("List", back_populates="board")

class List(Base):
    __tablename__ = 'lists'

    id = Column(String, primary_key=True)
    name = Column(String)
    board_id = Column(String, ForeignKey('boards.id'))

    board = relationship("Board", back_populates="lists")
    cards = relationship("Card", back_populates="list")

class Card(Base):
    __tablename__ = 'cards'

    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    list_id = Column(String, ForeignKey('lists.id'))

    list = relationship("List", back_populates="cards")
    checklists = relationship("Checklist", back_populates="card")
    attachments = relationship("Attachment", back_populates="card")
    comments = relationship("Comment", back_populates="card")

class Checklist(Base):
    __tablename__ = 'checklists'

    id = Column(String, primary_key=True)
    name = Column(String)
    card_id = Column(String, ForeignKey('cards.id'))

    card = relationship("Card", back_populates="checklists")

class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(String, primary_key=True)
    file_path = Column(String)
    card_id = Column(String, ForeignKey('cards.id'))

    card = relationship("Card", back_populates="attachments")

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(String, primary_key=True)
    text = Column(String)
    card_id = Column(String, ForeignKey('cards.id'))

    card = relationship("Card", back_populates="comments")

Base.metadata.create_all(engine)
