class Loop:
    is_running = False
    current_position = 0
    MAX_LOOP = 20

    def start(self, callback, max_loop = None):
        if max_loop is not None and max_loop != 20:
            self.MAX_LOOP = max_loop
        self.current_position = 0
        self.is_running = True
        self.run(callback)

    def stop(self):
        self.is_running = False   
    
    def run(self, callback):
        if self.is_running:
            if self.current_position <= self.MAX_LOOP:
                self.current_position += 1
                callbackResult = callback()
                if not Loop.check_if_break_loop(callbackResult):
                    return self.run(callback)
        self.stop()

    def is_first(self):
        if self.current_position == 1:
            return True
        return False
    
    @staticmethod
    def check_if_break_loop(response):
        if response is False or response == "BREAK":
            return True
        return False
    
    @staticmethod
    def check_if_continue_loop(response):
        if response == "CONTINUE":
            return True
        return False
