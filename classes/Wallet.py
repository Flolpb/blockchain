import os
import uuid
import json


class Wallet:
    def __init__(self, balance):
        self.unique_id = self.generate_unique_id()
        self.balance = balance
        self.history = []

    def generate_unique_id(self):
        unique_id = str(uuid.uuid4())
        #test
        #unique_id = "b250dd3c-53c7-45a1-93cd-9e8ed3f8881d"
        if os.path.exists("content/wallets/" + unique_id + ".json"):
            self.generate_unique_id()

        return unique_id

    def add_balance(self, balance):
        self.balance += balance

    def sub_balance(self, balance):
        self.balance -= balance

    def send(self):
        pass

    def save(self):
        with open("content/wallets/" + self.unique_id + ".json", 'w') as outfile:
            data = {'unique_id': self.unique_id, 'balance': self.balance, 'history': self.history}
            json.dump(data, outfile)

    def load(self, unique_id):
        with open("content/wallets/" + unique_id + ".json") as json_file:
            data = json.load(json_file)
            self.unique_id = data['unique_id']
            self.balance = data['balance']
            self.history = data['history']
