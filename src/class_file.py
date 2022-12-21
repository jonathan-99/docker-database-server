try:
    import os
    import sys
    import csv
    import json
    import logging
except ImportError as e:
    sys.exit("Importing error: " + str(e))


class config_data:
    """
    This holds and retrieves the config file for all other files to call on.
    """

    def __init__(self):
        self.path = ""
        self.logging_path = ""
        self.log_filename = ""
        self.data_location = ""
        self.server_port = ""
        self.logging_level = ""

    def set_path(self, path_location="/opt/docker-database-server/") -> None:
        self.path = path_location

    def set_logging_path(self, log_path="logging/") -> None:
        self.logging_path = log_path

    def set_log_filename(self, filename="debugging.log") -> None:
        self.log_filename = filename

    def set_data_location(self, location="data/") -> None:
        self.data_location = location

    def set_server_port(self, number=7000) -> None:
        self.server_port = number

    def set_logging_level(self, log_level="logging.DEBUG") -> None:
        self.logging_level = log_level

    def get_path(self) -> str:
        return self.path

    def get_logging_path(self) -> str:
        return self.logging_path

    def get_log_filename(self) -> str:
        return self.log_filename

    def get_data_location(self) -> str:
        return self.data_location

    def get_server_port(self) -> int:
        return int(self.server_port)

    def get_logging_level(self) -> str:
        return self.logging_level

    def show_all(self) -> str:
        output_string = str(self.path) \
            + str(self.logging_path) \
            + str(self.log_filename) \
            + str(self.data_location) \
            + str(self.server_port) \
            + str(self.logging_level)
        return output_string