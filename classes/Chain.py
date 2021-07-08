import hashlib
import os

from classes.Wallet import Wallet


class Chain:
    def __init__(self):
        self.blocs = []
        self.number = self.get_last_transactions_number()

    def new_transaction(self, w1, w2, montant, bloc):
        if bloc.size < 256000:
            if os.path.exists("content/wallets/" + w1 + ".json"):
                if os.path.exists("content/wallets/" + w2 + ".json"):
                    emetteur = Wallet(0)
                    emetteur.load(w1)
                    recepteur = Wallet(0)
                    recepteur.load(w2)
                    if emetteur.balance > montant:
                        self.number += 1
                        emetteur.send(recepteur, montant, bloc, str(self.number))

    def find_transactions(self, name):
        for i in range(len(self.blocs)):
            if self.blocs[i].get_transactions(name) is not None:
                return self.blocs[i].get_transactions(name)
        return None

    def get_last_transactions_number(self):
        last_number = 0
        for i in range(len(self.blocs)):
            for j in range(len(self.blocs[i].transactions)):
                if int(self.blocs[i].transactions[j]['name']) > last_number:
                    last_number = int(self.blocs[i].transactions[j]['name'])

        return last_number
