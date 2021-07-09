import hashlib
import json
import os


class Block:
    def __init__(self, parent_hash=None, hash=None, base_hash=None):
        self.size = 0
        self.base_hash = base_hash
        self.hash = hash
        self.parent_hash = parent_hash
        self.blocks = []
        self.transactions = []
        self.last_transaction = None

    def check_hash(self):
        return self.hash == hashlib.sha256(self.base_hash.encode()).hexdigest()

    def add_transaction(self, w1, w2, montant, name):
        w1.sub_balance(montant)
        w2.add_balance(montant)
        new_transactions = {
            'emetteur': w1.unique_id,
            'recepteur': w2.unique_id,
            'montant': montant,
            'name': name
        }
        self.last_transaction = new_transactions
        self.transactions.append(new_transactions)
        self.save()
        self.get_weight()
        self.save()

    def get_transaction(self, name):
        for i in range(len(self.transactions)):
            x = self.transactions[i]['name'].find(str(name))
            if x != -1:
                return self
        return None

    def get_weight(self):
        self.size = os.path.getsize("content/blocs/" + self.hash + ".json")

    def save(self):
        with open("content/blocs/" + self.hash + ".json", 'w') as outfile:
            data = {
                'hash': self.hash,
                'base_hash': self.base_hash,
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
            self.base_hash = data['base_hash']
            self.parent_hash = data['parent_hash']
            self.size = data['size']
            self.last_transaction = data['last_transaction']
            self.transactions = data['transactions']

    def info(self):
        print("------------------------------------")
        print("hash: " + self.hash)
        print("base_hash: " + str(self.base_hash))
        print("parent_hash: " + self.parent_hash)
        print("size: " + str(self.size))
        print("last_transaction: " + str(self.last_transaction))
        print("transactions: " + str(self.transactions))
        print("------------------------------------")
