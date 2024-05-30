from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Board(Base):
    __tablename__ = 'boards'

    id = Column(String, primary_key=True)
    name = Column(String)

    lists = relationship("List", back_populates="board")