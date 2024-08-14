import time
from hashlib import sha256
import json


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        return sha256(json.dumps(self.__dict__).encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []  # Khi xuất hiện transaction mới chưa được confirm
        self.create_genesis_block()

        self.difficulty = 3

    def create_genesis_block(self):
        genesis_block = Block(0,  [], time.time(), '0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if block.previous_hash != previous_hash:  # add in the last of blockchain
            return False

        self.chain.append(block)
        # return self.last_block().index + 1
        return self.last_block.index + 1

    def new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    # Định nghĩa phương thức để đào new_transaction
    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        new_block = Block(index=self.last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=self.last_block.hash)

        PoW = self.proof_of_work(new_block)
        self.add_block(new_block, PoW)
        return PoW

    def proof_of_work(self, block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return 'Nonce: {} - Hash: {}'.format(block.nonce, computed_hash)

    # Mỗi lần gọi phương thức cần dấu ngoặc, @property sẽ giúp gọi ko cần dấu ngoặc
    @property
    def last_block(self):
        return self.chain[-1]