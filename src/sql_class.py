#!/usr/bin/env python3

try:
    import os
    import sys
    import csv
    import json
    import logging
    import re
    import datetime
    import sqlite3 as database
    import src.mysql_error_translation
    # import mysql.connector
    # from mysql.connector import errorcode
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def error_translation(code) -> json:
    print("error_translation({}): type: {}".format(code, type(code)))
    first = "error in sqlite3"
    if (code >= 0) & (code < 100):
        second = "0-100: here"
    elif (code > 99) & (code < 1000):
        second = "100-1000: here"
    else:
        second = str(code) + "now catch it here"
    output = {first: second}
    logging.error("MySQL error." + str(output))
    return output


class DataBase:

    def __init__(self):
        logging.debug('Initiating a database object')
        """
        sql = 'CREATE DATABASE mydatabase'
        self.send_sql(sql)
        """
        #self.database_name = config_file["database_name"]


    def __mysql_database_connection_details__(self):
        self.user = 'user',
        self.password = 'password',
        self.host = '127.0.0.1',
        self.port = 3306,
        #self.database_name = config_file["database_name"]


    @staticmethod
    def send_sql(database_name: str, sql: str):
        print(">> send_sql({})".format(sql))
        logging.debug(">> in send_sql..." + str(type(sql)) + sql)
        try:
            connection = database.connect(database_name)
            # print("** connection {} ".format(connection.total_changes))
            mycursor = connection.cursor()
            temp_output = mycursor.execute(sql).fetchall()
            print(">> temp_output ", temp_output)

            output = mycursor.fetchall()

            connection.commit()
            mycursor.close()
            connection.close()
        # www.sqlite.org/rescode.html#extrc
        except ConnectionError as err:
            output = error_translation(err)
        logging.info("send_sql(): Sql done {}".format(sql))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        print("send_sql(): SLQ CLASS: ", output)
        output_json = json.dumps(output)
        out = {'send_sql() return':
                   {
                        'sql output': output_json,
                        'sql': sql,
                        'datetime': now
                    }
               }
        print("send_sql output: ", out)
        return out

    def check_duplicate(self, table: str, column: str, value: str) -> bool:
        # define what type this is checking
        # sql statement to check if it exists
        # return is: if check in sql return -> return True
        return True

    def check_exists(self, database: str, name_to_check: str):
        print("check_exist({})".format(name_to_check))
        sql = '`SELECT * FROM INFORMATION_SCHEMA.TABLES` WHERE table_name = {}'.format(name_to_check)
        output = self.send_sql(database, sql)
        print(" -- check {} exists within {}".format(name_to_check, output))
        if name_to_check in output:
            print(" -- {} already exists:".format(name_to_check))
            return True
        else:
            print(" -- {} is new".format(name_to_check))
            return False

    def add_data(self, database: str,  add_type: str, table_name: str, key: list) -> json:
        print("add_data({}, {}, {}, {})".format(database, add_type, table_name, key))
        sql = ""

        if (add_type == 'ADDTABLE') & (not self.check_exists(database, table_name)):
            print("add_data(): ", table_name)
            sql = "CREATE TABLE {} ({});".format(table_name, 'test_column VARCHAR(20)')
        elif add_type == 'ADDDATA':
            sql = "ALTER TABLE {}".format(table_name)
            for k in key:
                sql += " ADD COLUMN {} VARCHAR(20)".format(k)
            sql += ";"
            print("ADDDATA, sql statement: ", sql)
        else:
            pass
        output = self.send_sql(database, sql)
        print('add_data: ', output, type(output))
        return {'return': str(output)}

    def get_data(self, database: str, type_of_request: str, data) -> json:
        """
        Types of request are: Table names, column names, everything, values from specific column.
        :param type_of_request: TABLES
        :param data:
        :return:
        """
        print("get_all(self, {}, {}):".format(type_of_request, data))
        if type_of_request == 'tables':
            #  SELECT {} FROM sys.tables
            sql = 'SELECT {} FROM sys.tables;'.format(str(data))
        elif type_of_request == 'column':
            sql = "DESCRIBE `{}`;".format(data.upper()) #  SHOW COLUMNS FROM
        elif type_of_request == 'SPECIFIC':
            sql = 'SHOW TABLE {}'.format(data)
        elif type_of_request == 'GET-ALL':
            sql = 'SHOW tables;'
            print("within get_data(): elif GET-ALL")
        else:
            sql = 'SHOW tables;'
        print('get_data(): sql statement: ', sql)
        output = self.send_sql(database, sql)
        print("output from get_data(): ", output)
        return output

    def get_statistics(self) -> json:
        # .rowcount
        # .column_names
        # .description
        # size
        return {'database size': '10', 'table names': 'one, two, three'}

    @staticmethod
    def get_all_data() -> str:
        """
        This will return a json of summary data of all tables.
        + Table names.
        + Columns.
        + Number of data points.
        :return: json
        """
        logging.debug("Get all data function")
        sql_statement_all = 'SELECT *'
        sql_statement_table = 'SHOW TABLES'
        column_headers = 'select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='
        output = sql_statement_all
        print("Get_all_data(): ", output)
        return output
