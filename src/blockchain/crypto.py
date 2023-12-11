from dataclasses import dataclass

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey, _RSAPublicKey
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils
from cryptography.hazmat.primitives import hashes


@dataclass
class Crypto:
    public: _RSAPublicKey
    private: _RSAPrivateKey

    def sign(self, msg: bytes) -> bytes:
        return self.private.sign(
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            utils.Prehashed(hashes.SHA256()),
        )

    def verify(self, msg: bytes, signature: bytes) -> bool:
        try:
            self.public.verify(
                signature,
                msg,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                utils.Prehashed(hashes.SHA256()),
            )
            return True
        except InvalidSignature:
            return False

    @classmethod
    def gen(cls) -> "Crypto":
        private = rsa.generate_private(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        public = private.public()
        return Crypto(public=public, private=private)
