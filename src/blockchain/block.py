import hashlib
from typing import Generic, Optional, Self, TypeVar

from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

from blockchain.crypto import Crypto

T = TypeVar("T")


class Block(Generic[T]):
    def __init__(self, data: T, previous_hash: str, crypto: Optional[Crypto]):
        self.data = data
        self.hash = self._calculate_hash(previous_hash)
        self.signature = self._calculate_signature(crypto) if crypto else None

    def _calculate_hash(self, previous_hash: str):
        block_contents = repr(self.data) + previous_hash
        return hashlib.sha256(block_contents.encode()).hexdigest()

    def _calculate_signature(self, crypto: Crypto):
        return crypto.sign(self.hash)

    def verify_signature(self, crypto: Crypto) -> bool:
        if self.signature:
            return crypto.verify(msg=self.hash, signature=self.signature)
        return True
