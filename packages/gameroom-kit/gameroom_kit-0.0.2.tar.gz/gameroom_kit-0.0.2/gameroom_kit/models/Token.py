from os import getenv
import json, requests
from base64 import encodestring

url = '{}/token'.format(getenv('GAMEROOM_API_URL'))
headers = {'Authorization': 'Bearer {}'.format(getenv('GAMEROOM_TOKEN'))}

class Token:
    def __init__(self, **kwargs):
        # Default attributes
        self.token = None
        self.user = dict()
        # Supplied attributes
        for key, value in kwargs.items():
            if (hasattr(self, key)): setattr(self, key, value)
    # Class Methods
    @classmethod
    def get(email, password):
        response = requests.get(url=url, headers=headers)
        return Token(**response.json())
    # Instance Methods
