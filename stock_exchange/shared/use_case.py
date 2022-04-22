from stock_exchange.shared import response_object as res


class UseCase(object):
    """Base class for use case objects"""
    def execute(self, request_object):
        """Process particular request object and perform corresponding use case"""
        if not request_object:
            return res.ResponseFailure.build_from_invalid_request_objects(request_object)
        try:
            return self.process_request(request_object)
        except Exception as exc:
            return res.ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc))
            )

    def process_request(self, request_object):
        raise NotImplementedError(
            "process_request() not implemented by UseCase class"
        )
