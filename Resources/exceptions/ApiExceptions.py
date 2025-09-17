from Resources.core.Utils import Utils
class FailRequestAPI(Exception):
    def __init__(self, message:str = None):
        if message:
            super().__init__(message)
            Utils.print_with_time(f"ERROR DURING REQUEST IN API: {message}")
        Utils.print_with_time(f"ERROR DURING REQUEST IN API")
        pass
    pass