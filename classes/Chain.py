import hashlib
import os

from classes.Wallet import Wallet


class Chain:
    def __init__(self):
        self.blocs = []

    def new_transaction(self, w1, w2, montant, bloc):
        if bloc.size < 256000:
            if os.path.exists("content/wallets/" + w1 + ".json"):
                if os.path.exists("content/wallets/" + w2 + ".json"):
                    emetteur = Wallet(0)
                    emetteur.load(w1)
                    recepteur = Wallet(0)
                    recepteur.load(w2)
                    if emetteur.balance > montant:
                        emetteur.send(recepteur, montant, bloc)
