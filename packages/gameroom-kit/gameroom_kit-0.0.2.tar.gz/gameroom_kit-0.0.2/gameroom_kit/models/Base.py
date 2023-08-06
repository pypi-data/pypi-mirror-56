from base64 import encodestring
import json, requests
from uuid import uuid1 as uuid
from time import time
from os import getenv

url = getenv('GAMEROOM_API_URL') if getenv('GAMEROOM_API_URL') else 'https://api.gameroomforpresident.com'
headers = {'Authorization': f'Bearer {getenv("GAMEROOM_TOKEN")}'}

class Base():
    def __init__(self):
        # Default attributes
        self.created_at = time()
        self.updated_at = time()
        self.id = str(uuid())
    # Class Methods
    @classmethod
    def create(self, **kwargs):
        # self.create(object) returns the saved object
        object = self(**kwargs)
        response = requests.post(url=f'{url}/{self.endpoint}', json=object.__dict__, headers=headers)
        return self(**response.json())
    @classmethod
    def find(self, id):
        # self.find(id) finds and returns an object
        response = requests.get(url=f'{url}/{self.endpoint}/{id}', headers=headers)
        return self(**response.json())
    @classmethod
    def delete(self, id):
        # self.delete(id) removes an object, returns nothing
        response = requests.delete(url=f'{url}/{self.endpoint}/{id}', headers=headers)
        return
    @classmethod
    def get(self, filter=dict(), sort=list(), limit=100, offset=0):
        # self.get(filter, sort, limit, offset) returns the list of objects
        params = dict(
            filter = encodestring(json.dumps(filter).encode()),
            sort = encodestring(json.dumps(sort).encode()),
            limit = limit,
            offset = offset
        )
        response = requests.get(url=f'{url}/{self.endpoint}', params=params, headers=headers)
        result = []
        for entry in response.json(): result.append(self(**entry))
        return result
    @classmethod
    def update(self, dict):
        #self.update(object) returns the updated object
        response = requests.put(url=f'{url}/{self.endpoint}/{dict["id"]}', json=dict, headers=headers)
        return self(**response.json())
    # Instance Methods
    def save(self):
        response = requests.put(url=f'{url}/{self.__class__.endpoint}/{self.id}', json=self.__dict__, headers=headers)
        return self.__class__(**response.json())
    def remove(self):
        response = requests.delete(url=f'{url}/{self.__class__.endpoint}/{self.id}', headers=headers)
        return
