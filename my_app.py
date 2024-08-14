import time
from flask import Flask,request
from blockchain_operators import Block, Blockchain


app = Flask(__name__)

blockchain = Blockchain()


@app.route('/', methods=['GET'])
def index():
    return 'Hello'

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for bl in blockchain.chain:
        chain_data.append(bl.__dict__)

    return chain_data

@app.route('/new_transaction', methods=['POST'])
def add_new_transaction():
    data = request.get_json()   # <=> data = {}
    required_fields = ['title', 'author']
    for field in required_fields:
        data[field] = data.get(field)

    data['timestamp'] = time.time()

    blockchain.new_transaction(data)
    return 'Success.', 201

@app.route('/mine', methods=['POST'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return 'No transaction to mine.'

    return 'Block #{} is mined.'.format(result) 



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)