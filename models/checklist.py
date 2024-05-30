from dataclasses import dataclass
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


@dataclass
class Checklist(Base):
    __tablename__ = 'checklists'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    card_id = Column(String, ForeignKey('cards.id'))
    card = relationship("Card", back_populates="checklists")
