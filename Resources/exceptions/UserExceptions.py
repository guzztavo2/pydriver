from Resources.core.Utils import Utils
class UserNotFound(Exception):
    def __init__(self, message="USER NOT FOUND"):
        super().__init__(message)
        Utils.print_with_time(message)
    