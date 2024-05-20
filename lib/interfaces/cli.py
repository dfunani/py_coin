class CLIError(Exception):
    """Custom Error For User CLI Errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message