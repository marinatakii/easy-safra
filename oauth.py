import requests
import time

class SafraOAuth2:
    def __init__(self, base64credentials):
        self.base64credentials = base64credentials
        self.__connect()

    def __connect(self):
        form = {
            'grant_type': 'client_credentials',
            'scope': 'urn:opc:resource:consumer::all'
        }
        headers = {
            'Authorization': 'Basic ' + self.base64credentials
        }
        self.connected_time = time.time()
        response = requests.post('https://idcs-902a944ff6854c5fbe94750e48d66be5.identity.oraclecloud.com/oauth2/v1/token', headers=headers, data=form)
        self.connected = response.status_code == 200
        if self.connected:
            access = response.json()
            self.access_type = access["token_type"]
            self.access_token = access["access_token"]
            self.expires_in = access["expires_in"]

    def is_connected(self):
        elapsed_time = time.time() - self.connected_time
        if elapsed_time >= self.expires_in:
            self.connected = False
        return self.connected

    def get_token_type(self):
        if not self.is_connected():
            self.__connect()
        if self.is_connected():
            return self.access_type
        else:
            return None

    def get_token(self):
        if not self.is_connected():
            self.__connect()
        if self.is_connected():
            return self.access_token
        else:
            return None
