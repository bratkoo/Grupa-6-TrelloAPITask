from dataclasses import dataclass
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base


class Card(Base):
    __tablename__ = 'cards'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    list_id = Column(String, ForeignKey('lists.id'))
    list = relationship("List", back_populates="cards")
    checklists = relationship("Checklist", back_populates="card")

