import requests
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from database import Database
from models.card import Card
from models.list import List


app = FastAPI()
db = Database('sqlite:///trello.db')


# Modeli za request body
class NewCard(BaseModel):
    title: str
    description: str = None
    list_id: int


class NewList(BaseModel):
    name: str
    board_id: str  # Treba da bude string jer Trello API koristi string ID-jeve


# Servisi
class BoardService:
    @staticmethod
    def get_board(board_id):
        # Implementacija za dohvatanje board-a iz baze
        pass


class CardService:
    @staticmethod
    def get_card(card_id):
        # Implementacija za dohvatanje kartice iz baze
        pass

    @staticmethod
    def create_card(new_card: NewCard):
        # Kreiranje nove kartice u bazi
        db.create(new_card)

        # Kreiranje kartice na Trello-u
        url = "https://api.trello.com/1/cards"
        query = {
            "key": "74cb777096ebf5bf89ba2ce5dbcc7391",
            "token": "ATTAc1c8511419cdc00070a57b8955872a5e96ef67da82831fc1c975d5b073f74d6bE80CE80E",
            "name": new_card.title,
            "desc": new_card.description,
            "idList": new_card.list_id
        }
        response = requests.post(url, params=query)
        if not response.ok:
            raise HTTPException(status_code=response.status_code, detail="Failed to create card on Trello")

        # Ako je kreiranje na Trello-u uspešno, ažuriramo zapis u bazi podataka sa informacijama o kreiranoj kartici
        created_card_data = response.json()
        created_card = Card(id=created_card_data['id'], title=created_card_data['name'],
                            description=created_card_data.get('desc', ''), list_id=created_card_data['idList'])
        db.update(created_card)

        # Vraćanje odgovora sa potvrdom


class ListService:
    @staticmethod
    def get_list(list_id):
        # Implementacija za dohvatanje liste iz baze
        pass

    @staticmethod
    def create_list(new_list: NewList):
        # Kreiranje nove liste u bazi
        db.create(new_list)

        # Kreiranje liste na Trello-u
        url = "https://api.trello.com/1/lists"
        query = {
            "key": "74cb777096ebf5bf89ba2ce5dbcc7391",
            "token": "ATTAc1c8511419cdc00070a57b8955872a5e96ef67da82831fc1c975d5b073f74d6bE80CE80E",
            "name": new_list.name,
            "idBoard": new_list.board_id
        }
        response = requests.post(url, params=query)
        if not response.ok:
            raise HTTPException(status_code=response.status_code, detail="Failed to create list on Trello")

        # Ako je kreiranje na Trello-u uspešno, ažuriramo zapis u bazi podataka sa informacijama o kreiranoj listi
        created_list_data = response.json()
        created_list = List(id=created_list_data['id'], name=created_list_data['name'],
                            board_id=created_list_data['idBoard'])
        db.update(created_list)

# Rute...

@app.post("/cards/", response_model=None)
async def create_card(card_data: NewCard):
    return CardService.create_card(card_data)

@app.post("/lists/", response_model=None)
async def create_list(list_data: NewList):
    return ListService.create_list(list_data)