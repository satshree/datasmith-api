class BadRequestException(Exception):
    def __init__(self, message="Something went wrong") -> None:
        super().__init__()
        self.message = message
        self.status = 400
