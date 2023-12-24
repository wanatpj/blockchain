from typing import Generic
from blockchain.crypto import Crypto

from blockchain.policy.core import Policy, POLICY_SUBJECT
from blockchain.struct.trade import SignedTrade


DEFAULT_ENCODING = "UTF-8"


class IncorrectSignatureError(Exception):
    pass


class SingleSignPolicy(Policy[SignedTrade, None]):

    def __init__(self, crypto: Crypto) -> None:
        self._crypto = crypto

    def validate(self, subject: SignedTrade, hint: None = None) -> None:
        if not self._crypto.verify(
            msg=repr(subject.trade).encode(DEFAULT_ENCODING),
            signature=subject.signature,
        ):
            raise IncorrectSignatureError()  # No error messsage, not to reveal any data. Ok???
