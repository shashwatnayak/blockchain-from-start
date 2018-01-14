import hashlib as hash_algo
import json
from time import time

class blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #Creating genesis blocks
        self.new_block(previous_hash =1,proof=100)

    def new_block(self,proof,previous_hash=None):
        #new block and add it to chain
        """ The proof of word algorithm """
        block = {
                'index':len(self.chain) +1,
                'timestamp':time(),
                'transactions':self.current_transactions,
                'previous_hash':previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = [] #reset the list of transactions
        self.chain.append(block)
        return block


    def new_transaction(self, sender, recipient, amount):

        """ Creates a new transaction to go into the next mined Block"""



        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1


    @staticmethod
    def hash(block):
        # hashes the blocks
        block_link = json.dumps(block, sort_keys=True).encode()
        return hash_algo.sha256(block_link).hexdigest()


    @property
    def last_block(self):

        return self.chain[-1]
