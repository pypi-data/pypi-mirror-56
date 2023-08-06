# coding=utf-8
from __future__ import print_function

import pytest
from moto import mock_kms
from config_yourself.provider.kms import Service
from tests.conftest import KEYS
from tests.conftest import encrypt_test_value
from base64 import b64decode


@mock_kms
class TestKMS:
    @pytest.mark.parametrize(
        "config,region,errors",
        [
            ({}, None, True),
            ("nope", None, True),
            ({"key": "badkey"}, None, True),
            ({"key": 1}, None, True),
            ({"key": "bad-arn:key/000"}, None, True),
            ({"key": KEYS["kms"]}, "mx-central-1", False),
            ({"key": "key/000", "region": "mx-central-1"}, "mx-central-1", False),
        ],
    )
    def test_constuctor(self, config, region, errors):
        if errors:
            with pytest.raises(Exception):
                Service(config, {})
        else:
            s = Service(config, {})
            assert callable(s.decrypt)
            assert region == "mx-central-1"

    def test_decrypt(self):
        encrypted = encrypt_test_value("secret")
        s = Service({"key": KEYS["kms"]}, None)
        plainText = s.decrypt(b64decode(encrypted["ciphertext"]))
        assert plainText == b"secret"
