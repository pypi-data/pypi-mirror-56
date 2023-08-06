# Copyright 2018 Blink Health LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass


class CryptoService(with_metaclass(ABCMeta, object)):
    """The CryptoService abstract class must be implemented by providers
    """

    @abstractmethod
    def decrypt(self, ciphertext):  # pragma: no cover
        """The decrypt method takes a ciphertext string and returns the plaintext contents of it"""
        pass
