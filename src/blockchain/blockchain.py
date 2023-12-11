from dataclasses import dataclass
from typing import Callable, Dict, Generic, Optional, Sequence, TypeVar, Type

from blockchain.consensus import Consensus
from blockchain.crypto import Crypto
from blockchain.policy import Policy


BLOCK_TYPE = TypeVar("BLOCK_TYPE")
SUMMARY_TYPE = TypeVar("SUMMARY_TYPE")

NULL_HASH = ""


class Block(Generic[BLOCK_TYPE]):
    @dataclass
    class Builder:
        consensus: Consensus

        def build(self, data: BLOCK_TYPE, previous_hash: str) -> "Block[BLOCK_TYPE]":
            return Block[BLOCK_TYPE](
                data=data,
                previous_hash=previous_hash,
                hash=self.consensus.build(f"{previous_hash}#{data}"),
            )

    def __init__(self, data: BLOCK_TYPE, previous_hash: str, hash: str):
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False

        return self.hash == other.hash

    def __repr__(self):
        return f"Block(data={self.data}, previous_hash={self.previous_hash}, hash={self.hash})"


class Blockchain(Generic[BLOCK_TYPE]):
    def __init__(self, consensus: Consensus):
        self.consensus = consensus
        self.block_builder = Block[BLOCK_TYPE].Builder(consensus=consensus)
        self.branch_blockhash: Dict[str, str] = {}
        self.block: Dict[str, Block[BLOCK_TYPE]] = {}

    def add_block(self, block: BLOCK_TYPE, branch: str = "local") -> None:
        current_block = self.current_block(branch)
        previous_hash = current_block.hash if current_block else NULL_HASH
        block = self.block_builder.build(data=block, previous_hash=previous_hash)
        self.branch_blockhash[branch] = block.hash
        self.block[block.hash] = block

    def chain(self, branch: str = "local") -> Sequence[Block[BLOCK_TYPE]]:
        current_block = self.current_block(branch)
        reversed_results = []
        while current_block:
            reversed_results.append(current_block)
            current_block = self.block.get(current_block.previous_hash)
        return list(reversed(reversed_results))

    def raw_chain(self, branch: str = "local") -> Sequence[Block[BLOCK_TYPE]]:
        return list(map(lambda x: x.data, self.chain(branch)))

    def current_block(self, branch: str = "local") -> Optional[Block[BLOCK_TYPE]]:
        return self.block.get(self.branch_blockhash.get(branch))


class SummaryBlockchain(Generic[SUMMARY_TYPE, BLOCK_TYPE], Blockchain[BLOCK_TYPE]):
    def __init__(self, consensus: Consensus, summary_factory: Type[Callable[[Policy], SUMMARY_TYPE]], summary_policy: Optional[Policy] = None):
        super().__init__(consensus)
        self._summary: SUMMARY_TYPE = summary_factory(summary_policy)

    def add_block(self, block: BLOCK_TYPE, branch: str = "local") -> None:
        with self._summary:
            self._summary.reduce(block)
            super().add_block(block, branch=branch)

    def summary(self):
        return self._summary
