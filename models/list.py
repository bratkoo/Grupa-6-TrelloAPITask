from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class List(Base):
    __tablename__ = 'lists'

    id = Column(String, primary_key=True)
    name = Column(String)
    board_id = Column(String, ForeignKey('boards.id'))


    board = relationship("Board", back_populates="lists")
    cards = relationship("Card", back_populates="list", primaryjoin="List.id == Card.list_id")