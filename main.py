from genericClient import GenericClient
from models.card import Card
from fileManager import FileManager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from trelloModels import Board as BoardTrello
from trelloModels import List as ListaTrello
from trelloModels import Card as CardTrello
from trelloModels import Checklist as CheckListTrello

engine = create_engine('sqlite:///trello.db')
Session = sessionmaker(bind=engine)
session = Session()

client = GenericClient("74cb777096ebf5bf89ba2ce5dbcc7391",
                       "ATTAc1c8511419cdc00070a57b8955872a5e96ef67da82831fc1c975d5b073f74d6bE80CE80E",
                       "https://api.trello.com/1")
file_manager = FileManager('.')

try:
    fetched_board_data = client.get("boards/6649e8ae48d478e65373b854")

    board1 = BoardTrello(id=fetched_board_data.get("id"), name=fetched_board_data.get("name"))
    session.add(board1)
    session.commit()
    print("Dodat board")

except Exception as e:
    print(f"An error occurred: {e}")

try:
    fetched_list_data = client.get("lists/6649e8ae4ad55589838250fb")
    lista1 = ListaTrello(id=fetched_list_data.get("id"), name=fetched_list_data.get("name"),
                         board_id="6649e8ae48d478e65373b854")
    session.add(lista1)
    session.commit()
    print("Dodata lista")
except AttributeError as e:
    print(f"Attribute error: {e}")
except KeyError as e:
    print(f"Key error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

cards = []
checklists = []
fetched_card_data = client.get("boards/6649e8ae48d478e65373b854/cards")
for card in fetched_card_data:
    session.add(CardTrello(id=card.get("id"), title=card.get("name"), description=card.get("desc"),
                           list_id="6649e8ae4ad55589838250fb"))
    session.commit()
    print("Dodata kartica")

cards = []
checklists = []
try:
    fetched_card_data = client.get("boards/6649e8ae48d478e65373b854/cards")
    for card in fetched_card_data:
        try:
            cards.append(Card(card.get("id"), card.get("name"), card.get("desc"), card.get("shortUrl")))
            card_checklist_data = client.get(f'cards/{card.get("id")}/checklists')
            for checklist_data in card_checklist_data:
                try:
                    session.add(CheckListTrello(id=checklist_data.get("id"),name=checklist_data.get("name"),card_id="1exGxmdw"))
                    session.commit()
                    print("Dodat checlist")
                except Exception as e:
                    print(f"Doslo je do greske checklista: {e}")
        except Exception as e:
            print(f"Doslo je do greske kartice: {e}")

except Exception as e:
    print(f"Nije moguce prikupiti karticu: {e}")





