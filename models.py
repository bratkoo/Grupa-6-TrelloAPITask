from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lists = relationship("List", back_populates="board")

class List(Base):
    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    board_id = Column(Integer, ForeignKey('boards.id'), nullable=False)
    board = relationship("Board", back_populates="lists")
    cards = relationship("Card", back_populates="list")

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable=False)
    list = relationship("List", back_populates="cards")
    comments = relationship("Comment", back_populates="card")

class Checklist(Base):
    __tablename__ = 'checklists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    card_id = Column(Integer, ForeignKey('cards.id'), nullable=False)
    card = relationship("Card", back_populates="checklists")

class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    card_id = Column(Integer, ForeignKey('cards.id'), nullable=False)
    card = relationship("Card", back_populates="attachments")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    card_id = Column(Integer, ForeignKey('cards.id'), nullable=False)
    card = relationship("Card", back_populates="comments")
