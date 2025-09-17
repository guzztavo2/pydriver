from typing import Union
import mysql
from Resources.core.Utils import Utils
from Resources.integrations.ApiUser import ApiUser
from Resources.integrations.MySql import MySql

class MySqlConnection:
    MYSQL = None

    def fetch_data(self, map_keys:list = None, user: Union[ApiUser,str] = None, procedure:str = ""):
        try:
            if user is None:
                user = self.user.get_cpf()
                
            conn = self.get_mysql_connection()
            
            procedureProps = [self.MYSQL.consult_table_name,self.MYSQL.result_table_name]
            cursor = conn.cursor(dictionary=True)
            cursor.callproc(procedure,procedureProps)
            
            for result in cursor.stored_results():
                data = result.fetchone()
                if data:
                    if map_keys is not None and isinstance(map_keys, list):
                        result = {}
                        for key in map_keys:
                            result[map_keys[map_keys.index(key)]] = data['@' + key]
                        return result
                    else:
                        return data
                    
            return False
        except mysql.connector.errors.ProgrammingError as e:
            Utils.print_with_time(f"Error in SQL:\n{e}\n")
            myresult = None
        except Exception as e:
            Utils.print_with_time(f"Error in fetch data: {e}")
            myresult = None
        finally:
            if cursor: 
                cursor.close()
            if conn:
                conn.close()
        return False if myresult is None or 'error' in str(myresult) or len(myresult) == 0 else myresult
    
    def get_mysql_connection(self):
        self.initialize_mysql()
        return self.MYSQL.connect_my_sql()
    
    def insert_data(self, data):
        self.initialize_mysql()
        resultTable = self.get_result_table_name()
        insert_query, insert_values = self.MYSQL.build_prepared_insert_query(data, resultTable)
        if insert_query is False:
            return False
        
        return self.MYSQL.execute_prepared_query(insert_query, insert_values)
    
    def execute_mysql_query(self, query):
        self.initialize_mysql()
        return self.MYSQL.execute_query(query)
    
    def get_consult_table_name(self):
        return self.consult_table_name
    
    def get_result_table_name(self):
        return self.result_table_name
    
    def initialize_mysql(self):
        if self.MYSQL is None:
            self.MYSQL = MySql(self.consult_table_name, self.result_table_name)