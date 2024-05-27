import json
from client import TrelloClient
from models.board import Board
from models.list import List
from models.card import Card, Attachment
from models.checklist import Checklist
from dataclasses import asdict

API_KEY = '74cb777096ebf5bf89ba2ce5dbcc7391'
TOKEN = 'ATTAc1c8511419cdc00070a57b8955872a5e96ef67da82831fc1c975d5b073f74d6bE80CE80E'
BOARD_ID = '6649e8ae48d478e65373b854'
LIST_ID = '6649e8ae4ad55589838250fb'  # ID to do lista

#6649e8aef75814f0a8483c01 ID doing lista
#6649e8ae5c6cd545ed4d2855 ID done lista

client = TrelloClient(api_key=API_KEY, token=TOKEN)

def dataclass_to_dict(obj):
    if isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    elif hasattr(obj, "__dataclass_fields__"):
        return {key: dataclass_to_dict(value) for key, value in asdict(obj).items()}
    else:
        return obj

def fetch_board(board_id):
    endpoint = f'boards/{board_id}'
    data = client.get(endpoint)
    board = Board(id=data['id'], name=data['name'], url=data['url'])
    return board

def fetch_lists(board_id):
    endpoint = f'boards/{board_id}/lists'
    data = client.get(endpoint)
    lists = [List(id=item['id'], name=item['name'], board_id=board_id) for item in data]
    return lists

def fetch_cards(list_id):
    endpoint = f'lists/{list_id}/cards'
    data = client.get(endpoint)
    cards = []
    for item in data:
        attachments_endpoint = f'cards/{item["id"]}/attachments'
        attachments_data = client.get(attachments_endpoint)
        attachments = [Attachment(id=att['id'], name=att['name'], url=att['url']) for att in attachments_data]
        card = Card(id=item['id'], name=item['name'], desc=item.get('desc'), list_id=list_id, attachments=attachments)
        cards.append(card)
    return cards

def fetch_checklists(card_id):
    endpoint = f'cards/{card_id}/checklists'
    data = client.get(endpoint)
    checklists = []
    for item in data:
        checklist = Checklist(id=item['id'], name=item['name'], card_id=card_id, items=[check['name'] for check in item['checkItems']])
        checklists.append(checklist)
    return checklists

def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(dataclass_to_dict(data), f, indent=4)

def load_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def create_card(list_id, name, desc=''):
    endpoint = 'cards'
    data = {
        'idList': list_id,
        'name': name,
        'desc': desc
    }
    return client.post(endpoint, data=data)

def main():
    # uzimanje boarda
    board = fetch_board(BOARD_ID)
    save_to_file(board, 'board.json')

    # uzimanje liste
    lists = fetch_lists(BOARD_ID)
    save_to_file(lists, 'lists.json')

    # uzimanje kartice checkliste
    all_cards = []
    all_checklists = []
    for lst in lists:
        cards = fetch_cards(lst.id)
        all_cards.extend(cards)
        for card in cards:
            checklists = fetch_checklists(card.id)
            all_checklists.extend(checklists)

    save_to_file(all_cards, 'cards.json')
    save_to_file(all_checklists, 'checklists.json')

    # loadujemo fajlove
    print("\nLoaded data from files:")
    print("Board:", load_from_file('board.json'))
    print("Liste:", load_from_file('lists.json'))
    print("Kartice:", load_from_file('cards.json'))
    print("Ceckliste:", load_from_file('checklists.json'))


    list_id = input('Unesite list id: ')
    name = input('Unesite ime kartice: ')
    desc = input('Unesite opis kartice: ')


    print('Pravljenje nove kartice')
    new_card = create_card(list_id, name, desc)
    print(f"Nova kartica ID: {new_card['id']}, Ime: {new_card['name']}, Opis: {new_card['desc']}")

if __name__ == '__main__':
    main()
