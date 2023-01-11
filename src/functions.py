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
    from flask import jsonify
    import mysql.connector
    from mysql.connector import errorcode
    from config import mysql
    from flask_cors import CORS, cross_origin
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


def enact_mysql_command(command: str, data: str, dbObject: DataBase) -> json:
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

    try:
        cnx = mysql.connector.connect(user='root', database='mydatabase')
        mycursur = cnx.cursor()
        injectorObject = InjectorCheck()

        injectorObject.add(data)
        check = injectorObject.check_against_comment()
        if check:
            if command == 'ADDTABLE':
                sql_statement = dbObject.add_data('tab', data)
                output = mycursur.execute(sql_statement)
            elif command == 'ADDDATA':
                output = "temp"
            elif command == 'GET-ALL':
                output = dbObject.get_all_data()
            else:
                output = "temp"
            print("enact_mysql_command() ", output)
            return jsonify(output)
        else:
            return "Error with input being dodgy"

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.commit()
        mycursur.close()
        cnx.close()
