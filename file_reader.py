import json
from dataclasses import dataclass
import os
import requests

trello_key = '74cb777096ebf5bf89ba2ce5dbcc7391'
trello_token = 'ATTAc1c8511419cdc00070a57b8955872a5e96ef67da82831fc1c975d5b073f74d6bE80CE80E'

@dataclass
class FileReader:
    directory: str

    # metoda za citanje JSON fajlova
    def read_file(self, name):
        with open(self.directory + name, 'r') as file:
            content = json.load(file)
            print(json.dumps(content, indent=4))

    # metoda za cuvanje JSON fajlova
    def save_file(self, name, content):
        with open(self.directory + name, 'w') as file:
            json.dump(content, file, indent=4)
        print("File saved to /" + self.directory + name)

    # metoda za prikaz fajlova u direktorijumu
    def all_files(self):
        files = os.listdir(self.directory)
        print(files)

    # metoda za citanje svih fajlova
    def print_all(self):
        for f in os.listdir(self.directory):
            if f.endswith(".json"):
                print("File name: " + f)
                with open(self.directory + f, 'r') as file:
                    content = json.load(file)
                    print(json.dumps(content, indent=4))
                print("----------")
            else:
                print("File name: " + f)
                print("----------")

    # metoda za preuzimanje attachmenta
    def download_attachment(self, attachment_id, name, url):
        headers = {
            "Authorization": "OAuth oauth_consumer_key=\"" + API.trello_key +
                             "\", oauth_token=\"" + API.trello_token + "\""
        }
        content = requests.get(url, stream=True, headers=headers).content
        with open(self.directory + attachment_id + name, 'wb') as f:
            f.write(content)
        print("File saved to /" + self.directory + attachment_id + name)