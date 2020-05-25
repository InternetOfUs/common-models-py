class TaskNotFound(ValueError):
    def __init__(self, task_id: str) -> None:
        super().__init__(f"Task [{task_id}] does not exist")
        self.message = f"Task [{task_id}] does not exist"


class UpdateMetadataError(ValueError):
    def __init__(self, wenet_user_id: str, telegram_id: int) -> None:
        super().__init__(f"No WeNet user [{wenet_user_id}] associated with Telegram id [{telegram_id}]")
        self.message = f"No WeNet user [{wenet_user_id}] associated with Telegram id [{telegram_id}]"


class TaskCreationError(ValueError):

    def __init__(self, http_status: int, json_response: dict) -> None:
        super().__init__()
        self.http_status = http_status
        self.json_response = json_response


class TaskTransactionCreationError(ValueError):

    def __init__(self, http_status: int, json_response: dict) -> None:
        super().__init__()
        self.http_status = http_status
        self.json_response = json_response
