# Copyright 2018 Blink Health LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

from pgpy import PGPKey, PGPMessage
from pgpy.errors import PGPDecryptionError
import warnings

from config_yourself.provider.datakey import DataKeyService
from config_yourself.exceptions import InvalidConfig, BlinkConfigException


class Service(DataKeyService):
    """A GPG CryptoService

    Provide the ``privateKey`` secret to :py:class:`~config_yourself.Config` when loading to initialize this provider. It should contain the bytes of a GPG private key. Provide the ``privateKeyPassword`` if the key is password protected.
    """

    def __init__(self, config, secrets):
        try:
            dataKeyBytes = config.get("key", None)
        except AttributeError as e:
            raise InvalidConfig(original=e)

        if not dataKeyBytes or dataKeyBytes == "":
            msg = (
                "crypto.key is not a string, "
                "Remove the crypto property if encryption is not needed"
            )
            raise InvalidConfig(message=msg)

        privateKey = secrets.get("privateKey", None)
        if not privateKey or privateKey == "":
            msg = (
                "No gpg private key provided for decryption. "
                "Remove the crypto property if encryption is not needed"
            )
            raise InvalidConfig(message=msg)

        gpgKey = PGPKey()
        gpgKey.parse(privateKey)

        password = secrets.get("privateKeyPassword", None)
        if password:
            try:
                gpgKey.unlock(password)
            except PGPDecryptionError as err:
                raise BadGPGKeyPasswordError(gpgKey.userids[0])

        with warnings.catch_warnings():
            # prevents warning of type `UserWarning: Message was encrypted with this key's subkey: ...`
            warnings.simplefilter("ignore", category=UserWarning)
            dataKey = gpgKey.decrypt(PGPMessage.from_blob(dataKeyBytes)).message

        DataKeyService.__init__(self, dataKey)


class BadGPGKeyPasswordError(BlinkConfigException):
    def __init__(self, key):

        msg = "Invalid password for key <{}>".format(key)

        self.message = msg
        super(BadGPGKeyPasswordError, self).__init__(msg)
