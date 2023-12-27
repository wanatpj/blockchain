from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils
from cryptography.hazmat.primitives import hashes, serialization


class MissingPrivateKeyException(Exception):
    pass


class Crypto(ABC):
    @abstractmethod
    def private_id(self) -> bytes:
        ...

    @abstractmethod
    def public_id(self) -> bytes:
        ...

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

    def __init__(
        self,
        public: RSAPublicKey,
        private: Optional[RSAPrivateKey] = None,
    ) -> None:
        self._public = public
        self._private = private

    def private_id(self) -> bytes:
        if self._private is None:
            raise MissingPrivateKeyException()
        return self._private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

    def public_id(self) -> bytes:
        return self._public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def sign(self, msg: bytes) -> bytes:
        if self._private is None:
            raise MissingPrivateKeyException()
        return self._private.sign(
            msg,
            self._PADDING,
            self._ALGORITHM,
        )

    def verify(self, msg: bytes, signature: bytes) -> bool:
        try:
            self._public.verify(
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
