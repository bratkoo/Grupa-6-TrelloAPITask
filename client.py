import requests

class TrelloClient:
    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token
        self.base_url = 'https://api.trello.com/1/'

    def _get_auth_params(self):
        return {
            'key': self.api_key,
            'token': self.token
        }

    def get(self, endpoint: str, params: dict = None):
        if params is None:
            params = {}
        params.update(self._get_auth_params())
        response = requests.get(f'{self.base_url}{endpoint}', params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict = None):
        if data is None:
            data = {}
        data.update(self._get_auth_params())
        response = requests.post(f'{self.base_url}{endpoint}', data=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict = None):
        if data is None:
            data = {}
        data.update(self._get_auth_params())
        response = requests.put(f'{self.base_url}{endpoint}', data=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str, params: dict = None):
        if params is None:
            params = {}
        params.update(self._get_auth_params())
        response = requests.delete(f'{self.base_url}{endpoint}', params=params)
        response.raise_for_status()
        return response.json()
