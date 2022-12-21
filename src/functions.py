#!/usr/bin/env python3

"""
The main functionality is referenced here.
"""

try:
    import datetime
    import os
    import sys
    import time
    import logging
    import json
    from class_file import config_data
    # importing the class file for getting config data
except Exception as e:
    print("importing error: ", e)


def get_config() -> config_data:
    """
    Get the config from a json file and return an object class of that data.
    """
    location = "config.json"
    type_of_file = "json"

    config_data_object = config_data()
    print("Path debug default ", location)
    if type_of_file == "json":
        try:
            f = open(location)
            data = json.load(f)
            f.close()
            config_data_object.set_path(data["path"])
            config_data_object.set_logging_path(data["logging_path"])
            config_data_object.set_log_filename(data["log_filename"])
            config_data_object.set_data_location(data["data"])
            config_data_object.set_server_port(data["simple-server-port"])
            config_data_object.set_logging_level(["logging-level"])
        except FileExistsError or FileExistsError as err:
            logging.error("Getting config error: " + str(err))
    else:
        print("was expecting json as a config file")
        config_data_object.set_path()
        config_data_object.set_logging_path()
        config_data_object.set_log_filename()
        config_data_object.set_data_location()
        config_data_object.set_server_port()
        config_data_object.set_logging_level()
    logging.debug("We found these configs: " + str(config_data_object.show_all()))
    return config_data_object


def get_all_data() -> json:
    logging.debug("Get_all_data")
    return {
        "username": "username",
        "theme": "theme",
        "image": "image",
    }
