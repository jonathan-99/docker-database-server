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


class DataBase:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword"
        )

        self.mydb.execute("CREATE DATABASE mydatabase")

    def check_database_exists(self):
        return self.mydb.execute("SHOW DATABASES")

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

