# coding=utf-8
from __future__ import print_function

import pytest

# mock_kms just base64 encodes values
from moto import mock_kms
from copy import deepcopy
import warnings
from tests.conftest import add_kms_entries, get_config_yourself, KEYS, SECRETS
import config_yourself.exceptions as errors

# noinspection PyClassHasNoInit
@mock_kms
class TestBlinkConfig(object):
    @pytest.mark.parametrize(
        "input_config",
        [
            {"key": "value"},
            {"key": {"encrypted": True, "ciphertext": "Wlc1amNubHdkRzFs"}},
            {"key": {"nested": {"value": True}}},
            {"key": [{"nested": True}, {"nested": False}]},
        ],
    )
    def test_verify_returned_encrypted_config_can_not_modify_original(
        self, input_config
    ):
        input_config_with_kms = add_kms_entries(input_config)
        original = input_config_with_kms["key"]
        with warnings.catch_warnings(record=True):
            config_yourself = get_config_yourself(
                input_config_with_kms, {"key": "overriden"}
            )
        with pytest.raises(TypeError):
            config_yourself["foo"] = "bar"

        assert input_config_with_kms["key"] == original
        assert config_yourself["key"] == "overriden"

    @pytest.mark.parametrize(
        "source,override",
        [
            (
                {"value": True, "key": {"nested": {"value": True, "unchanged": True}}},
                {"value": False, "key": {"nested": {"value": False}}},
            )
        ],
    )
    def test_verify_overrides_are_not_destructive(self, source, override):
        original_source = deepcopy(source)
        with warnings.catch_warnings(record=True):
            resulting_config = get_config_yourself(source, override)

        # the original object was not modified
        assert source == original_source
        # the resulting config has been overridden
        assert not resulting_config["key"]["nested"]["value"]
        # make sure the nested value that is defined in source and not defined in the override is present
        assert "unchanged" in resulting_config["key"]["nested"]
        assert resulting_config["key"]["nested"]["unchanged"]

    def test_overrides_warn_on_potential_errors(self):
        with warnings.catch_warnings(record=True) as warns:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            crypto = {"key": "<key>"}
            source = {
                "crypto": crypto,
                "key": {"encrypted": True, "ciphertext": "Wlc1amNubHdkRzFs"},
            }
            override = {
                "crypto": crypto,
                "key": {"encrypted": True, "ciphertext": "Y3JhcCEK"},
                "ignored": True,
            }

            with pytest.raises(errors.InvalidConfig):
                cfg = get_config_yourself(source, override)

            all_warnings = "\n".join([str(w.message) for w in warns])
            assert "<key>" in all_warnings
            assert "<ignored>" in all_warnings
            assert "defaulting to `kms`" in all_warnings

    def test_decrypts(self):
        secret = {
            "ciphertext": "Ds84SJ3l3l0Xz2CSlo3Ap0MF3bNTFA/+IVZ8uLIk7YhEC/mVrV5je6LlaBst7Xj2ggWs9pN6",
            "encrypted": "true",
        }
        cfg = get_config_yourself(
            {
                "crypto": {
                    "provider": "password",
                    "key": "dRVeKIGwNwJU0LQ69eUwsUyQRCyPh7DMRiU1bK//LtoMg81SHohquBR9S5fSYa6Uz+yvAHrx2KjBzS+0QXs6bM6fDJVpNodXOgA5XtNMV+iA8hVZlkC12cnfsNw=",
                },
                "secret": secret,
                "nested": {"secret": secret},
                "list": [{"secret": secret}, secret],
            },
            password="password",
        )

        assert cfg["secret"] == "secret"
        assert cfg["nested"]["secret"] == "secret"
        assert cfg["list"][0]["secret"] == "secret"
        assert cfg["list"][1] == "secret"
        assert len(cfg) == 4

    def test_fails_on_bad_secret(self):
        with pytest.raises(errors.DecryptError) as err:
            get_config_yourself(
                {
                    "crypto": {"provider": "password", "key": KEYS["password"]},
                    "secret": {"ciphertext": "bad-secret", "encrypted": "true"},
                },
                password="password",
            )

    def test_fails_on_unknown_provider(self):
        with pytest.raises(ImportError) as err:
            get_config_yourself(
                {"crypto": {"provider": "fake-provider", "key": "adsf"}}
            )
