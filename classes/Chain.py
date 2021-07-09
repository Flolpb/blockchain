import hashlib
import os

from classes.Block import Block
from classes.Wallet import Wallet


class Chain:
    def __init__(self):
        self.blocs = []
        self.blocsToAdd = []
        self.last_base = 0
        self.number = self.get_last_transactions_number()

    def add_transaction(self, w1, w2, montant, bloc):
        if bloc.size < 256000:
            if os.path.exists("content/wallets/" + w1 + ".json"):
                if os.path.exists("content/wallets/" + w2 + ".json"):
                    emetteur = Wallet(0)
                    emetteur.load(w1)
                    recepteur = Wallet(0)
                    recepteur.load(w2)
                    if emetteur.balance >= montant:
                        self.number += 1
                        emetteur.send(recepteur,
                                      montant,
                                      bloc,
                                      str(self.number))
                    else:
                        print("The emitter doesnt have enough "
                              "money to do this transaction: {} < {}"
                              .format(emetteur.balance, montant))
                else:
                    print("The receiver id doesnt exist")
            else:
                print("The emitter id doesnt exist")
        else:
            print("size of the bloc is over the limit !")

    def find_transactions(self, name):
        for i in range(len(self.blocs)):
            if self.blocs[i].get_transaction(name) is not None:
                return self.blocs[i].get_transaction(name)
        return None

    def get_last_transactions_number(self):
        last_number = 0
        for i in range(len(self.blocs)):
            for j in range(len(self.blocs[i].transactions)):
                if int(self.blocs[i].transactions[j]['name']) > last_number:
                    last_number = int(self.blocs[i].transactions[j]['name'])
        return last_number

    def add_block(self):
        new_block = Block(self.blocs[len(self.blocs) - 1].hash,
                          self.generate_hash(), self.last_base)
        if new_block.check_hash():
            print("hash checked")
            self.blocs.append(new_block)
            new_block.save()
            new_block.get_weight()
            new_block.save()

    def get_block(self, hash):
        b = Block()
        b.load(hash)
        if b.hash == "00":
            self.blocs.append(b)
        else:
            if b.parent_hash == self.blocs[len(self.blocs) - 1].hash:
                self.blocs.append(b)
            else:
                self.blocsToAdd.append(b)

    def get_block_to_add(self, block):
        if block.parent_hash == self.blocs[len(self.blocs) - 1].hash:
            self.blocs.append(block)
        else:
            self.blocsToAdd.append(block)

    def generate_hash(self):
        find = False
        i = 0
        gen_hash = None
        while not find:
            i = i + 1
            str_i = str(i)
            gen_hash = hashlib.sha256(str_i.encode()).hexdigest()
            find = self.verify_hash(gen_hash)
        str_i = str(i)
        self.last_base = str_i
        return gen_hash

    def verify_hash(self, gen_hash):
        if gen_hash[0: 4] == "1000":
            if not os.path.exists("content/blocs/" + gen_hash + ".json"):
                return True
        return False
