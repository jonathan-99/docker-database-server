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
    from class_file import ConfigData
    from sql_class import DataBase, InjectorCheck
except Exception as e:
    print("importing error: ", e)


def get_config() -> ConfigData:
    """
    Get the config from a json file and return an object class of that data.
    """
    location = "config.json"
    type_of_file = "json"

    config_data_object = ConfigData()
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


def check_input(potentially_dodgy: str) -> str:
    """
    This needs to sanitise all user data coming in against the Robert') DROPS TABLE * vulnerability.
    :param: potentially_dodgy (str) :
    :return: potentially_safe (str) :
    """
    i = InjectorCheck()
    if i.check_against_comment(potentially_dodgy):
        potentially_safe = potentially_dodgy
    else:
        potentially_safe = "QWERTY"  # safe word
    return potentially_safe


def setup_database():
    d = DataBase()
    print("Check it was successfully setup", d.check_database_exists())


def create_table(name: str, attributes: list) -> json:
    if DataBase.add_table(name, attributes):
        return DataBase.get_table(name)
    else:
        print("Error in creating table called: ", name)
        logging.error("Error in creating table called {}".format(name))
        return {
            "Error": "Something went wrong in create_table"
        }


def get_table(name: str) -> json:
    return DataBase.get_table(name)


def get_all_data() -> json:
    logging.debug("Get_all_data")
    return {
        "username": "username",
        "theme": "theme",
        "image": "image",
    }
