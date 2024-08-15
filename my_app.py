import time
from flask import Flask,request
from blockchain_operators import Block, Blockchain

import requests
import json



app = Flask(__name__)

blockchain = Blockchain()
blockchain.create_genesis_block()

peers = set()

@app.route('/', methods=['GET'])
def index():
    return 'Hello'

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for bl in blockchain.chain:
        chain_data.append(bl.__dict__)

    return {
        "length": len(chain_data),
        "chain": chain_data,
        "peers": list(peers)
    }

@app.route('/new_transaction', methods=['POST'])
def add_new_transaction():
    data = request.get_json()   # <=> data = {}
    required_fields = ['title', 'author']
    for field in required_fields:
        data[field] = data.get(field)

    data['timestamp'] = time.time()

    blockchain.new_transaction(data)
    return 'Success.', 201

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return 'No transaction to mine.'

    return 'Block #{} is mined.'.format(result) 

@app.route('/register_new_node', methods=['POST'])
def register_new_node():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400
    
    peers.add(node_address)
    return get_chain()

@app.route('/register_node_with', methods=['POST'])
def register_node_with():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400


    data = {"node_address": request.host_url}
    headers = {"Content-Type": "application/json"}
    response = requests.post(node_address + '/register_new_node',
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers          #global to change global var ( peers, blockchain,..)

        chain_dump = response.json()["chain"]
        blockchain = create_chain_from_chaindump(chain_dump)
        peers.update(response.json()["peers"])
        return "Resistration successful.", 200
    else:
        return response.content, response.status_code


def create_chain_from_chaindump(chain_dump):
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()
    for idx, bl in enumerate(chain_dump):
        if idx == 0:
            continue
        block = Block(
            index=bl["index"],
            transactions=bl["transactions"],
            timestamp=bl["timestamp"],
            previous_hash=bl["previous_hash"],
            nonce=bl["nonce"]
        )
        proof = bl["hash"]
        added = generated_blockchain.add_block(block, proof)
        if not added:
            raise Exception("the chain dump is tampered !") 
        
    return generated_blockchain


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)