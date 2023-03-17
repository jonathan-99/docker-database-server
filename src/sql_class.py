#!/usr/bin/env python3

try:
    import os
    import sys
    import csv
    import json
    import logging
    import re
    import mysql.connector
    from mysql.connector import errorcode
except ImportError as e:
    sys.exit("Importing error: " + str(e))


class DataBase:

    def __init__(self):
        logging.debug('Initiating a database object')
        """
        sql = 'CREATE DATABASE mydatabase'
        self.send_sql(sql)
        """

    @staticmethod
    def send_sql(sql: str): # check return is ALWAYS a list
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
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(">>> Something is wrong with your user name or password")
                output = str(err)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(">>> Database does not exist")
                output = str(err.errno)
            elif err.errno == 1050:  # table already exists
                print('>>> table already exists')
                output = str(err.errno) + ' Table seems to exist'
            elif err.errno == 1146: # table doesn't exit
                output = str(err.errno) + ' Table does not seem to exist'
            elif err.errno == 1064:  # SQL syntax error
                output = str(err.errno) + ' SQL syntax error?'
            elif err.errno == 10061:  # server not up
                output = str(err.errno) + 'Is your SQL database up? It cannot connect.'
            else:
                print(err)
                print('>>> Error here not seen: ' + str(err))
                output = str(err)
        logging.info("Sql done {}".format(sql))
        return output

    def check_duplicate(self, table: str, column: str, value: str) -> bool:
        # define what type this is checking
        # sql statement to check if it exists
        # return is: if check in sql return -> return True
        return True

    def check_exists(self, name_to_check: str):
        sql = '`SELECT * FROM information_schema.tables`' # WHERE table_name = {}".format(name_to_check)
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
        print('add_data: ', output, type(output))
        return {'return': str(output)}

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
        return {'output from get': output}

    def get_statistics(self) -> json:
        # .rowcount
        # .column_names
        # .description
        # size
        return {'database size': '10', 'table names': 'one, two, three' }

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
        print("Output: ", output)
        return output
