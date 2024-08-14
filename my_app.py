from flask import Flask
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)