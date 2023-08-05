"""Simple encryption/decryption mechanism which uses cryptography.fernet."""
import os
import pickle
import warnings
from cryptography.fernet import Fernet


CRYPTO_KEY = os.getenvb(b"CRYPTO_KEY", b"")

if len(CRYPTO_KEY) < 44:
    warnings.warn("length of key must be at least 44 chars")

__all__ = ["Cypher"]


class Cypher:
    """A class for encryption/decryption of data."""

    def __init__(self, key=CRYPTO_KEY, pickle_protocol=3):
        """Initialize the class.

        :param bytes key: key (password) which will be used
        for encryption/decryption

        :param int pickle_protocol: pickle protocol version (default: 3)

        """
        self.pickle_protocol = pickle_protocol
        self.fernet = Fernet(key)

    def encrypt(self, data):
        """Encrypt data.

        :param data: any pickled data type
        :returns: encrypted data

        """
        return self.fernet.encrypt(
            pickle.dumps(data, protocol=self.pickle_protocol)
        )

    def decrypt(self, data):
        """Decrypt data.

        :param data: any pickled data type
        :returns: original decrypted data

        """
        return pickle.loads(self.fernet.decrypt(data))
