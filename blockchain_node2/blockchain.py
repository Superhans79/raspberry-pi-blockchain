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

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
def get_balance(self, wallet_address):
    balance = 0

    for block in self.chain:
        for tx in block['transactions']:
            if tx['receiver'] == wallet_address:
                balance += tx['amount']
            if tx['sender'] == wallet_address:
                balance -= tx['amount']

    return balance


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

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f'http://{node}/get_chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False
    




# Flask app
app = Flask(__name__)

blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    previous_hash = blockchain.hash(previous_block)

    blockchain.add_transaction(
        sender="Network",
        receiver="Miner",
        amount=1
    )

    block = blockchain.create_block(proof, previous_hash)

    return jsonify({
        'message': 'Block mined!',
        'block': block
    }), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()

    required = ['sender', 'receiver', 'amount']
    if not all(k in data for k in required):
        return 'Missing values', 400

    index = blockchain.add_transaction(
        data['sender'],
        data['receiver'],
        data['amount']
    )

    return jsonify({
        'message': f'Transaction will be added to block {index}'
    }), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    data = request.get_json()
    nodes = data.get('nodes')

    if nodes is None:
        return "No node", 400

    for node in nodes:
        blockchain.add_node(node)

    return jsonify({
        'message': 'Nodes connected',
        'total_nodes': list(blockchain.nodes)
    }), 201


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    replaced = blockchain.replace_chain()

    if replaced:
        return jsonify({
            'message': 'Chain was replaced',
            'new_chain': blockchain.chain
        }), 200
    else:
        return jsonify({
            'message': 'Chain is already the longest',
            'chain': blockchain.chain
        }), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    valid = blockchain.is_chain_valid(blockchain.chain)

    return jsonify({
        'valid': valid
    }), 200

@app.route('/create_wallet', methods=['GET'])
def create_wallet():
    private_key = str(datetime.datetime.now())
    wallet_address = hashlib.sha256(private_key.encode()).hexdigest()

    return jsonify({
        'wallet_address': wallet_address
    }), 200
    
    @app.route('/get_balance/<wallet>', methods=['GET'])
def get_balance(wallet):
    balance = blockchain.get_balance(wallet)

    return jsonify({
        'wallet': wallet,
        'balance': balance
    }), 200


app.run(host='0.0.0.0', port=5001)
