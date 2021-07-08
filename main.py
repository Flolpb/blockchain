
from classes.Block import Block
from classes.Wallet import Wallet

if __name__ == '__main__':
    block = Block()
    block.load("00")
    block.get_weight()
    block.save()

