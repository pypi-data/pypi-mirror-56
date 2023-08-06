# coding=utf-8
from __future__ import print_function
from base64 import b64decode
from tests.conftest import KEYS, SECRETS

import pytest
from config_yourself.provider.password import Service
from tests.conftest import KEYS, SECRETS


class TestPassword:
    @pytest.mark.parametrize(
        "config,secrets,errors",
        [
            ({}, None, True),
            ("nope", None, True),
            ({"key": "badkey"}, None, True),
            ({"key": KEYS["password"]}, {"password": "badpassword"}, True),
            ({"key": KEYS["password"]}, {"no-password": ""}, True),
            ({"key": KEYS["password"]}, SECRETS["password"], False),
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
            "Ds84SJ3l3l0Xz2CSlo3Ap0MF3bNTFA/+IVZ8uLIk7YhEC/mVrV5je6LlaBst7Xj2ggWs9pN6"
        )
        s = Service({"key": KEYS["password"]}, SECRETS["password"])
        plainText = s.decrypt(b64decode(encrypted))
        assert plainText == b"secret"
