# Copyright 2018 Blink Health LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

from config_yourself.exceptions import InvalidConfig, BlinkConfigException
from config_yourself.provider.datakey import (
    DataKeyService,
    DataKeyDecryptError,
    decrypt_key_with_password,
)
from base64 import b64decode
from binascii import Error


class Service(DataKeyService):
    """A Password CryptoService

    Provide the ``password`` secret to :py:class:`~config_yourself.Config` when loading to initialize this provider.
    """

    def __init__(self, config, secrets):
        try:
            key = config.get("key", None)
        except AttributeError as e:
            raise InvalidConfig(original=e)

        if not key or key == "":
            msg = (
                "crypto.key is empty, "
                "remove the crypto property if no encryption is needed"
            )
            raise InvalidConfig(message=msg)

        try:
            keyBytes = b64decode(key)
        except Error:
            raise InvalidConfig(message="Could not read file key as base64")

        password = secrets.get("password", None)
        if not password or password == "":
            msg = (
                "No password provided for decryption. "
                "Remove the crypto property if no encryption is needed"
            )
            raise InvalidConfig(message=msg)

        try:
            # decrypt the file's key with the supplied password
            dataKey = decrypt_key_with_password(keyBytes, password)
        except DataKeyDecryptError:
            raise PasswordDecryptError(key)
        DataKeyService.__init__(self, dataKey)


class PasswordDecryptError(BlinkConfigException):
    def __init__(self, key):

        msg = "Failed to decrypt with key <{}> and a supplied password".format(key)

        self.message = msg
        super(PasswordDecryptError, self).__init__(msg)
