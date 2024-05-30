import requests

TRELLO_API_KEY = "your_trello_api_key"
TRELLO_TOKEN = "your_trello_token"

def create_trello_card(list_id: str, name: str, desc: str):
    url = f"https://api.trello.com/1/cards"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idList': list_id,
        'name': name,
        'desc': desc
    }
    response = requests.post(url, params=query)
    return response.json()

def create_trello_list(board_id: str, name: str):
    url = f"https://api.trello.com/1/lists"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idBoard': board_id,
        'name': name
    }
    response = requests.post(url, params=query)
    return response.json()
