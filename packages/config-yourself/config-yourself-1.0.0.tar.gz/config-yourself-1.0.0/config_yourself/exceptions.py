class BlinkConfigException(Exception):
    """The base BlinkConfig Exception"""

    pass


class DecryptError(BlinkConfigException):
    """A value could not be decrypted"""

    def __init__(self, full_path, original=None):
        msg = "Could not decrypt path {}".format(".".join(full_path))
        super(DecryptError, self).__init__(msg)


class InvalidConfig(BlinkConfigException):
    """A supplied config file was not valid"""

    def __init__(
        self,
        original=None,
        message="crypto property is not an object of key and region.",
    ):
        if original:
            message = "{}\n{}".format(message, original)
        self.message = message
        super(InvalidConfig, self).__init__(message)
