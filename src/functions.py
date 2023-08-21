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



def enact_mysql_command(database: str, command: str, table_name: str, data) -> json:
    """
    A generic function which calls the mysql class and returns all data in json format.
    :param command:
    table_name:
    :param data:
    :return: json
    """
    logging.debug('Enact_mysql_command: {}'.format(command))

    # injectorObject = InjectorCheck()
    # injectorObject.add(str(data))
    # check = injectorObject.check_against_comment()
    check = True

    c = get_config('src/config.json')
    c.set_database_name('src/database_name.db')
    a = DataBase(c.get_database_name())


    if check and (a.check_database_exists(a.database_name)):
        if command == 'ADDTABLE':
            output = a.add_table(table_name)
        elif command == 'ADDDATA':
            output = (a.add_data_to_table(table_name, data))
        elif command == 'GET-DATA':
            output = (a.get_data_from_table(table_name, data))
        elif command == 'GET-COLUMN':
            output = a.get_data(database, 'column', table_name)
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
        if matching is not None:
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
        if matching is not None:
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
