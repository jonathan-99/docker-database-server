#!/usr/bin/env python3

"""
This file holds the details of each route called in app.py
"""

import logging
import sql_class


def rule_filter():
    return True

def model_filter():
    return True

def get_swagger_function():
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": '/apidocs',
                "route": '/',
                "rule_filter": rule_filter(),
                "model_filter": model_filter(),
            }
        ],
        "static_url_path": "/swagger-ui",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    return swagger_config


def get_data(table_name: str, get_column: str):

    logging.debug("api_add_data: {}".format(get_column))

    input_list = get_column.split()

    a = sql_class.DataBase('main')
    output = a.get_data_from_table(table_name, input_list)
    return output

def add_data(deviceid: str, table_name: str, input_data: str, request) -> bool:
    """
    This takes data from any source, containing any data, and adds it to a known table.
    requires input_data to be in the following format.
    Parameters:
        deviceid (str): client ip address
        table_name (str) : weather
        input_data (list): "20221209 23", 12.3, ...
        table_name : test or main
    Returns:
        output (bool): True is success.
    """
    logging.debug("api_add_data: " + table_name + " : " + input_data)

    print("Senders IP address - {}".format(request.remote_addr))

    new_list = []
    if table_name.lower() == 'weather':
        new_list = input_data.split(',')
    elif table_name.lower() == 'test1':
        new_list = input_data.split('-')
    else:
        print("api_add_data new list:", table_name)

    a = sql_class.DataBase('main')
    return a.add_data_to_table(deviceid, table_name, new_list)