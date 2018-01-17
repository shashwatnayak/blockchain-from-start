import hashlib as hash_algo
import json
from time import time
from uuid import uuid4
#IMPORT FLASK TO SETUP LOCAL HTTP SERVER
from textwrap import indent
from flask import Flask,jsonify, request

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


        def proof_of_work(self, last_proof):

        #Simple Proof of Work Algorithm:



            proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        # hashes the blocks
        block_link = json.dumps(block, sort_keys=True).encode()
        return hash_algo.sha256(block_link).hexdigest()


    @property
    def last_block(self):

        return self.chain[-1]

# Flask
# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # proof of work to get next proof_of_work
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    # sending reward for finding Proof
    #Sender is 0 to signify that it has mined new coin.
    #amount = 1 means the transaction is valid and node is verified

    blockchain.new_transaction(sender="0",recipient=node_identifier,amount= 1)

    #Connect the Newblock to hash chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_transaction(proof,previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    # Check that the required fields are in posted data
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing Values',400
    #New transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response),201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
