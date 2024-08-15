import time
from hashlib import sha256
import json


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        return sha256(json.dumps(self.__dict__).encode()).hexdigest()


class Blockchain:
    difficulty = 5

    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []  # Khi xuất hiện transaction mới chưa được confirm
        # self.create_genesis_block()

        

    def create_genesis_block(self):
        genesis_block = Block(0,  [], 0, '0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if block.previous_hash != previous_hash:  # add in the last of blockchain
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        # return self.last_block().index + 1
        return self.last_block.index + 1


    @classmethod  #phương thức dùng riêng cho class blockchain, sử dụng cls thay vì self
    def is_valid_proof(cls, block, proof):
        return proof.startswith('0' * Blockchain.difficulty) and proof == block.compute_hash()

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
        
        result = self.add_block(new_block, PoW)
        self.unconfirmed_transactions = []
        return result

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        PoW = computed_hash
        return PoW


    # Mỗi lần gọi phương thức cần dấu ngoặc, @property sẽ giúp gọi ko cần dấu ngoặc
    @property
    def last_block(self):
        return self.chain[-1]