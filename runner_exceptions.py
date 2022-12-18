from typing import Any


class OutputValidationError(Exception):
    expected: Any
    obtained: Any

    def __init__(self, expected, obtained) -> None:
        self.expected = expected
        self.obtained = obtained
        super().__init__()


class ExceptionValidationError(Exception):
    message: str

    def __init__(self, message) -> None:
        self.message = message
        super().__init__()
