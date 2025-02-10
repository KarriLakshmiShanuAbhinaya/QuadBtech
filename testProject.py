import hashlib
import time

# Block structure
class Block:
    def __init__(self, index, previous_hash, transactions, proof, timestamp=None):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof  # Proof-of-Work value (optional)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.proof}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create the first block in the blockchain (Genesis block)
        genesis_block = Block(0, "0", ["Genesis Block"], 100)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        last_block = self.get_last_block()
        index = len(self.chain)
        previous_hash = last_block.hash
        proof = self.proof_of_work(last_block.proof)  # Simple Proof-of-Work
        new_block = Block(index, previous_hash, transactions, proof)
        self.chain.append(new_block)

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # Condition for valid proof (proof must start with four leading zeros)
        return guess_hash[:4] == "0000"

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if current block's previous hash matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def tamper_with_chain(self, index, new_transactions):
        # Tamper with a block by changing its transactions
        if index < len(self.chain):
            self.chain[index].transactions = new_transactions
            self.chain[index].hash = self.chain[index].calculate_hash()

    def print_chain(self):
        for block in self.chain:
            print(f"Block {block.index} [Timestamp: {block.timestamp}]")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Transactions: {block.transactions}")
            print(f"Proof: {block.proof}")
            print(f"Hash: {block.hash}")
            print("-" * 50)


# Example usage
if __name__ == "__main__":
    # Create blockchain and add blocks
    blockchain = Blockchain()
    blockchain.add_block(["Alice pays Bob 5 BTC", "Bob pays Charlie 3 BTC"])
    blockchain.add_block(["Charlie pays Dave 2 BTC", "Dave pays Eve 1 BTC"])

    print("Blockchain before tampering:")
    blockchain.print_chain()

    # Validate the chain before tampering
    print("Is blockchain valid?", blockchain.is_chain_valid())

    # Tamper with the second block
    blockchain.tamper_with_chain(1, ["Alice pays Bob 50 BTC"])
    print("\nBlockchain after tampering with block 1:")
    blockchain.print_chain()

    # Validate the chain after tampering
    print("Is blockchain valid?", blockchain.is_chain_valid())
