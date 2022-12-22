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
    _comment = "--"

    def __init__(self, incoming):
        self.incoming = incoming

    def check_against_comment(self):
        if self._comment in self.incoming:
            # this is bad -> remove the comment?
            return False
        else:
            return True


class input_format:
    """
    A simple way of creating flexible table entry for any device.
    """
    def __init__(self):
        self.device_id = ""
        self.table_name = ""
        self.key_value = []

    def add(self, name: str, type_of_data: str) -> bool:
        if type_of_data == "dev":
            self.device_id = name
        elif type_of_data == "tab":
            self.table_name = name
        elif type_of_data == "d":
            self.key_value.append(name)
        else:
            return False
        return True


class DataBase:

    def __init__(self):
        logging.debug('Initiating a database')
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword"
        )

        self.mydb.execute("CREATE DATABASE mydatabase")

    def check_database_exists(self):
        logging.debug('Check if database exists.')
        da = self.mydb.execute("SHOW DATABASES")
        temp = []
        for d in da:
            temp.append(d)
        output_data = json.dumps(temp)
        return output_data

    def check_table_exists(self, in_name) -> bool:
        sql = 'SHOW TABLE' + str(in_name)
        print("test: ", sql)
        output_check = self.mydb.execute(sql)
        logging.debug('Checked if table {} exists'.format(in_name))
        if in_name in output_check:
            return True
        else:
            return False

    def add_table(self, name: str, key: list) -> bool:
        try:
            self.mydb.execute("CREATE TABLE {} ({}) ", name, key)
            logging.info("Table {} created successfully.".format(name))
            return True
        except Exception as err:
            logging.error("Error in creating a table: " + str(err))
            return False

    def get_table(self, name: str) -> json:
        try:
            return self.mydb.execute("SHOW {}".format(name))
        except Exception as err:
            logging.error("Error in finding table: " + str(err))

    def add_data(self, input_data: list) -> json:
        """
        Assume the data will come in the expected format...
        :param input_data:
        :return: json
        """
        i = input_format()
        i.add(input_data[0], "dev")
        i.add(input_data[1], "tab")
        i.add(input_data[2], "d")
        sql = 'INSERT INTO {} ({}) VALUES ({}) '.format(str(i.table_name), 'DATETIME, SPEED', i.key_value)
        logging.debug("Sql statement for add: " + str(sql))
        try:
            self.mydb.execute(sql)
            return {"response": "success"}
        except Exception as err:
            logging.error("Error adding data: " + str(err))
            return {"response": "failure to add data to table"}
