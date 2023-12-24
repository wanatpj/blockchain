from abc import ABC, abstractmethod
from dataclasses import dataclass

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils
from cryptography.hazmat.primitives import hashes


class Crypto(ABC):

    @abstractmethod
    def sign(self, msg: bytes) -> bytes:
        ...

    @abstractmethod
    def verify(self, msg: bytes, signature: bytes) -> bool:
        ...


class RSACrypto(Crypto):

    _ALGORITHM = hashes.SHA256()
    _PADDING = padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    )

    def __init__(self, public: RSAPublicKey, private: RSAPrivateKey) -> None:
        self.public = public
        self.private = private

    def sign(self, msg: bytes) -> bytes:
        return self.private.sign(
            msg,
            self._PADDING,
            self._ALGORITHM,
        )

    def verify(self, msg: bytes, signature: bytes) -> bool:
        try:
            self.public.verify(
                signature,
                msg,
                self._PADDING,
                self._ALGORITHM,
            )
            return True
        except InvalidSignature:
            return False

    @classmethod
    def gen(cls) -> "RSACrypto":
        private = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )
        public = private.public_key()
        return RSACrypto(public=public, private=private)
