class DiceIOError(Exception):
    def __init__(self, message: str):
        super().__init__()

        self.message = message

def fail_if(condition: bool, error_message: str):
    if condition:
        raise DiceIOError(error_message)
