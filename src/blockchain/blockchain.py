from dataclasses import dataclass
from typing import Generic, List

from cryptography.hazmat.primitives.asymmetric import rsa

from blockchain.block import Block
from blockchain.crypto import Crypto
from blockchain.policy import ChainPolicy

POLICY_TYPE = TypeVar("POLICY_TYPE")
BLOCK_TYPE = TypeVar("BLOCK_TYPE")
SUMMARY_TYPE = TypeVar("SUMMARY_TYPE")


class Blockchain(Generic[BLOCK_TYPE, SUMMARY_TYPE]):
    def __init__(self, config: dict):
        self.chain: List[Block[ChainPolicy | BLOCK_TYPE | SUMMARY_TYPE]] = []
        self.create_genesis_block(policy_config=config["policy"])
        self.crypto = Crypto(**config["id"])

    def create_genesis_block(self, policy_config):
        self.chain.append(
            Block[ChainPolicy](
                data=ChainPolicy.build(policy_config=policy_config),
                previous_hash=0,
                crypto=self.crypto,
            )
        )

    def add_block(self, data: BLOCK_TYPE):
        self.chain.append(
            Block[BLOCK_TYPE](
                data=data, previous_block=self.chain[-1], crypto=self.crypto
            )
        )

    @classmethod
    def build_new(cls):
        pass

    @classmethod
    def gen(cls) -> "Blockchain":
        pass
