try:
    import os
    import sys
    import csv
    import json
    import logging
    import sqlite3
    # import mysql.connector

except ImportError as e:
    sys.exit("Importing error: " + str(e))


class ConfigData:
    """
    This holds and retrieves the config file for all other files to call on.
    """

    def __init__(self):
        self.__get_config('src/config.json')
        self.path = ""
        self.logging_path = ""
        self.log_filename = ""
        self.src = ""
        self.data_location = ""
        self.server_port = 0
        self.logging_level = "DEBUG"
        self.database_name = ""
        self.testing_database_name = ""

    def __get_config(self, input_file_name="src/config.json") -> None:
        """
        Get the config from a json file and return an object class of that data.
        """
        type_of_file = "json"
        if type_of_file == "json":
            try:
                with open(input_file_name, 'r') as fileObject:
                    data = json.load(fileObject)
                    self.set_path(data["path"])
                    self.set_logging_path(data["logging_path"])
                    self.set_log_filename(data["log_filename"])
                    self.set_src(data["src"])
                    self.set_data_location(data["data"])
                    self.set_server_port(data["simple-server-port"])
                    self.set_logging_level(data["logging-level"])
                    self.set_database_name(data["database-name"])
                    self.set_testing_database_name(data["test-database-name"])
            except FileExistsError or FileExistsError as err:
                logging.error("Getting config error: " + str(err))
        else:
            print("was expecting json as a config file")
            self.set_path()
            self.set_logging_path()
            self.set_log_filename()
            self.set_src()
            self.set_data_location()
            self.set_server_port()
            self.set_logging_level()
            self.set_database_name()
            self.set_testing_database_name()
        logging.debug("We found these configs: " + str(self.show_all()))
        return

    def set_testing_database_name(self, db_name="testing/database_name.db") -> bool:
        """
        This function will test the db exists that is being entered, if not, it will default to the config one.
        """
        if os.path.isfile(db_name):
            self.testing_database_name = db_name
            return True
        else:
            print("Error is setting testing database name")
            return False

    def get_testing_database_name(self) -> str:
        return self.testing_database_name

    def set_database_name(self, db_name='src/database_name.db') -> bool:
        """
        This function sets a user entered value, however if the file cannot be found in its current directory,
        it will default to the main src/database_name.db
        """
        if os.path.exists(db_name):
            self.database_name = db_name
            return True
        else:
            print("Error setting a file that doesn't exist in the correct directory")
            return False

    def get_path(self) -> str:
        return self.path

    def set_path(self, path_location="/opt/docker-database-server/") -> bool:
        if os.path.isdir(path_location):
            self.path = path_location
            return True
        else:
            print("Error is setting path.")
            return False

    def set_logging_path(self, log_path="logging/") -> None:
        self.logging_path = log_path

    def set_log_filename(self, filename="debugging.log") -> None:
        self.log_filename = filename

    def set_src(self, src_input="src") -> None:
        self.src = src_input

    def set_data_location(self, location="data/") -> None:
        self.data_location = location

    def set_server_port(self, number=7000) -> None:
        self.server_port = number

    def set_logging_level(self, log_level="logging.DEBUG") -> None:
        self.logging_level = log_level

    def get_database_name(self) -> str:
        return self.database_name

    def get_logging_path(self) -> str:
        return self.logging_path

    def get_log_filename(self) -> str:
        return self.log_filename

    def get_src(self) -> str:
        return self.src

    def get_data_location(self) -> str:
        return self.data_location

    def get_server_port(self) -> int:
        return int(self.server_port)

    def get_logging_level(self) -> str:
        return self.logging_level

    def show_all(self) -> json:
        output_json = {"path": self.path,
                       "logging_path": self.logging_path,
                       "log_filename": self.log_filename,
                       "src": self.src,
                       "data": self.data_location,
                       "simple-server-port": self.server_port,
                       "logging-level": self.logging_level,
                       "database-name": self.database_name,
                       "test-database-name": self.testing_database_name
                       }
        return output_json
