from Resources.core.Utils import Utils

class ApiUser:
    username = None
    password = None
    status = None
    numbers_consult = None
    quantidade_dia = 0

    def __init__(self, username, password, status = "Active", numbers_consult = 0):
        self.username = username
        self.password = password
        self.status = status
        self.numbers_consult = numbers_consult        

    def set_status(self, status):
        self.status = status
        return self
    
    def set_numbers_consult(self, numbers_consult):
        self.numbers_consult = numbers_consult
        return self
    
    def set_username(self, username):
        self.username = username
        return self
    
    def set_password(self, password):
        self.password = password
        return self
    
    def get_status(self):
        return self.status
    
    def get_numbers_consult(self):
        return self.numbers_consult
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def update_numbers_consult(self, number_consult:int = None):
        if number_consult is None:
            self.numbers_consult += 1
        else:
            self.numbers_consult += 1
        return self
    
    @staticmethod
    def dict_to_user(user:dict):
        user = {'username': user.get('username') if not Utils.is_empty(user.get('username')) else user.get('user'), 'password': user.get('password'), 'status': user.get('status'), 'numbers_consult': user.get('numbers_consult') }
        return ApiUser(user['username'], user['password'], user['status'], user['numbers_consult'])