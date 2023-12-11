import hashlib
from abc import abstractmethod
from typing import Callable


class Consensus:
    @abstractmethod
    def build(self, msg: str) -> str:
        ...

    # @abstractmethod
    # def validate():
    #     ...

    # @staticmethod
    # @abstractmethod
    # def from_config():
    #     ...


class SimpleConsnsus(Consensus):
    def __init__(self, hash_fn: Callable[[str], str]):
        self.hash_fn = hash_fn

    def build(self, msg: str) -> str:
        return self.hash_fn(msg)


class Sha256HexDigestConsensus(SimpleConsnsus):
    def __init__(self):
        super().__init__(lambda msg: hashlib.sha256(msg.encode()).hexdigest())
