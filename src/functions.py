#!/usr/bin/env python3

"""
The main functionality is referenced here.
"""

try:
    import datetime
    import re
    import os
    import sys
    import time
    import logging
    import json
    from src.class_file import ConfigData
    from src.sql_class import DataBase
    from src.injection_class import InjectorCheck
    import src.app as app
    from flask import jsonify
except Exception as e:
    print("importing error: ", e)


def get_config(default_location='config.json') -> ConfigData:
    """
    Get the config from a json file and return an object class of that data.
    """
    type_of_file = "json"

    config_data_object = ConfigData()
    print("Path debug default ", default_location)
    if type_of_file == "json":
        try:
            f = open(default_location)
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


def enact_mysql_command(command: str, table_name: str, data) -> json:
    """
    A generic function which calls the mysql class and returns all data in json format.
    :param command:
    :param data:
    :return: json
    """
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
        elif command == 'GET-COLUMN':
            a = DataBase()
            output = a.get_data('column', table_name)
        else:
            output = {'temp': 'these needs doing'}
        logging.debug("enact_mysql_command() " + str(output))
        return output
    else:
        return {'Error with input being dodgy': 'something'}



def get_urls(filename: str) -> list:
    """

    :param filename:
    :return:
    """
    infile = open(filename)
    data = infile.readlines()
    result = []
    for line in data:
        matching = re.search(r'(@app\.route\(\")((/[a-z]*[-/][a-z]*))', line)
        if matching != None:
            result.append(matching.group(2))
    infile.close()
    return result

def get_func_names(filename):
    """

    :param filename:
    :return:
    """
    infile = open(filename)
    data = infile.readlines()
    result = []
    for line in data:
        matching = re.search(r'\s*def (\w+)', line)
        if matching != None:
            result.append(matching.group(1))
    infile.close()
    return result

def get_directory_listing(input_directory='testing/') -> list:
    names = get_func_names('src/app.py')
    urls = get_urls('src/app.py')
    input_list = ['/',
                   '/get-column/tablename-columnname',
                   '/get/all',
                   '/add_data/table_name/input_data',
                   '/create_table/table_name',
                   '/get-all-table]']
    return urls

  
  
def html_table(input_value) -> list:
    """
    This function takes values and places them in a html list
    :param input_value:
    :return list:
    """
    logging.debug("html_table")

    output = ['<table>']
    for sublist in input_value:
        output.append('<tr><td>')
        output.append('</td><td>'.join(sublist))
        output.append('</td></tr>')
    output.append('</table>')
    return output

def create_html_page_wrapper(name: str) -> tuple:
    """
    Need the start and end of a html page.
    :return: str, str
    """
    logging.debug("create_html_page_wrapper with " + name)

    title = "<!DOCTYPE html><head><title>" + name
    title += "</title></head><body>"
    end_tags = "</body></html>"
    return title, end_tags
