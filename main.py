import sqlalchemy
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import httpx
import requests
from sqlalchemy.orm import sessionmaker

from models.card import Card
from database import Database
from sqlalchemy import create_engine
from typing import List, Optional

app = FastAPI()

TRELLO_API_KEY = "74cb777096ebf5bf89ba2ce5dbcc7391"
TRELLO_API_TOKEN = "ATTAc1c8511419cdc00070a57b8955872a5e96ef67da82831fc1c975d5b073f74d6bE80CE80E"

DATABASE_URL = "sqlite:///trello.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

class CardUpdate(BaseModel):
    id: str
    title: Optional[str]
    description: Optional[str]
    list_id: Optional[str]

async def get_cards_from_trello(board_id: str) -> List[CardUpdate]:
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    params = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_API_TOKEN
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        cards = response.json()
        return [CardUpdate(**{key: card[key] for key in CardUpdate.__annotations__.keys() if key in card}) for card in cards]


def get_card_by_id(card_id):
    with SessionLocal() as session:
        card = session.query(Card).filter_by(id=card_id).first()
        return card


async def save_cards_to_database(cards: List[CardUpdate]):
    db = Database(DATABASE_URL)
    for card_update in cards:
        card_id = card_update.id
        existing_card = get_card_by_id(card_id)
        if existing_card is None:
            new_card = Card(
                id=card_update.id,
                title=card_update.title,
                description=card_update.description,
                list_id=card_update.list_id
            )
            await db.create(new_card)
        else:
            existing_card.title = card_update.title
            existing_card.description = card_update.description
            existing_card.list_id = card_update.list_id
            await db.update(existing_card)

@app.post("/update-cards/{board_id}")
async def update_cards(background_tasks: BackgroundTasks, board_id: str):
    cards_from_trello = await get_cards_from_trello(board_id)
    background_tasks.add_task(save_cards_to_database, cards_from_trello)
    return {"message": f"Baza kartica azurirana za board ID: {board_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
