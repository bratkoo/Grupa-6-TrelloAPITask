from fastapi import FastAPI
from genericClient import GenericClient
from models.board import Board
from models.list import List
from models.card import Card
from models.checkList import CheckList
from models.comment import Comment
from fileManager import FileManager
import requests

from trelloModels import List as ListaTrello
from trelloModels import Card as CardTrello

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///trello.db')
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()
client = GenericClient("737f990a50b95a1db675188c99175c8a",
                       "ATTA7d15664b7f73521ad1fafa12717b24d6de9136f780224304473d52fe59b0452e0935F6AF",
                       "https://api.trello.com/1")


# 127.0.0.1:8000/boards/6645fee8d15bb6bc3076c8e9                      -- Radi
@app.get("/boards/{board_id}")
async def getBoardInfo(board_id):
    fetched_board_data = client.get(f"boards/{board_id}")
    board = Board(
        fetched_board_data.get("id"),
        fetched_board_data.get("name"),
        fetched_board_data.get("desc"),
        fetched_board_data.get("shortUrl")
    )

    return board


# http://127.0.0.1:8000/cards/OidP4NJH                               -- Radi
comments = []


@app.get("/cards/{card_id}")
async def getComment(card_id):
    card_comments_data = client.get(f'cards/{card_id}/actions?filter=commentCard')
    for attachment_data in card_comments_data:
        comment = Comment(
            attachment_data.get("id"),
            attachment_data.get("idMemberCreator"),
            attachment_data.get("date"),
            attachment_data['data']['text']
        )
        comments.append(comment)
    return comments


cards = []


# 127.0.0.1:8000/lists/66460051007109943d036a44                      -- Radi
@app.get("/lists/{list_id}")
async def getListInfo(list_id):
    fetched_card_data = client.get("boards/6645fee8d15bb6bc3076c8e9/cards")
    for card in fetched_card_data:
        cards.append(Card(card.get("id"), card.get("name"), card.get("desc"), card.get("shortUrl")))
    return cards


# http://127.0.0.1:8000/card/66460051007109943d036a44                -- Radi kroz docs
@app.post("/card/{list_id}")
async def napravi_karticu(list_id):
    api_key = "737f990a50b95a1db675188c99175c8a"
    token = "ATTA7d15664b7f73521ad1fafa12717b24d6de9136f780224304473d52fe59b0452e0935F6AF"
    url_post = "https://api.trello.com/1/cards"
    name = "nova kartica"
    desc = "deskripcija"
    query_post = {"key": api_key, "token": token, "name": name, "desc": desc, "idList": list_id}
    response = requests.post(url_post, query_post, timeout=10)
    session.add(CardTrello(id="", title=name, description=desc, list_id=list_id))
    session.commit()


# http://127.0.0.1:8000/list/6645fee8d15bb6bc3076c8e9                -- Radi kroz docs
@app.post("/list/{board_id}")
async def nova_lista(board_id):
    api_key = "737f990a50b95a1db675188c99175c8a"
    token = "ATTA7d15664b7f73521ad1fafa12717b24d6de9136f780224304473d52fe59b0452e0935F6AF"
    url_post = "https://api.trello.com/1/lists"
    name = "NovaLista"
    query_post = {"name": name, "idBoard": board_id, "key": api_key, "token": token}
    response = requests.post(url_post, query_post, timeout=10)
    session.add(ListaTrello(id="", name=name, board_id=board_id))
    session.commit()
