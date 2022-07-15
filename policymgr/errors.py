"""Define package errors."""


class CloudOneResponseError(Exception):
    pass


class CloudOneError(CloudOneResponseError):
    """Exception for when CloudOne throws an error with a numeric value.

    Args:
        error_number (int): Non-zero integer.
        error_message (str): Message describing the issue that was encountered.

    """

    def __init__(self, error_number: int, error_message: str):
        """Initialize NumericError object."""
        super().__init__(self)
        self.message = "Error %d: %s" % (error_number, error_message)

    def __str__(self):
        """Message to display with error."""
        return self.message


class CloudOneHttpError(CloudOneResponseError):
    """Exception for when CloudOne throws an error without a numeric value.

    Args:
        error_message (str): Message describing the issue that was encountered.

    """

    def __init__(self, error_message: str):
        """Initialize ErrorMessage object."""
        super().__init__(self)
        self.message = error_message

    def __str__(self):
        """Message to display with error."""
        return self.message


class CloudOneHttp400Error(CloudOneHttpError):
    pass


class CloudOneHttp500Error(CloudOneHttpError):
    pass


class RequestConnectionError(IOError):
    pass
