from typing import Union
from Resources.core.Utils import Utils
from Resources.integrations.ApiUser import ApiUser
from Resources.exceptions.UserExceptions import UserNotFound
from Resources.exceptions.ApiExceptions import FailRequestAPI
class Api:    
    headers = {'ApiKey': 'NEEDED_?', 'Content-Type': 'application/x-www-form-urlencoded'}
    API_URL = Utils.get_env('API_URL')
    user = None

    def request_and_prepare_response(self, url, headers, payload = None):
        response = Utils.request_and_prepare_response(url, headers, payload)
        if response is False:
            return False
        elif response is not None:
            if 'erro' in response:
                raise FailRequestAPI(f"Erro na resposta da API: {response}")
            return response
        else:
            raise FailRequestAPI("Erro ao fazer a requisição para a API.")

    def get_user(self):
        user = self.user
        if Utils.is_empty(user) or not isinstance(user, ApiUser):
            raise UserNotFound()
        return user
    
    def search_user(self, data:dict = None):
        Utils.print_with_time(f"Search a user")
        url = self.API_URL + 'get_user'
        if data is not None:
            response = self.request_and_prepare_response(url + f"?{Utils.url_encoded(data)}", self.headers)
        else:
            response = self.request_and_prepare_response(url, self.headers)

        if Utils.is_empty(response):
            raise FailRequestAPI()
        
        self.set_user(response)

        Utils.print_with_time(f"User found: {self.user.get_username()}")
        return self.user

    def set_user(self, user:Union[dict,ApiUser]):
        if not Utils.is_empty(user) and isinstance(user, dict):
            self.user = ApiUser.dict_to_user(user)
        else:
            self.user = user
            return self.user
        
    def disable_user(self, erro:str):
        url = self.API_URL + 'disable_user/'
        data = {'username': self.user.get_username(), 'erro': erro}

        return self.request_and_prepare_response(url + f"?{Utils.url_encoded(data)}", self.headers)