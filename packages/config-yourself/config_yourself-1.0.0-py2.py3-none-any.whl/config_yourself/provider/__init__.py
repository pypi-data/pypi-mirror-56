# Copyright 2018 Blink Health LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

from importlib import import_module
import warnings
from future.utils import raise_from


def Load(crypto, secrets=None):
    """Load a crypto provider, initializing it with secrets

    :param dict[str,Union[str,List]] crypto: The Config's `crypto` node
    :param dict[str,str] secrets: The runtime provided secrets

    :return: An initialized CryptoService
    :rtype: config_yourself.provider.CryptoService
    """
    providerName = crypto.get("provider", None)
    if not providerName:
        msg = "crypto.provider undefined in config file, defaulting to `kms`"
        warnings.warn(msg, DeprecationWarning)
        providerName = "kms"

    module_path = "config_yourself.provider.{}".format(providerName)
    module = import_module(module_path)

    try:
        provider = getattr(module, "Service")
    except AttributeError as err:  # pragma: no cover
        msg = 'Provider "%s" does not define a Service class' % (module_path)
        raise_from(ImportError(msg), err)

    return provider(crypto, secrets)
