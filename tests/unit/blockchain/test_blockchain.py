from dataclasses import dataclass

import pytest

from blockchain.blockchain import Block, Blockchain, SummaryBlockchain
from blockchain.consensus.core import SimpleConsnsus
from blockchain.crypto import Crypto, RSACrypto
from blockchain.policy.sign import IncorrectSignatureError, SingleSignPolicy
from blockchain.struct.allocation import Allocation
from blockchain.struct.trade import SignedTrade, Trade


CONFIG_DIR = "config/sample"
sample_hash = lambda x: f"{hash(x)}"


# @pytest.fixture(scope="module", params=os.listdir(CONFIG_DIR))
# def config(request):
#     with os.open(f"{CONFIG_DIR}/{request.params}") as raw_config:
#         return yaml.safe_load(raw_config)


# def test_blockchain_config(config):
#     Blockchain.from_config(config)


def test_string_blockchain():
    blockchain = Blockchain[str](consensus=SimpleConsnsus(hash_fn=sample_hash))
    blockchain.add_block("Block 1")
    blockchain.add_block("Block 2")

    assert [
        "Block 1",
        "Block 2",
    ] == blockchain.raw_chain()

    assert [
        Block(
            "Block 1",
            hash=sample_hash("#Block 1"),
            previous_hash="",
        ),
        Block(
            "Block 2",
            hash=sample_hash(f"{sample_hash('#Block 1')}#Block 2"),
            previous_hash=sample_hash("#Block 1"),
        ),
    ] == blockchain.chain()


def test_trade_blockchain():
    @dataclass
    class _Trade:
        src: int
        dest: int
        value: int

    blockchain = Blockchain[_Trade](consensus=SimpleConsnsus(hash_fn=sample_hash))
    blockchain.add_block(_Trade(src=2, dest=4, value=3))
    blockchain.add_block(_Trade(src=4, dest=1, value=7))

    assert [
        _Trade(src=2, dest=4, value=3),
        _Trade(src=4, dest=1, value=7),
    ] == blockchain.raw_chain()


def test_trade_blockchain():
    blockchain = SummaryBlockchain[Allocation, Trade](
        consensus=SimpleConsnsus(hash_fn=sample_hash),
        summary_factory=Allocation,
    )
    blockchain.add_block(Trade(src=2, dst=4, value=3))
    blockchain.add_block(Trade(src=4, dst=1, value=7))

    assert {
        2: -3,
        4: -4,
        1: 7,
    } == blockchain.summary().as_dict()


def test_trade_blockchain_with_single_sign_policy():
    crypto: Crypto = RSACrypto.gen()
    policy = SingleSignPolicy(crypto=crypto)
    blockchain = Blockchain[SignedTrade](
        consensus=SimpleConsnsus(hash_fn=sample_hash),
        policy=policy,
    )

    blockchain.add_block(SignedTrade.sign(
        trade=Trade(src=2, dst=4, value=3),
        crypto=crypto
    ))

    with pytest.raises(IncorrectSignatureError):
        blockchain.add_block(SignedTrade(
            trade=Trade(src=2, dst=4, value=3),
            signature=b"",
        ))
