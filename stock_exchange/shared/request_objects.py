class InvalidRequestObject(object):
    """Request object handling errors"""
    def __init__(self):
        # List of errors obtained while processing command
        self.errors = []

    def add_error(self, parameter, message):
        """Add error to list of errors"""
        self.errors.append({'parameter': parameter, 'message': message})

    def has_errors(self):
        """Check if request object has errors

        Returns:
            bool: Has errors
        """
        return len(self.errors) > 0

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__


class ValidRequestObject(object):
    """Request object handling no errors base class"""
    @classmethod
    def from_dict(cls, input_dict):
        raise NotImplementedError

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__
