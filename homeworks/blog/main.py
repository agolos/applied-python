import mysql.connector
from mysql.connector import Error


dbconfig = {'user': 'root',
            'password': '12345',
            'host': '20.185.73.166'}

class DataBaseAdapter:

    _connection = None

    def __init__(self, db_name):
        self._connection = mysql.connector.connect(database = db_name,**dbconfig)
        self._connection.config()
        try:
            if self._connection.is_connected():
                db_Info = self._connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self._connection.cursor()
                cursor.execute("select user();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if (self._connection.is_connected()):
                cursor.close()
                self._connection.close()
                print("MySQL connection is closed")

    def create_new_database(self, name, is_create_tables: bool):
        create_database_str = f"CREATE DATABASE IF NOT EXISTS {name};"
        self._connection.reconnect()
        cursor = self._connection.cursor()
        cursor.execute(create_database_str)
        print(f"Creating results: {cursor.fetchone()}")
        if is_create_tables:
            cursor.execute(f'USE {name};')
            self.create_tables(cursor)
        cursor.close()
        self._connection.close()

    def create_tables(self, cursor):
        with open('create_tables.sql','r') as f:
            create_script_lst = f.readlines()
        create_script_str = ''.join(create_script_lst)
        for script in create_script_str.split(';\n'):
            cursor.execute(f'{script};')
        print('Tables were created')

    def delete_all_tables(self):
        with open('delete_tables.sql','r') as f:
            delete_script_lst = f.readlines()
        delete_str = ''.join(delete_script_lst)
        self._connection.reconnect()
        cursor = self._connection.cursor()
        for req in delete_str.split('\n'):
            cursor.execute(req)
        print("All tables were deleted.")
        cursor.close()
        self._connection.close()

    def check_databases(self):
        self._connection.reconnect()
        cursor = self._connection.cursor()
        cursor.execute("SHOW tables;")
        print(cursor.fetchall())
        cursor.close()
        self._connection.close()


db = DataBaseAdapter("blogs")
#db.check_databases()
db.create_new_database("blogs", True)
#db.delete_all_tables()



