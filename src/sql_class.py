#!/usr/bin/env python3

try:
    import os
    import datetime
    import sys
    import csv
    import json
    import logging
    import re
    import mysql.connector
    from mysql.connector import errorcode
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def error_translation(code) -> json:
    first = 'Error'
    second = ''
    if (code > 0) and (code < 1000):
        second = 'Global Error'
    elif (code > 999) and (code < 2000):
        if code == 1050:
            second += ' 1050. Table already exists'
        elif code == 1064:
            second += ' 1064. SQL syntax error?'
        elif code == 1146:
            second += ' 1146. Table does not seem to exist.'
        else:
            second = "Server error codes reserved for messages sent to clients."
    elif (code > 1999) and (code < 3000):
        second = "Client error codes reserved for use by the client library."
    elif (code > 2999) and (code < 4000):
        second = "Client error codes reserved for use by the client library."
    elif (code > 3999) and (code < 5000):
        second = "Server error codes reserved for messages sent to clients."
    elif (code > 4999) and (code < 6000):
        second = "Error codes reserved for use by X Plugin for messages sent to clients."
    elif (code > 9999) and (code < 50000):
        if code == 10061:
            second += ' 10061. Is your SQL database up? It cannot connect.'
        else:
            second = "Server error codes reserved for messages to be written to the error log (not sent to clients)."
    elif (code > 49999) and (code < 52000):
        second = "50,000 to 51,999: Error codes reserved for use by third parties."
    else:
        second = "This is a new Error to MySQL"

    if code == errorcode.ER_ACCESS_DENIED_ERROR:
        second = "Something is wrong with your user name or password"
    elif code == errorcode.ER_BAD_DB_ERROR:
        second = "Database does not exist"

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

    @staticmethod
    def send_sql(sql: str):  # check return is ALWAYS a list
        logging.debug(">> in send_sql..." + str(type(sql)) + sql)
        #  output = {'beginning': 'end'}
        try:
            cnx = mysql.connector.connect(
                user='user',
                password='password',
                host='127.0.0.1',
                port=3306,
                database='mydatabase'
            )
            mycursor = cnx.cursor()
            print(">> Connection status: ", mycursor)
            print(">> mycursor: ", mycursor.description)

            # check the table exists first

            mycursor.execute(sql)
            output = mycursor.fetchall()
            # out3 = mycursor.description

            cnx.commit()
            mycursor.close()
            cnx.close()
            return output
        except mysql.connector.Error as err:
            output = error_translation(err.errno)
        logging.info("Sql done {}".format(sql))
        out = {'return':
                   [
                       output,
                       {'sql': str(sql)},
                       {'datetime': datetime.datetime.now()}
                   ]
        }
        return out

    def check_duplicate(self, table: str, column: str, value: str) -> bool:
        # define what type this is checking
        # sql statement to check if it exists
        # return is: if check in sql return -> return True
        return True

    def check_exists(self, name_to_check: str):
        sql = '`SELECT * FROM information_schema.tables`'  # WHERE table_name = {}".format(name_to_check)
        output = self.send_sql(sql)
        print(" -- check {} exists within {}".format(name_to_check, output))
        if name_to_check in output:
            print(" -- {} already exists:".format(name_to_check))
            return True
        else:
            print(" -- {} is new".format(name_to_check))
            return False

    def add_data(self, add_type: str, table_name: str, key: list) -> json:
        sql = ""

        if (add_type == 'ADDTABLE') & (not self.check_exists(table_name)):
            print("add_data(): ", table_name)
            sql = "CREATE TABLE {} ({});".format(table_name, 'test_column VARCHAR(20)')
        elif add_type == 'ADDDATA':
            sql = "INSERT TABLE {} ({})".format(table_name, key)
        else:
            pass
        output = self.send_sql(sql)
        print('Possible error:', output)
        return output

    def get_data(self, type_of_request: str, data) -> json:
        """
        Types of request are: Table names, column names, everything, values from specific column.
        :param type_of_request: TABLES
        :param data:
        :return:
        """
        if type_of_request == 'tables':
            sql = 'SELECT * from {};'.format(str(data))
        elif type_of_request == 'column':
            sql = 'SELECT {} from {};'.format(data[0], data[1])
        elif type_of_request == 'SPECIFIC':
            sql = 'SHOW TABLE {}'.format(data)
        elif type_of_request == 'all':
            sql = 'Show tables;'
        else:
            sql = 'Show tables;'
        print('sql statement: ', sql)
        output = self.send_sql(sql)
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
        print("Probable errors: ", output)
        return output
