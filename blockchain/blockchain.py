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
    
app.run(host='0.0.0.0', port=5000)

