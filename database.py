# database.py
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.future import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from models.card import Card
from models.list import List
from models.board import Board
from models.checklist import Checklist
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Database:
    def __init__(self, db_uri):
        # Inicijalizacija Engine-a za povezivanje sa bazom
        self.engine = create_engine(db_uri)
        # Kreiranje Session klase
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        # Metoda za dobijanje Session objekta
        return self.Session()

    async def create(self, card):
        with SessionLocal() as session:
            session.add(card)
            session.commit()

    def read_all(self, model):
        # Metoda za čitanje svih zapisa iz baze
        session = self.get_session()
        objects = session.query(model).all()
        session.close()
        return objects


    def read_by_id(self, model, id):
        # Metoda za čitanje zapisa po ID-u iz baze
        session = self.get_session()
        obj = session.query(model).filter_by(id=id).first()
        session.close()
        return obj

    async def update(self, card):
        with SessionLocal() as session:
            session.merge(card)
            session.commit()
    def delete(self, obj):
        # Metoda za brisanje zapisa iz baze
        session = self.get_session()
        session.delete(obj)
        session.commit()
        session.close()

    def get_list_by_id(self, list_id):
        session = self.Session()
        card = session.query(Card).filter_by(id=list_id).first()
        session.close()
        return list
