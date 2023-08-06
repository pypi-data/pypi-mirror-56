import pytest
import warnings
from tests.conftest import get_config_yourself, add_kms_entries, encrypt_test_value


class TestBlinkConfig(object):
    @pytest.mark.parametrize(
        "input_config,expected_config",
        [
            (
                {"encrypted_key": encrypt_test_value("encryptme")},
                {"encrypted_key": "encryptme"},
            ),
            (
                {"encrypted_number": encrypt_test_value("042")},
                {"encrypted_number": "042"},
            ),
            (
                {
                    "nested_encrypted_dict": {
                        "outer_dict": {
                            "first_value": encrypt_test_value("hidden"),
                            "second_value": encrypt_test_value("092"),
                        }
                    }
                },
                {
                    "nested_encrypted_dict": {
                        "outer_dict": {"first_value": "hidden", "second_value": "092"}
                    }
                },
            ),
        ],
    )
    def test_config(self, input_config, expected_config):
        input_with_kms_entries = add_kms_entries(input_config)
        expected_with_kms_entries = add_kms_entries(expected_config)
        config_yourself = get_config_yourself(input_with_kms_entries)

        assert config_yourself._data == expected_with_kms_entries

    @pytest.mark.parametrize(
        "input_config, other_config, expected_overridden_config",
        [
            (
                {"both_key": "initial_value"},
                {"both_key": "new_value", "other_key": "other_value"},
                {"both_key": "new_value"},
            ),
            (
                {"change_key": "initial_value", "untouched_key": "untouched_value"},
                {"change_key": "other_value", "other_key": "other_value"},
                {"change_key": "other_value", "untouched_key": "untouched_value"},
            ),
            (
                {
                    "outer-key": {
                        "inner-change-key": "initial-value",
                        "inner-untouched": "untouched-value",
                    }
                },
                {
                    "outer-key": {
                        "inner-change-key": "new-value",
                        "inner-other": "other-value",
                    }
                },
                {
                    "outer-key": {
                        "inner-change-key": "new-value",
                        "inner-untouched": "untouched-value",
                    }
                },
            ),
            (
                {"change-secret": encrypt_test_value("initial-secret")},
                {"change-secret": encrypt_test_value("other-secret")},
                {"change-secret": encrypt_test_value("other-secret")},
            ),
            (
                {
                    "outer-key": {
                        "untouched-secret": encrypt_test_value("my-secret"),
                        "touched-secret": encrypt_test_value("initial-secret"),
                    }
                },
                {
                    "outer-key": {
                        "other-key": "other-value",
                        "touched-secret": encrypt_test_value("new-secret"),
                    }
                },
                {
                    "outer-key": {
                        "untouched-secret": encrypt_test_value("my-secret"),
                        "touched-secret": encrypt_test_value("new-secret"),
                    }
                },
            ),
        ],
    )
    def test_override(self, input_config, other_config, expected_overridden_config):
        with warnings.catch_warnings(record=True):
            input_with_kms_entries = get_config_yourself(
                add_kms_entries(input_config), add_kms_entries(other_config)
            )

            expected_with_kms_entries = get_config_yourself(
                add_kms_entries(expected_overridden_config)
            )

            assert input_with_kms_entries._data == expected_with_kms_entries._data
