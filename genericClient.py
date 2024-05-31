from dataclasses import dataclass
import requests

@dataclass
class GenericClient:
    api_key: str
    api_token: str
    base_url: str

    def get(self, endpoint: str) -> dict:
        url = f"{self.base_url}/{endpoint}"
        query = {
         'key': self.api_key,
         'token': self.api_token
        }
        response = requests.get(url, params=query, timeout=10)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict) -> dict:
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_attachment(self, url: str) -> dict:
        headers = {"Authorization": f"OAuth oauth_consumer_key=\"{self.api_key}\", oauth_token=\"{self.api_token}\""}
        query = {
         'key': self.api_key,
         'token': self.api_token
        }
        response = requests.get(url, headers=headers, timeout=10)
        return response
