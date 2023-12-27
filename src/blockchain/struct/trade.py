from dataclasses import dataclass

from blockchain.crypto import Crypto


@dataclass
class Trade:
    src: bytes
    dst: bytes
    value: int


@dataclass
class SignedTrade:
    trade: Trade
    signature: bytes  # TODO: amend the type?

    @classmethod
    def sign(cls, trade: Trade, crypto: Crypto) -> "SignedTrade":
        return SignedTrade(
            trade=trade,
            signature=crypto.sign(repr(trade).encode("UTF-8")),
        )
