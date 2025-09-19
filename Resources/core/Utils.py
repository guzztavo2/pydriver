from datetime import datetime
import json, re, sys, time, requests, os
from typing import Union
from urllib.parse import urlencode
from json.decoder import JSONDecodeError
class Utils:    

    @staticmethod
    def current_time():
        return datetime.now().strftime(Utils.get_env('HOUR_FORMAT') or '%d/%m/%Y %H:%M:%S')
        
    @staticmethod
    def print_with_time(message):
        print(f"[{Utils.current_time()}] {message}", flush=True)

    @staticmethod
    def formata_null(valor):
        if Utils.is_empty(valor):
            return 'NULL'
        else:
            valor = str(valor).replace("'", "''")
            if len(valor) > 248:
                valor = valor[:248]
            return f"'{valor}'"    

    @staticmethod
    def get_input(message, onlyLetters:bool = False, onlyNumbers:bool = False)->str:
        if onlyLetters:
            return re.sub(r'[^a-z-A-Z-{_}]', '', (input(message)).strip()) 
        elif onlyNumbers:
            val = re.sub(r'[^0-9]', '', (input(message)).strip())
            try:
                return int(val)
            except BaseException:
                return val
        else:
            return input(message).strip()
        
    @staticmethod
    def json_decoded(data_to_decoded:str) -> Union[dict,bool]:
        try:
            return json.loads(data_to_decoded)
        except JSONDecodeError as e:
            return False
    
    @staticmethod
    def create_file_insert_data(fileDir, dataToInsert) -> bool:
        try:
            f = open(f"{fileDir}", "x")
            f.write(dataToInsert.strip())
            f.close()
            return True
        except Exception as e:
            Utils.print_with_time(f"Error created file: {fileDir}")
            return False

    @staticmethod
    def request_and_prepare_response(url, headers, payload=None, requestMethod:str = 'POST', returnInJson:bool = True, jsonData = None):
        if not Utils.is_empty(payload):
            response = requests.request(requestMethod, url, headers=headers, data=payload, json=jsonData)
        else:
            response = requests.request(requestMethod, url, headers=headers, json=jsonData)

        if returnInJson is False:
            return response

        if not Utils.is_empty(response.text):
            result = Utils.json_decoded(response.text)
        
        return False if Utils.is_empty(result) else result

    @staticmethod
    def url_encoded(data):
        return urlencode(data)
    
    @staticmethod 
    def get_env(key):
        from dotenv import load_dotenv
        load_dotenv()
        val = os.environ.get(key)
        Utils.print_with_time(f"Finding environment variable: {key} ...... {val}")
        return val

    @staticmethod 
    def validate_cpf(cpf):
        cpf = Utils.only_numbers(cpf)
        if len(cpf) != 11:
            return False
        if cpf == cpf[0] * 11:
            return False

        sum_ = sum([int(cpf[i]) * (10 - i) for i in range(9)])
        digit1 = (sum_ * 10 % 11) % 10
        if digit1 != int(cpf[9]):
            return False

        sum_ = sum([int(cpf[i]) * (11 - i) for i in range(10)])
        digit2 = (sum_ * 10 % 11) % 10
        if digit2 != int(cpf[10]):
            return False

        return True

    @staticmethod
    def format_cpf(cpf):
        cpf_only_number = Utils.only_numbers(cpf)
        if len(cpf_only_number) != 11:
            cpf_only_number = cpf_only_number.zfill(11)
        cpf_formated = f"{cpf_only_number[:3]}.{cpf_only_number[3:6]}.{cpf_only_number[6:9]}-{cpf_only_number[9:]}"
        return cpf_formated

    @staticmethod
    def only_numbers(value):
        return re.sub(r'[^0-9]', '', value)

    @staticmethod
    def is_empty(value):
        if isinstance(value, dict) or isinstance(value, list) or isinstance(value, str): 
            return True if value is None or len(value) == 0 or value is False else False
        else:
            return True if value is None or value is False else False

    @staticmethod
    def get_argv(key):
        try:
            return None if Utils.is_empty(sys.argv[key]) else sys.argv[key]
        except Exception:
            return None

    @staticmethod
    def sleep(sec):
        time.sleep(sec)

    @staticmethod
    def flatten_dict(d, parent_key=''):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}[{k}]" if parent_key else k
            if isinstance(v, dict):
                items.extend(Utils.flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)
