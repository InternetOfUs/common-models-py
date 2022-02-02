from __future__ import absolute_import, annotations


class ApiException(Exception):

    def __init__(self, status_code: int, message: str):
        self.http_status_code = status_code
        self.server_response = message
        super().__init__(f"Unable to complete the request, status code [{self.http_status_code}], error [{self.server_response}]")


class AuthenticationException(ApiException):

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)


class NotFound(ApiException):

    def __init__(self, message: str, status_code: int = 404) -> None:
        super().__init__(status_code, message)


class BadGateway(ApiException):

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(status_code, message)


class BadRequest(ApiException):

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(status_code, message)


class RefreshTokenExpiredError(Exception):

    def __init__(self, *args) -> None:
        super().__init__(*args)
