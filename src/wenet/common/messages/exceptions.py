class NotificationTypeError(ValueError):
    def __init__(self, wrong_value: str) -> None:
        self.message = "Unrecognized type [%s] of notification type" % wrong_value
        super().__init__(self.message)


class MessageTypeError(ValueError):
    def __init__(self, wrong_type: str) -> None:
        self.message = "Unrecognized type [%s] of message" % wrong_type
        super().__init__(self.message)
