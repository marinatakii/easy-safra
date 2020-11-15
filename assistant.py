from webapi import SafraWebAPI
import json

credentials = "OThiMmEwZDY0MWQ0NDFmZDhmMWQyOTdlNDg3NjFmMzk6ZDczMjU5YWYtYzJhZC00MTMzLWI0NjEtNDYyN2IwN2VlMDZj"

class SafraAssistant:
    def __init__(self):
        self.api = None

    def serialize(self):
        if self.api:
            return self.api.serialize()

    @staticmethod
    def deserialize(serialized):
        assistant = SafraAssistant()
        assistant.api = SafraWebAPI.deserialize(credentials, serialized)
        return assistant

    def start_session(self):
        return "Assisting you as Easy Safra."

    def __get_full_name_from_id(self, id):
        if id == "00711234533":
            return "Mark Zuckerberg da Silva"
        if id == "00711234511":
            return "Susan Wojcicki da Silva"
        if id == "00711234522":
            return "Satya Nadella da Silva"

    def __get_user_id_from_name(self, name):
        # Workaround, because Alexa understands "Susan" as "Suzanne"
        if name.lower() == "susan" or name.lower() == "suzanne":
            return "00711234511"
        # Workaround, because Alexa understands "Mark" as "Marc"
        if name.lower() == "mark" or name.lower() == "marc":
            return "00711234533"
        if name.lower() == "satya":
            return "00711234522"

    def __get_user_name_by_id(self, id):
        if id == "00711234511":
            return "Susan"
        if id == "00711234533":
            return "Mark"
        if id == "00711234522":
            return "Satya"

    def login(self, name):
        account_id = self.__get_user_id_from_name(name)
        if account_id:
            self.api = SafraWebAPI(credentials, account_id)
            account_info = self.api.get_account_info()
            return "Logging into {}'s account.".format(account_info["Nickname"])
        else:
            return "I couldn't find any account for {}.".format(name)

    def get_balances(self):
        balances = self.api.get_balances()
        account_balance = balances["Amount"]["Amount"]
        credit_balance = balances["CreditLine"][0]["Amount"]["Amount"]
        return "Your account balance is R${}. You also have R${} in your credit line.".format(account_balance,
                                                                                              credit_balance)

    def make_transfer(self, name, value, description):
        id = self.__get_user_id_from_name(name)
        full_name = self.__get_full_name_from_id(id) # we should also get registered info such as cpf, bank # and agency
        transfer = self.api.make_transfer(full_name, value, description)
        value = transfer["Amount"]["Amount"]
        name = transfer["DestinyAccount"]["Name"]
        description = transfer["TransactionInformation"]

        balances = self.api.get_balances()
        account_balance = balances["Amount"]["Amount"]
        balance = float(account_balance) - float(value)

        return "R${} transfer made to {} as {}. Your current balance is R${}.".format(value, name, description, balance)

    def find_received_transfer_by_value(self, value):
        transactions = self.api.get_transactions()
        for transaction in transactions:
            if float(transaction["amount"]["amount"]) == value:
                return "Found a R${} transfer described as {}.".format(value, transaction["transactionInformation"])
        return "I couldn't find any R${} transfer.".format(value)

    def find_received_transfer_from_name(self, name):
        from_id = self.__get_user_id_from_name(name)
        if from_id is None:
            return "I can't find {}'s account number."
        full_name = self.__get_full_name_from_id(from_id)
        api = SafraWebAPI(credentials, from_id)
        from_transactions = api.get_transactions()
        transactions = self.api.get_transactions()
        for from_transaction in from_transactions:
            for transaction in transactions:
                if from_transaction["transactionId"] == transaction["transactionId"] and from_transaction["valueDateTime"] == transaction["valueDateTime"]:
                    return "Found a R${} transfer from {} described as {}.".format(transaction["amount"]["amount"], full_name, transaction["transactionInformation"])
        return "I couldn't find any transfer from {}.".format(full_name)

    def play_morning_call(self):
        morning_calls = self.api.get_morning_call()
        morning_call = morning_calls[0]
        audio_url = ""
        for link in morning_call["links"]:
            if link["rel"] == "audioFile":
                audio_url = link["href"]
        return morning_call["description"], audio_url

    def get_help(self):
        return "You can ask me to make a transfer, to tell your account balance, to find any received transfer by value or to play the morning call."


if __name__ == "__main__":
    assistant = SafraAssistant()
    print("[You] Alexa, start Easy Safra.")
    print("[Alexa]", assistant.start_session())
    print("[You] Login as Susan.")
    print("[Alexa]", assistant.login("Susan"))
    print("[You] Get account balances.")
    print("[Alexa]", assistant.get_balances())
    print("[You] Alexa, please make a 250.00 transfer to Mark Zuckerberg da Silva.")
    print("[Alexa] How would you like to describe this transfer?")
    print("[You] Gym Membership.")
    print("[Alexa]", assistant.make_transfer("Mark", 250.0, "Gym Membership"))
    print("")
    print("[You] Login as Mark.")
    print("[Alexa]", assistant.login("Mark"))
    print("[You] What's my account balance?")
    print("[Alexa]", assistant.get_balances())
    print("[You] Did I get a transfer from Susan?")
    print("[Alexa]", assistant.find_received_transfer_from_name("Susan"))
    print("[You] Play the morning call.")
    print("[Alexa]", assistant.play_morning_call()[0])