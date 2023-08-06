# Copyright 2018 Blink Health LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

import re
import boto3
import botocore
from config_yourself.exceptions import InvalidConfig, BlinkConfigException
from .base import CryptoService


class Service(CryptoService):
    """The original KMS CryptoService

    This provider does not need ``secrets``, and will use the AWS default credential chain to get credentials.
    """

    def __init__(self, config, _secrets):
        # secrets are ignored by the kms provider
        self._client = None
        self._region = None
        self._key = None
        self._setup_client(config)

    def _setup_client(self, crypto):
        # Setup the region for kms by looking at `crypto.region` and fallback on parsing
        # the key ARN and extracting the region from it
        try:
            region = crypto.get("region", None)
        except AttributeError as e:
            # When the crypto property exists, but is not a dict, we raise this error.
            raise InvalidConfig(original=e)

        try:
            if not region and "key" in crypto and ":" in crypto["key"]:
                # try and fetch the region name from the key's arn if specified
                # arn:aws:kms:{region}:{account}:{key_name}
                arn = crypto["key"].split(":")
                if len(arn) == 6:
                    region = crypto["key"].split(":")[3]
                else:
                    raise IndexError
        except TypeError:
            # crypto.key is not a string, which is likely a pebkac error!
            msg = (
                "crypto.key is not a string, "
                "please remove the crypto property if no encryption is needed"
            )
            raise InvalidConfig(message=msg)
        except IndexError:
            # crypto.key is likely in the non fq ARN alias/form
            msg = (
                "Could not parse region name from crypto.key. Please ensure you have "
                "specified a fully-qualifed KSM key ARN to replace `{}` before continuing".format(
                    crypto["key"]
                )
            )
            raise InvalidConfig(message=msg)

        if not region or region == "":
            # region not set or empty
            msg = (
                "Unable to resolve AWS region to query when decrypting. "
                "Please use specify a full KMS key ARN in `crypto.key` or set a specific region "
                "by adding a `crypto.region`"
            )
            raise InvalidConfig(message=msg)

        self._region = region
        self._key = crypto["key"]
        self._client = boto3.client("kms", region_name=self._region)

    def decrypt(self, ciphertext):
        try:
            res = self._client.decrypt(CiphertextBlob=ciphertext)
            return res["Plaintext"]
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "AccessDeniedException":
                # when we get this error, the most likely case is region mismatch or bonafide
                # permission error, let's make this error helpful by showing which credentials
                # we tried to use during decryption
                try:
                    creds = boto3.client(
                        "sts", region_name=self._region
                    ).get_caller_identity()["Arn"]
                except Exception:
                    creds = None

                raise KMSDecryptError(
                    str(self._region), self._key, creds=creds, original=e
                )
            else:
                raise


class KMSDecryptError(BlinkConfigException):
    def __init__(self, region, key, creds=None, original=None):
        msg = ""
        if original:
            msg = "{}. ".format(original)

        msg += "Failed to decrypt in region <{}> with key <{}>".format(region, key)

        if creds:
            msg += " using credentials <{}>".format(creds)
        else:
            msg += " with no known credentials"

        self.message = msg
        super(KMSDecryptError, self).__init__(msg)
