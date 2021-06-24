class AuthenticationException(ValueError):

    def __init__(self, interface: str) -> None:
        super().__init__(f"Not a valid authentication for the [{interface}] interface")
        self.message = f"Not a valid authentication for the [{interface}] interface"


class NotFound(ValueError):

    def __init__(self, object_type: str, task_id: str) -> None:
        super().__init__(f"{object_type} with [{task_id}] does not exist")
        self.message = f"{object_type} with [{task_id}] does not exist"


class CreationError(ValueError):

    def __init__(self, http_status: int, json_response: dict) -> None:
        super().__init__()
        self.http_status = http_status
        self.json_response = json_response


class RefreshTokenExpiredError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
