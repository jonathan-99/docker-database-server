try:
    import os
    import sys
    import csv
    import json
    import logging
    import re
    import mysql.connector
except ImportError as e:
    sys.exit("Importing error: " + str(e))


class InjectorCheck:
    _concern = ['--', 'DEL', 'DELETE']

    def __init__(self):
        self.incoming = ""

    def add(self, value) -> None:
        self.incoming = value

    def check_against_comment(self) -> bool:
        if self._concern in self.incoming:
            # this is bad -> remove the comment?
            return False
        else:
            return True


class Input_Format:
    """
    A simple way of creating flexible table entry for any device.
    """
    def __init__(self):
        self.device_id = ""
        self.table_name = []
        self.key_value = []

    def add(self, name: str, type_of_data: str) -> bool:
        if type_of_data == "dev":
            self.device_id = name
        elif type_of_data == "tab":
            self.table_name.append(name)
        elif type_of_data == "d":
            self.key_value.append(name)
        else:
            return False
        return True


class DataBase:

    def __init__(self):
        logging.debug('Initiating a database object')
        """
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword"
        )
        """
        self.mydb.table_name = []

        self.mydb.execute("CREATE DATABASE mydatabase")
        self.mydb.table_name = ['default']

    def add_data(self, table_name: str, key: list) -> str:
        sql = 'CREATE TABLE {} ({})'.format(table_name, key)
        print("sql: ", sql)
        logging.info("Table {} created successfully.".format(table_name))
        return sql

    def get_data(self, type_of_request: str, data: str) -> str:
        """
        Types of request are: Table names, column names, everything, values from specific column.
        :param type_of_request: TABLES
        :param data:
        :return:
        """
        if type_of_request == 'TABLES':
            output = 'SHOW {}'.format(type_of_request)
        elif type_of_request == 'COLUMN':
            output = 'SHOW TABLES'
        elif type_of_request == 'SPECIFIC':
            output = 'SHOW TABLE {}'.format(data)
        else:
            output = 'SHOW *'
        return output


    def get_all_data(self) -> str:
        """
        This will return a json of summary data of all tables.
        + Table names.
        + Columns.
        + Number of data points.
        :return: json
        """
        logging.debug("Get all data function")
        print("within get_all_data")
        sql_statement_all = 'SHOW *'
        sql_statement_table = 'SHOW TABLES'
        column_headers = 'select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='
        output = sql_statement_all
        print("Output: ", output)
        return output
