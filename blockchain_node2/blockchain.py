from flask import Flask, jsonify, request
import hashlib
import datetime
import json
import requests
from urllib.parse import urlparse

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()

            if hash_operation[:4] == '0000':
                return new_proof

            new_proof += 1

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # ✅ MOVED INSIDE CLASS
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    # ✅ MOVED INSIDE CLASS
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # ✅ MOVED INSIDE CLASS
    def get_balance(self, wallet_address):
        balance = 0

        for block in self.chain:
            for tx in block['transactions']:
                if tx['receiver'] == wallet_address:
                    balance += tx['amount']
                if tx['sender'] == wallet_address:
                    balance -= tx['amount']

        return balance

    # ✅ GIVE THIS A BODY
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']

            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()
            ).hexdigest()

            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True


# 🔹 Flask app setup
app = Flask(__name__)

blockchain = Blockchain()

# 🔹 Mine block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    return jsonify(block), 200


# 🔹 Add transaction
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json_data = request.get_json()

    required = ['sender', 'receiver', 'amount']
    if not all(k in json_data for k in required):
        return 'Missing values', 400

    index = blockchain.add_transaction(
        json_data['sender'],
        json_data['receiver'],
        json_data['amount']
    )

    return jsonify({'message': f'Transaction will be added to block {index}'}), 201


# 🔹 Get full chain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200


# 🔹 Get wallet balance
@app.route('/get_balance/<wallet>', methods=['GET'])
def get_balance(wallet):
    balance = blockchain.get_balance(wallet)
    return jsonify({'wallet': wallet, 'balance': balance}), 200


# 🔹 Run node
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
