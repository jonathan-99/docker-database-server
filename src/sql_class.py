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
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword"
        )
        """

    def send_sql(self, sql: str) -> str:
        print("in send_sql...", type(sql), sql)
        output = {'beginning': 'end'}
        try:
            cnx = mysql.connector.connect(
                user='user',
                password='password',
                host='127.0.0.1',
                port=3306,
                # database='mydatabase'
            )
            mycursor = cnx.cursor()

            # check the table exists first

            output = mycursor.execute(sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
                output = 'Error here' + str(err)
        else:
            cnx.commit()
            mycursor.close()
            cnx.close()
            output = "Error in send_sql"
        logging.info("Sql done {}".format(sql))
        return output

    def add_data(self, add_type: str, table_name: str, key: list) -> str:
        sql = ""
        if add_type == 'ADDTABLE':
            sql = "CREATE TABLE {}".format(table_name)
        elif add_type == 'ADDDATA':
            sql = "INSERT TABLE {} ({})".format(table_name, key)
        else:
            pass
        output = self.send_sql(sql)
        print('add_data: ', output, type(output))
        return {'return': output}

    def get_data(self, type_of_request: str, data: str) -> str:
        """
        Types of request are: Table names, column names, everything, values from specific column.
        :param type_of_request: TABLES
        :param data:
        :return:
        """
        if type_of_request == 'TABLES':
            sql = 'SHOW {}'.format(type_of_request)
        elif type_of_request == 'COLUMN':
            sql = 'SHOW TABLES'
        elif type_of_request == 'SPECIFIC':
            sql = 'SHOW TABLE {}'.format(data)
        else:
            sql = 'SHOW *'
        output = self.send_sql(sql)
        return {'output from get': output}

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
