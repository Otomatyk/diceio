import regex
import functools
import utils


class Parser:
    def __init__(self, cmd: str):        
        self.cmd = cmd

    def consume_or_none(self, pattern) -> str | None:
        result = regex.search(pattern, self.cmd)

        if result is None:
            return None
        
        group = result.group()
        self.cmd = self.cmd[len(group):]
        
        return group

    def consume_or_fail(self, pattern, error_message) -> str:
        result = self.consume_or_none(pattern)

        utils.fail_if(result is None, error_message)

        return result

    @staticmethod
    def if_consume_succesed(pattern):
        def decorator(fn):
            @functools.wraps(fn)
            def decorated(self):
                consumed = self.consume_or_none(pattern)
                
                if consumed is None:
                    return None
                    
                return fn(self, consumed)
            return decorated
        return decorator
