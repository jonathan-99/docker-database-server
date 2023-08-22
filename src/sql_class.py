#!/usr/bin/env python3

try:
    import os
    import sys
    import csv
    import json
    import logging
    import re
    import datetime
    import src.class_file as config_file
    import sqlite3 as database
    import src.mysql_error_translation
    # import mysql.connector
    # from mysql.connector import errorcode
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def error_translation(code: int) -> json:
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

    def __init__(self, type_use: str) -> None:
        logging.debug('Initiating a database object')
        """
        This function creates the Database object which is used to control the engagement with the sqlite3 database.
        """
        #  -- get config data here. --
        c = config_file.ConfigData()
        self.__database_name = ""
        if type_use == 'main':
            self.__database_name = c.get_database_name()
        else:
            self.__database_name = c.get_testing_database_name()

        self.__table_name = []
        self._connection_user = 'user'
        self._connection_password = 'password'
        self._connection_host = '127.0.0.1'
        self._connection_port = 3306

    def get_database_name(self):
        return self.__database_name

    @staticmethod
    def _check_sql_statement(inp: str) -> bool:
        if database.complete_statement(inp):
            return True
        else:
            return False


    @staticmethod
    def check_database_exists(database_name: str) -> bool:
        """
        This checks to see if the database file exists only.
        """
        return os.path.isfile(database_name)

    def check_table_exists(self, table_name: str) -> bool:
        """
        This function checks if a table exists only. Pre-req - the database must be checked first.
        """
        sql = "SELECT * FROM sqlite_master WHERE type='table' ORDER BY name;"
        output = self._send_sql(self.__database_name, sql)
        if table_name in output['send_sql() return']['sql output']:
            return True
        else:
            return False

    def add_table(self, table_name: str) -> bool:
        """
        Prerequisite, check if database exists, then this will add a specific table.
        """
        sql = "CREATE TABLE {} ({});".format(table_name, 'test_column VARCHAR(20)')
        output = self._send_sql(self.__database_name, sql)
        if '' in output['send_sql() return': 'sql output']:
            return True
        else:
            internal_error = "sql_class.add_table() error - {}".format(output)
            logging.debug(internal_error)
            print(internal_error)
            return False

    @staticmethod
    def add_data_to_table(table_name: str, inp: list) -> bool:
        """
        This function will add data to a table. Assume columns exists
        """
        string_value = ""
        for i in inp:
            string_value += str(i)
        sql = "INSERT TABLE {} VALUES {}".format(table_name, string_value)
        for i in inp:
            sql += " ADD COLUMN {} VARCHAR(20)".format(i)
        sql += ";"
        return True

    def get_data_from_table(self, table_name: str, data: list) -> json:
        """
        This function returns the data from a table by each column.
        {"table name": "<name>",
            {"column 1 title": [data1, data2], "column 2 title": [data3, data4]}}
        """
        if not data:
            sql_select_where = "*"
        elif len(data) == 0:
            sql_select_where = str(data[0])
        else:
            sql_select_where = "*"  # this is for multiple columns
        
        sql = "SELECT {} FROM table {} WHERE type='table'".format(sql_select_where, table_name)
        output = self._send_sql(self.__database_name, sql)
        print("Need to refine the return into json format")
        print("get_data_from_table -- {}".format(output))
        return output

    def get_table_details(self, input_value: str) -> json:
        """
        This function returns column headings.
        """
        sql = "SELECT * FROM {} WHERE type='table';".format(input_value)
        output = self._send_sql(self.__database_name, sql)
        return output

    def get_all(self) -> json:
        """
        This function will return everything
        """
        sql = 'SHOW tables;'
        output = self._send_sql(self.__database_name, sql)
        return output

    def get_statistics(self) -> json:
        # .rowcount
        # .column_names
        # .description
        # size
        sql = "SELECT count() FROM PRAGMA_TABLE_INFO({});".format(self.__database_name)
        output = self._send_sql(self.__database_name, sql)
        return output

    @staticmethod
    def _send_sql(database_name: str, sql: str):
        print(">> send_sql()")
        logging.debug(">> in send_sql..." + str(type(sql)) + sql)
        try:
            connection = database.connect(database_name)
            # print("** connection {} ".format(connection.total_changes))
            mycursor = connection.cursor()
            temp_output = mycursor.execute(sql).fetchone()
            print(">> mycursor.execute output ", temp_output)

            output = mycursor.fetchall()

            connection.commit()
            mycursor.close()
            connection.close()
        # www.sqlite.org/rescode.html#extrc
        except ConnectionError as err:
            output = error_translation(err.errno)
        logging.info("send_sql(): Sql done {}".format(sql))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        print(">> send_sql(): SLQ CLASS: ", output)
        output_json = json.dumps(output)
        out = {'send_sql() return': {'sql output': output_json, 'sql': sql, 'datetime': now}}
        print(">> send_sql output: ", out)
        return out
