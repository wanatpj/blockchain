from blockchain.consensus.core import Consensus



from cryptography.hazmat.primitives.asymmetric import rsa

class SingleSignConsensus(Consensus):
    def build(self, hash: str) -> str:
        return crypto.sign(hash)

    def validate():
        return crypto.verify(msg=self.hash, signature=self.signature)
