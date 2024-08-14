from blockchain_operators import Block, Blockchain
import time

data2 = {
    'title': 'Hoc Python2',
    'author': 'Doan tan hoang',
    'timestamp': time.time()
}
#
# block = Block(1, data, time.time(), '0')
# block2 = Block(1, data, time.time(), '0')
# print(block.compute_hash())
# print(block2.compute_hash())

# #
# # print(block.__dict__)  # print(vars(block))
#
blockchain = Blockchain()
blockchain.new_transaction(data2)
print(blockchain.mine())

print(blockchain.chain[-1].__dict__)



dict = blockchain.__dict__
print(dict['chain'][0].__dict__)