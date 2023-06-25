from blockchain.blockchain import Blockchain


def test_blockchain():
    blockchain = Blockchain()

    blockchain.add_block("Block 1")
    blockchain.add_block("Block 2")
    blockchain.add_block("Block 3")

    assert [] == blockchain.chain()
