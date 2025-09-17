from Resources.core.Utils import Utils
class MySqlException(Exception):
    def __init__(self, message:str):
        super().__init__(message)
        Utils.print_with_time(message)

class MySqlQueryException(Exception):
    def __init__(self, message:str):
        super().__init__(message)
        Utils.print_with_time(message)
    