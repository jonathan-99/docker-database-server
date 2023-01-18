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
    from config import mysql
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

    def add_data(self, add_type: str, table_name: str, key: list) -> str:
        sql = ""
        if add_type == 'ADDTABLE':
            sql = "CREATE TABLE {}".format(table_name)
        elif add_type == 'ADDDATA':
            sql = "INSERT TABLE {} ({})".format(table_name, key)
        else:
            pass
        try:
            cnx = mysql.connector.connect(user='root', database='mydatabase')
            mycursor = cnx.cursor()

        # check the table exists first

            print("sql: ", sql)
            mycursor.execute(sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.commit()
            mycursor.close()
            cnx.close()
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
