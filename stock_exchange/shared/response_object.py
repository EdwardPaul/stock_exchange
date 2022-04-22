class ResponseSuccess(object):
    """Response object handling successful operation

    Arguments:
        value(any): Value of successful return from use case
    """
    def __init__(self, value=None):
        self.value = value

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__


class ResponseFailure(object):
    """Response object handling errors while performing use case

    Arguments:
        type_(str): Error type
        message(str): Error message
    """
    # Error in database
    RESOURCE_ERROR = 'RESOURCE_ERROR'
    # Wrong command error
    PARAMETERS_ERROR = 'PARAMETERS_ERROR'
    # Error in system
    SYSTEM_ERROR = 'SYSTEM_ERROR'

    def __init__(self, type_, message):
        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, msg):
        """Process exception messages

        Returns:
            str: Message description
        """
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg

    @property
    def value(self):
        """Property representing dictionary with type and message error"""
        return {'type': self.type, 'message': self.message}

    def __bool__(self):
        return False

    @classmethod
    def build_resourse_error(cls, message=None):
        """Generate ResponseFailure object with resourse error

        Arguments:
            message(str): Error message

        Returns:
            ResponseFailure: Response object with error
        """
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message=None):
        """Generate ResponseFailure object with system error

        Arguments:
            message(str): Error message

        Returns:
            ResponseFailure: Response object with error
        """
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message=None):
        """Generate ResponseFailure object with parameters error

        Arguments:
            message(str): Error message

        Returns:
            ResponseFailure: Response object with error
        """
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_from_invalid_request_objects(cls, invalid_request_object):
        """Generate ResponseFailure object with parameters error from invalid request

        Arguments:
            invalid_request_object(InvalidRequestObject): Error message

        Returns:
            ResponseFailure: Response object with error
        """
        message = "\n".join(["{}: {}".format(err['parameter'], err['message'])
                             for err in invalid_request_object.errors])
        return cls.build_parameters_error(message)
