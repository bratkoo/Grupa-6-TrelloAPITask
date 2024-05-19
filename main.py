import requests


API_KEY = '74cb777096ebf5bf89ba2ce5dbcc7391'
TOKEN = 'ATTAc1c8511419cdc00070a57b8955872a5e96ef67da82831fc1c975d5b073f74d6bE80CE80E'
BOARD_ID = '6649e8ae48d478e65373b854'
LIST_ID = '6649e8ae4ad55589838250fb'

BASE_URL = 'https://api.trello.com/1/'

def get_all_cards(board_id):
    url = f'{BASE_URL}boards/{board_id}/cards'
    query = {
        'key': API_KEY,
        'token': TOKEN
    }
    response = requests.get(url, params=query)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Greska: {response.status_code}')
        return None

def create_card(list_id, name, desc=''):
    url = f'{BASE_URL}cards'
    query = {
        'idList': list_id,
        'name': name,
        'desc': desc,
        'key': API_KEY,
        'token': TOKEN
    }
    response = requests.post(url, params=query)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Greska: {response.status_code}')
        return None

def main():
    print('Prikupljivanje svih kartica........')
    cards = get_all_cards(BOARD_ID)
    if cards is not None:
        for card in cards:
            print(f"Card ID: {card['id']}, Name: {card['name']}, Description: {card['desc']}")

    name = input('Unesite ime nove kartice ')
    desc = input('Unesite opis nove kartice: ')

    print('Pravljenje nove kartice...........')
    new_card = create_card(LIST_ID, name, desc)
    if new_card is not None:
        print(f"Nova kartica ID: {new_card['id']}, Name: {new_card['name']}, Description: {new_card['desc']}")


if __name__ == '__main__':
    main()