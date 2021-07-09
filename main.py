import os
import time
from classes.Block import Block
from classes.Chain import Chain
from classes.Wallet import Wallet


def test_wallet():
    print("You are testing the wallet class...")
    time.sleep(0.8)
    print("Creating a new wallet...")
    time.sleep(0.4)
    balance = input("How much money do you want on your wallet ?\n")
    try:
        balance = int(balance)
        new_wallet = Wallet(balance)
        new_wallet.info()
        save = input("Do you want to save your wallet ? (y/n)\n")
        if save == "y" or save == "Y":
            new_wallet.save()
    except ValueError:
        print("That's not an int!")
    loader = True
    while loader:
        load = input("do you want to load a wallet ? (y/n)")
        if load == "y" or load == "Y":
            wallet_to_load_id = input("Load a wallet with an id : ")
            load_wallet = Wallet(0)
            load_wallet.load(wallet_to_load_id)
            if load_wallet.unique_id == wallet_to_load_id:
                load_wallet.info()
                add_money = input("Add money to the wallet : ")
                try:
                    add_money = int(add_money)
                    load_wallet.add_balance(add_money)
                    load_wallet.info()
                except ValueError:
                    print("That's not an int!")
                sub_money = input("Remove money to the wallet : ")
                try:
                    sub_money = int(sub_money)
                    load_wallet.sub_balance(sub_money)
                    load_wallet.info()
                except ValueError:
                    print("That's not an int!")
        else:
            loader = False
    print("Finishing testing the Wallet Class..")


def test_chain():
    print("You are testing the blockchain...")
    print("Loading the parent block : ")
    bl = Block()
    bl.load("00")
    time.sleep(0.4)
    bl.info()
    time.sleep(0.8)
    print("Loading the Chain...")
    chain = Chain()
    chain.get_block("00")
    # Je reconstruis la chaine de blocs en checkant tous les
    # fichiers qu'il y a dans les blocs et en les organisant
    # dans l'ordre en checkant si leur parent à déjà été assigné
    # avant eux.
    files = os.listdir('content/blocs/')
    for i in range(len(files)):
        if files[i] != "00.json":
            filename = files[i].split('.')
            chain.get_block(filename[0])
    while len(chain.blocs) < len(files):
        for i in range(len(chain.blocsToAdd)):
            chain.get_block_to_add(chain.blocsToAdd[i])
    for i in range(len(chain.blocs)):
        chain.blocs[i].get_weight()
        chain.blocs[i].save()

    chains = "Chain contain: "
    for i in range(len(chain.blocs)):
        chains += chain.blocs[i].hash
        chains += " -> "
    print(chains)

    wantToAdd = True
    while wantToAdd:
        res = input("Do u want to add a bloc to the chain ? (y/n)")
        if res == "y" or res == "Y":
            chain.add_block()
            print("block added to the chain")
            chain.blocs[len(chain.blocs) - 1].info()
            chains += chain.blocs[len(chain.blocs) - 1].hash
            chains += " -> "
            time.sleep(0.5)
            print(chains)
        else:
            wantToAdd = False
    chain.number = chain.get_last_transactions_number()
    time.sleep(0.5)
    print("Getting the last transaction number...")
    time.sleep(0.3)
    print("Found : " + str(chain.get_last_transactions_number()))
    det = input("Do you want to get informations of "
                "the block related to this transaction ? (y/n)")
    if det == "y" or det == "Y":
        block_transaction = chain.find_transactions(chain.number)
        block_transaction.info()
    trans = True
    while trans:
        res = input("Do u want to add a transaction to a bloc ? (y/n)")
        if res == "y" or res == "Y":
            bloc_id = input("Load a bloc with an id : ")
            bloc = None
            for i in range(len(chain.blocs)):
                if bloc_id == chain.blocs[i].hash:
                    bloc = chain.blocs[i]
            if bloc is not None:
                w1 = input("Load the emitter with an id : ")
                w2 = input("Load the receiver with an id : ")
                montant = input("Money to transfer : ")
                try:
                    montant = int(montant)
                    chain.add_transaction(w1, w2, montant, bloc)
                except ValueError:
                    print("Thats not an int!")
            else:
                print("Could not find the block")
        else:
            trans = False

    print("My program is now finished ! Thank you !")


if __name__ == '__main__':
    test_wallet()
    test_chain()
