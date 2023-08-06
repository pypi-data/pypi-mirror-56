# coding=utf-8
from __future__ import print_function
from base64 import b64decode
from tests.conftest import KEYS, SECRETS

import pytest
from config_yourself.provider.gpg import Service


class TestGPG:
    @pytest.mark.parametrize(
        "config,secrets,errors",
        [
            ({}, None, True),
            ("nope", None, True),
            ({"key": "badkey"}, None, True),
            ({"key": KEYS["gpg"]}, SECRETS["gpg"], False),
        ],
    )
    def test_constuctor(self, config, secrets, errors):
        if errors:
            with pytest.raises(Exception):
                Service(config, secrets)
        else:
            s = Service(config, secrets)
            assert callable(s.decrypt)

    def test_decrypt(self):
        encrypted = (
            "on//Ow0gJ3gRBzKO7Q0jq/75v6oIlUKZV3lJOuE3CYfEj/hHlYdX5O3WF10dseH1y8QIgi2n"
        )
        s = Service({"key": KEYS["gpg"]}, SECRETS["gpg"])
        plainText = s.decrypt(b64decode(encrypted))
        assert plainText == b"secret"
