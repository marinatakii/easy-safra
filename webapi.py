import requests
import json
from oauth import SafraOAuth2

OK_CODE = 200
CREATED_CODE = 201


class SafraWebAPI:
    def __init__(self, base64credentials, account_id):
        self.auth = SafraOAuth2(base64credentials)
        self.account_id = account_id

    def serialize(self):
        return self.account_id

    @staticmethod
    def deserialize(credentials, serialized):
        return SafraWebAPI(credentials, serialized)

    def is_valid_account(self):
        return self.account_id is not None

    def is_connected(self):
        return self.auth.is_connected()

    def __base_url(self):
        return 'https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/'

    def __open_banking_url(self):
        return self.__base_url() + "open-banking/v1"

    def __media_url(self):
        return self.__base_url() + "media/v1"

    def __accounts_url(self):
        return self.__base_url() + "accounts/v1"

    def __headers(self):
        token_type = self.auth.get_token_type()
        token = self.auth.get_token()
        return {
            'Authorization' : '{} {}'.format(token_type, token)
        }

    def __get(self, method):
        headers = self.__headers()
        response = requests.get(self.__open_banking_url() + method, headers=headers)
        if response.status_code == OK_CODE:
            json = response.json()
            return json.get("Data") or json.get("data")

    def __get_media(self, method):
        headers = self.__headers()
        response = requests.get(self.__media_url() + method, headers=headers)
        if response.status_code == OK_CODE:
            json = response.json()
            return json.get("Data") or json.get("data")

    def __post(self, method, json):
        headers = self.__headers()
        response = requests.post(self.__accounts_url() + method, headers=headers, json=json)
        if response.status_code == CREATED_CODE and len(response.content) > 0:
            return response.json().get("Data")

    def get_account_info(self):
        response = self.__get("/accounts/{}".format(self.account_id))
        if response:
            return response["Account"][0]

    def get_balances(self):
        response = self.__get("/accounts/{}/balances".format(self.account_id))
        if response:
            return response["Balance"][0]

    def get_transactions(self):
        response = self.__get("/accounts/{}/transactions".format(self.account_id))
        if response:
            return response["transaction"]

    def get_morning_call(self):
        response = self.__get_media("/youtube?fromData=2020-07-09&toData=2020-07-14&playlist=morningCalls&channel=safra")
        return response


    def make_transfer(self, name, value, description):
        json = {
            "Amount": {
                "Amount": "250.00",
                "Currency": "BRL"
            },
            "DestinyAccount": {
                "Bank": "422",
                "Agency": "0071",
                "Id": "1234533",
                "Cpf": "12345678933",
                "Name": "Mark Zuckerberg da Silva",
                "Goal":"Credit"
            },
            "Type": "TEF",
            "TransactionInformation": "Mensalidade Academia"
        }
        return self.__post("/accounts/{}/transfers".format(self.account_id), json)

    def opt_in(self):
        json = {
            "Name": "Eric Evans Silva",
            "Email": "eric.evans@ddd.com",
            "Phone": "+5511911111111"
        }
        return self.__post("/optin", json)
