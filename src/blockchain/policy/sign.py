from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from blockchain.crypto import Crypto, RSACrypto
from blockchain.policy.core import Policy
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


class SourceSignPolicy(Policy[SignedTrade, None]):
    def validate(self, subject: SignedTrade, hint: None = None) -> None:
        public_key: RSAPublicKey = serialization.load_pem_public_key(
            subject.trade.src, backend=default_backend()
        )
        crypto = RSACrypto(public=public_key)
        if not crypto.verify(
            msg=repr(subject.trade).encode(DEFAULT_ENCODING),
            signature=subject.signature,
        ):
            raise IncorrectSignatureError()  # No error messsage, not to reveal any data. Ok???
