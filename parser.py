from random import randint, shuffle
from regex import search
from functools import wraps
from utils import fail_if


class Parser:
    def __init__(self, cmd: str):        
        self.cmd = cmd

    def consume_or_none(self, pattern) -> str | None:
        result = search(pattern, self.cmd)

        if not result:
            return None
        
        group = result.group()
        self.cmd = self.cmd[len(group):]
        
        return group

    def consume_or_fail(self, pattern, error_message) -> str:
        result = self.consume_or_none(pattern)

        fail_if(result is None, error_message)

        return result

    @staticmethod
    def if_consume_succesed(pattern):
        def decorator(fn):
            @wraps(fn)
            def decorated(self):
                consumed = self.consume_or_none(pattern)
                
                if not consumed:
                    return None
                    
                return fn(self, consumed)
            return decorated
        return decorator
