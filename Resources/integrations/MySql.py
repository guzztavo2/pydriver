import re
import mysql.connector
from Resources.core.Utils import Utils
from Resources.exceptions.MySqlExceptions import MySqlException, MySqlQueryException

class MySql:  
    isProduction = None
    host = None
    user = None
    password = None
    database = None
    idExecucao = 0
    consult_table_name = "d"
    result_table_name = "e"

    def __init__(self, consult_table_name, result_table_name, isProduction = None):
        if MySql.set_is_production(isProduction) is False:
            Utils.print_with_time("Establishing data: database in user test - MYSQL_TEST.")
            self.set_database_host(Utils.get_env('MYSQL_HOST_TEST'))
            self.set_database_user(Utils.get_env('MYSQL_USER_TEST'))
            self.set_database_password(Utils.get_env('MYSQL_PASSWORD_TEST'))
            self.set_database_name(Utils.get_env('MYSQL_DATABASE_TEST'))
        else:            
            Utils.print_with_time("Establishing data: database in user production - MYSQL_PRODUCTION.")
            self.set_database_host(Utils.get_env('MYSQL_HOST_PRODUCTION'))
            self.set_database_user(Utils.get_env('MYSQL_USER_PRODUCTION'))
            self.set_database_password(Utils.get_env('MYSQL_PASSWORD_PRODUCTION'))
            self.set_database_name(Utils.get_env('MYSQL_DATABASE_PRODUCTION'))
        
        self.consult_table_name = consult_table_name
        self.result_table_name = result_table_name
    
    @staticmethod
    def set_is_production(isProduction = None):
        if isProduction is None:
            return True if Utils.get_env('MYSQL_IN_PRODUCTION') == "True" else False
        else:
            return isProduction

    def set_database_host(self,host):
        self.host = host
        return self

    def set_database_user(self,user):
        self.user = user
        return self

    def set_database_password(self,password):
        self.password = password
        return self

    def set_database_name(self,database):
        self.database = database
        return self

    def get_database_host(self):
        return self.host

    def get_database_user(self):
        return self.user

    def get_database_password(self, password):
        if password == self.password:
            return self.password
        return False

    def get_database_name(self):
        return self.database
    
    def connect_my_sql(self):
        try:
            return mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database, auth_plugin='mysql_native_password')
        except Exception as err:
            raise MySqlException(f"Error connecting to MySQL: {err}")
        
    def execute_query(self, query):
        try:
            conn = self.connect_my_sql()
            if conn is False:
                return False
            cursor = conn.cursor()
            cursor.execute(query)
            myresult = cursor.fetchone()
            conn.commit()
            if myresult is None:
                return True
            return myresult
        except Exception as e:
            raise MySqlQueryException(f"Error execute query: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def by_data_from_insert_query(data, table = None, isRecursive = False):
        if data is None or len(data) == 0 or isinstance(data, dict) is False:
            return False
        
        if table is None:
            table = MySql.result_table_name

        query = ""
        value = f""
        
        for key in data:
            val = data[key]
            
            if isinstance(val, str):
                val = re.sub(r'\s+', ' ', val.strip())
                val = val.strip()
                if not val:
                    val = None
            
            if Utils.is_empty(val):
                query += key + ", "
                value += Utils.formata_null(None) + ", "
            elif isinstance(val, dict):
                queryData = MySql.by_data_from_insert_query(table, val, True)
                query += queryData[0]
                value += queryData[1]
            else:
                try:
                    if not Utils.is_empty(val):
                        query += key + ", "
                        value += Utils.formata_null(val) + ", "
                except TypeError:
                    query += key + ", "
                    value += Utils.formata_null(val) + ", "

        if isRecursive:
            return [query, value]
        
        query = f"INSERT INTO {table} ({query[:-2]}) VALUES ({value[:-2]})"
        return query


    def execute_prepared_query(self, query, params=None):
        try:
            conn = self.connect_my_sql()
            if conn is False:
                return False
            cursor = conn.cursor(prepared=True)
            cursor.execute(query, params or ())
            myresult = cursor.fetchone()
            conn.commit()
            if Utils.is_empty(myresult):
                return True
            return myresult
        except Exception as e:
            raise MySqlQueryException(f"Error executing the prepared query: {e}")
        finally:
            if cursor: 
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def build_prepared_insert_query(data, table):
        if  Utils.is_empty(data) or isinstance(data, dict) is False:
            return False, []
        
        columns = []
        placeholders = []
        values = []
        
        for key, val in data.items():
            if not Utils.is_empty(val):
                columns.append(key)
                placeholders.append('%s')
                values.append(val)

        columns_str = ', '.join(columns)
        placeholders_str = ', '.join(placeholders)
        
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders_str})"
        
        return query, values

    @staticmethod
    def build_prepared_update_query(data, tabela, where_clause, where_params):
        if data is None or len(data) == 0:
            return False, []
        
        set_clauses = []
        values = []
        
        for key, val in data.items():
            if not Utils.is_empty(val):
                set_clauses.append(f"{key} = %s")
                values.append(val)
        
        if not set_clauses:
            return False, []
        
        set_str = ', '.join(set_clauses)
        query = f"UPDATE {tabela} SET {set_str} WHERE {where_clause}"
        
        if where_params:
            values.extend(where_params)
        
        return query, values