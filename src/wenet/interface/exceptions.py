class AuthenticationException(ValueError):

    def __init__(self, interface: str, http_status_code: int, server_response: str) -> None:
        super().__init__(f"Not a valid authentication for the [{interface}] interface. Request has return a code [{http_status_code}] with content [{server_response}]")
        self.http_status_code = http_status_code
        self.server_response = server_response
        self.message = f"Not a valid authentication for the [{interface}] interface. Request has return a code [{http_status_code}] with content [{server_response}]"


class NotFound(ValueError):

    def __init__(self, object_type: str, object_id: str, http_status_code: int, server_response: str) -> None:
        super().__init__(f"{object_type} with [{object_id}] does not exist. Request has return a code [{http_status_code}] with content [{server_response}]")
        self.http_status_code = http_status_code
        self.server_response = server_response
        self.message = f"{object_type} with [{object_id}] does not exist. Request has return a code [{http_status_code}] with content [{server_response}]"


class CreationError(ValueError):

    def __init__(self, http_status_code: int, server_response: str) -> None:
        super().__init__(f"Request has return a code [{http_status_code}] with content [{server_response}]")
        self.http_status_code = http_status_code
        self.server_response = server_response
        self.message = f"Request has return a code [{http_status_code}] with content [{server_response}]"


class RefreshTokenExpiredError(Exception):

    def __init__(self, *args) -> None:
        super().__init__(*args)
