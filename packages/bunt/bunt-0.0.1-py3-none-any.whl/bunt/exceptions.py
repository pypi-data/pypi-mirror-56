from requests import Response


class BuntException(Exception):
    """
    Generic wrapper for all DSL exceptions
    """


class EnvironmentException(BuntException):
    """
    Generic wrapper for all Environment related exceptions
    """


class ContainerNeverBecameHealthy(EnvironmentException):
    """
    Container was started but never became healthy
    """


class ContainerRestStyleException(BuntException):
    ...


class ContainerRestException(BuntException):
    status_code: int = 0

    def __init__(self, response: Response):
        self.response = response
        super().__init__(
            f'RESTful Service Exception. Status Code: {self.response.status_code}. Contents: {self.response.content}'
        )


class ContainerRestExceptionMultipleChoices(ContainerRestException):
    status_code = 300


class ContainerRestExceptionMovedPermanently(ContainerRestException):
    status_code = 301


class ContainerRestExceptionFound(ContainerRestException):
    status_code = 302


class ContainerRestNotModified(ContainerRestException):
    status_code = 304


class ContainerRestTemporaryRedirect(ContainerRestException):
    status_code = 307


class ContainerRestBadRequest(ContainerRestException):
    status_code = 400


class ContainerRestUnauthorized(ContainerRestException):
    status_code = 401


class ContainerRestForbidden(ContainerRestException):
    status_code = 403


class ContainerRestNotFound(ContainerRestException):
    status_code = 404


class ContainerRestGone(ContainerRestException):
    status_code = 410


class ContainerRestInternalServerError(ContainerRestException):
    status_code = 500


class ContainerRestNotImplemented(ContainerRestException):
    status_code = 501


class ContainerRestServiceUnavailable(ContainerRestException):
    status_code = 503


class ContainerRestPermissionDenied(ContainerRestException):
    status_code = 550
