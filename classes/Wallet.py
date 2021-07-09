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
        # test
        # unique_id = "b250dd3c-53c7-45a1-93cd-9e8ed3f8881d"
        if os.path.exists("content/wallets/" + unique_id + ".json"):
            self.generate_unique_id()

        return unique_id

    def add_balance(self, balance):
        self.balance += balance
        self.save()

    def sub_balance(self, balance):
        self.balance -= balance
        self.save()

    def send(self, recepteur, montant, bloc, name):
        bloc.add_transaction(self, recepteur, montant, name)
        new_transaction = {'emetteur': self.unique_id,
                           'recepteur': recepteur.unique_id,
                           'montant': montant,
                           'name': name}
        recepteur.history.append(new_transaction)
        recepteur.save()
        self.history.append(new_transaction)
        self.save()

    def info(self):
        print("------------------------------------")
        print("uuid: " + self.unique_id)
        print("balance: " + str(self.balance))
        print("history: " + str(self.history))
        print("------------------------------------")

    def save(self):
        with open("content/wallets/" + self.unique_id + ".json",
                  'w') as outfile:
            data = {
                'unique_id': self.unique_id,
                'balance': self.balance,
                'history': []
            }

            for i in range(len(self.history)):
                data['history'].append({
                    'emetteur': self.history[i]['emetteur'],
                    'recepteur': self.history[i]['recepteur'],
                    'montant': self.history[i]['montant'],
                    'name': self.history[i]['name'],
                })

            json.dump(data, outfile)

    def load(self, unique_id):
        if os.path.exists("content/wallets/" + unique_id + ".json"):
            with open("content/wallets/" + unique_id + ".json") as json_file:
                data = json.load(json_file)
                self.unique_id = data['unique_id']
                self.balance = data['balance']
                self.history = data['history']
        else:
            print("try loading a wallet that doesnt exist")
