# Copyright 2018 Blink Health LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

from base64 import b64decode
from os import environ, path

import json

try:  # pragma: no cover
    # YAY PYTHON!
    # noinspection PyPackageRequirements
    from collections.abc import Mapping, Hashable
except ImportError:  # pragma: no cover
    try:
        # noinspection PyPackageRequirements
        from collections import Mapping, Hashable
    except ImportError:
        # noinspection PyPackageRequirements
        from future.moves.collections import Mapping, Hashable
from functools import reduce

from six import iteritems

import config_yourself.exceptions as exceptions
import config_yourself.provider as provider
import config_yourself.load as load
from config_yourself.util import merge_dicts


class Config(Mapping, Hashable):
    """A Config object

    The configs supplied are merged sequentially, the resulting ``dict`` is decrypted recursively and
    frozen. ``Config`` objects are proxies for that resulting ``dict``, and behave just like it

    :param dict[str,Any] default_config: A dictionary with default values
    :param List[dict[str,Any]] configs: Any number of overrides to apply over `default_config`
    :param str password: The password string when `crypto.provider` is password
    :param str privateKey: The armored contents of the private GPG key when `crypto.provider` is gpg

    :return: A decrypted config file as a frozen dictionary
    """

    def __init__(self, default_config, *configs, **secrets):
        self._hash = None
        self._provider = None

        cfg = self._merge_configs(default_config, configs)
        crypto = cfg.get("crypto", None)
        if not crypto:
            # no crypto means no secrets
            self._data = cfg
            return

        self._provider = provider.Load(crypto, secrets)
        self._data = self._decrypt(cfg)

    def _merge_configs(self, default_config, overrides):
        if len(overrides) > 0:
            # copy the first element to prevent modifying it. Deepcopy is way slower for large dicts
            # such as backend configs, and both `copy` and `OrderedDict` keep nested references
            # this hack is fast, but a hack nonetheless
            copies = tuple((json.loads(json.dumps(default_config)),) + overrides)
            return reduce(merge_dicts, copies)
        else:
            # when we're not using overrides, we don't care about copying, since the decryption
            # process copies on iteration
            return default_config

    def _decrypt(self, node, parents=[]):
        if isinstance(node, Mapping):
            if "encrypted" in node:
                try:
                    cipherBytes = b64decode(node["ciphertext"])
                    return self._provider.decrypt(cipherBytes).decode("utf-8")
                except Exception as e:
                    raise exceptions.DecryptError(parents, e)

            decrypted_dict = dict()
            for key, inner_value in iteritems(node):
                full_path = parents + [key]
                decrypted_dict[key] = self._decrypt(inner_value, parents=full_path)
            return decrypted_dict

        elif isinstance(node, list):
            decrypted_list = []
            for index, subNode in enumerate(node):
                full_path = parents + [str(index)]
                decrypted_list.append(self._decrypt(subNode, parents=full_path))
            return decrypted_list

        else:
            return node

    # basically make this class into a frozen dict
    # taken from http://stackoverflow.com/a/2704866

    def __iter__(self):  # pragma: no cover
        return iter(self._data)

    def __len__(self):
        """Get the size of this dict"""
        return len(self._data)

    def __getitem__(self, key):
        """Get the value for a top level config item"""
        return self._data[key]

    def __hash__(self):  # pragma: no cover
        if self._hash is None:
            self._hash = 0
            # noinspection PyTypeChecker
            for pair in iteritems(self):
                self._hash ^= hash(pair)
        return self._hash


def AppConfig(config_file=None, before=None, after=None, config_folder="./config"):
    """Load a sequence of resolved config file names

    When using config_yourself in Flask or Django, this helper will load:

    * the ``"{config_folder}/defaults.yml"`` file,
    * a file located at ``os.environ.get("CONFIG_FILE", path.join(config_folder, "local.yml"))``
    * a ``"{config_folder}/personal.yml"`` file, if it exists


    All parameters are optional, and allow tweaking of the locations and extensions used for config files.

    :param Optional[str] config_file: the path to the main config file to load, usually. (default: ``os.environ.get("CONFIG_FILE", "./config/local.yml")``)
    :param Optional[list[str]] before: File names to load before ``config_file`` (default: `['default']`)
    :param Optional[list[str]] after: File names to apply after ``config_file`` if they exist (default: `['personal']`)
    :param Optional[str] config_folder: Base folder path to look for files in, (default: `./config`)

    :returns: A Config object
    :rtype: :py:class:`~config_yourself.Config`
    """
    if config_file is None:
        config_file = environ.get("CONFIG_FILE", path.join(config_folder, "local.yml"))

    if before is None:
        before = ["defaults"]

    if after is None:
        after = ["personal"]

    # the chain of files to merge before decrypting
    chain = []
    # extract some details about the main file
    config_file = path.abspath(config_file)
    if config_folder is None:
        config_folder = path.dirname(config_file)
    _main_ext = path.splitext(config_file)[1]
    name_to_path = lambda name: path.join(
        config_folder, "{}.{}".format(name, _main_ext)
    )

    # Add the resolved before files
    chain = [name_to_path(file_name) for file_name in before]
    # Add the main config file
    chain.append(config_file)

    # Add after files if they exist
    for f in [name_to_path(file_name) for file_name in after]:
        if path.exists(f):
            chain.append(f)

    return Config(*[load.file(file_path) for file_path in chain])
