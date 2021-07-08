import hashlib
import json
import os
import random
import string


class Block:
    def __init__(self, parent_hash=None):
        self.size = 0
        self.base_hash = hashlib.sha256()
        self.hash = self.generate_hash()
        self.parent_hash = parent_hash
        self.blocks = []
        self.transactions = []
        self.last_transaction = None

    def generate_hash(self):
        find = False
        i = 0
        gen_hash = None
        while not find:
            i = i + 1
            str_i = str(i)
            gen_hash = hashlib.sha256(str_i.encode()).hexdigest()
            find = self.verify_hash(gen_hash=gen_hash)
        return gen_hash

    def verify_hash(self, gen_hash):
        if gen_hash[0: 4] == "1000":
            if not os.path.exists("content/wallets/" + gen_hash + ".json"):
                return True
        return False

    def add_transaction(self, w1, w2, montant, name):
        w1.sub_balance(montant)
        w2.add_balance(montant)
        new_transactions = {'emetteur': w1.unique_id, 'recepteur': w2.unique_id, 'montant': montant, 'name': name}
        self.last_transaction = new_transactions
        self.transactions.append(new_transactions)
        self.save()
        self.get_weight()
        self.save()

    def get_transaction(self, name):
        for i in range(len(self.transactions)):
            x = self.transactions[i]['name'].find(name)
            if x != -1:
                return self
        return None

    def get_weight(self):
        self.size = os.path.getsize("content/blocs/" + self.hash + ".json")

    def save(self):
        with open("content/blocs/" + self.hash + ".json", 'w') as outfile:
            data = {
                'hash': self.hash,
                'size': self.size,
                'parent_hash': self.parent_hash,
                'last_transaction': self.last_transaction,
                'transactions': []
            }
            for i in range(len(self.transactions)):
                data['transactions'].append({
                    'emetteur': self.transactions[i]['emetteur'],
                    'recepteur': self.transactions[i]['recepteur'],
                    'montant': self.transactions[i]['montant'],
                    'name': self.transactions[i]['name']
                })

            json.dump(data, outfile)

    def load(self, hash):
        with open("content/blocs/" + hash + ".json") as json_file:
            data = json.load(json_file)
            self.hash = data['hash']
            self.parent_hash = data['parent_hash']
            self.size = data['size']
            self.last_transaction = data['last_transaction']
            self.transactions = data['transactions']

    def add_block(self):
        new_block = Block(parent_hash=self.hash)
        self.blocks.append(new_block)
        new_block.save()
        print("saved")

    def get_block(self, hash):
        b = Block()
        b.load(hash)
        if b.parent_hash == self.hash:
            self.blocks.append(b)
