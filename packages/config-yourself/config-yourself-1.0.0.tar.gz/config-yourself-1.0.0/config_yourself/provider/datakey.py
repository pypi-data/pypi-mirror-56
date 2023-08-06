# Copyright 2018 Blink Health LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

from .base import CryptoService
from builtins import bytes
from config_yourself.exceptions import BlinkConfigException
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

NONCE_BYTE_SIZE = 32
SALT_SIZE = 12


class DataKeyService(CryptoService):
    """The DataKeyService implements a CryptoService that uses an in-file data key to decrypt secrets

    :param bytes key: this file's datakey
    """

    def __init__(self, key):
        self._cipher = AESGCM(key)

    def decrypt(self, ciphertext):
        nonce, data = ciphertext[0:NONCE_BYTE_SIZE], ciphertext[NONCE_BYTE_SIZE:]
        try:
            return self._cipher.decrypt(nonce, data, b"")
        except InvalidTag:
            raise DataKeyDecryptError("Could not decrypt")


def decrypt_key_with_password(key, password):
    """Turns a key and password into a scrypt key

    :param bytes key: The key bytes, containing the salt and encrypted key
    :param str password: The password in plaintext to derive the key from

    :returns: The decrypted key contained in ``key``
    :rtype: bytes
    """
    # get the salt and encrypted key
    salt, encryptedKey = key[0:SALT_SIZE], key[SALT_SIZE:]
    # re-create the file's key with the provided password and salt
    derivedKey = Scrypt(
        salt,
        backend=default_backend(),
        # key length for AES
        length=32,
        # The cost parameter
        n=32 * 1024,
        # same values as go-config-yourself
        r=8,
        p=1,
    ).derive(bytes(password, "utf-8"))
    # Return the decrypted key using the derived key
    return DataKeyService(derivedKey).decrypt(encryptedKey)


class DataKeyDecryptError(BlinkConfigException):
    pass
