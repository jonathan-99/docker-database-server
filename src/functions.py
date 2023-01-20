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
    from sql_class import DataBase
    from injection_class import InjectorCheck
    from flask import jsonify
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


def enact_mysql_command(command: str, table_name: str, data: str) -> json:
    """
    A generic function which calls the mysql class and returns all data in json format.
    :param command:
    :param data:
    :param injectorObject:
    :param dbObject:
    :return:
    """
    print("Enact_mysql_command: ", command)
    logging.debug('Enact_mysql_command: {}'.format(command))

    # injectorObject = InjectorCheck()
    # injectorObject.add(str(data))
    # check = injectorObject.check_against_comment()
    check = True
    if check:
        if command == 'ADDTABLE':
            a = DataBase()
            output = a.add_data('ADDTABLE', table_name, '')
        elif command == 'ADDDATA':
            a = DataBase()
            output = a.add_data('ADDDATA', table_name, data)
        elif command == 'GET-DATA':
            a = DataBase()
            output = a.get_data(table_name, data)
        else:
            output = {'temp': 'these needs doing'}
        print("enact_mysql_command() ", output)
        return output
    else:
        return {'Error with input being dodgy': 'something'}

