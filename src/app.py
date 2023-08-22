#!/usr/bin/env python3

"""
This is the main python file running the flask app.
"""


try:
    import datetime
    import os
    import sys
    import time
    import logging
    import flask
    from flask import Flask, jsonify
    from flask import render_template
    import src.functions as functions
    import src.incoming_data_class
    import src.injection_class
    import src.sql_class as sql_class
    import src.class_file
    import json
    import jinja2
    import os
    import requests
except Exception as e:
    print("importing error: ", e)

app = flask.Flask(__name__, template_folder='../templates')
# os.system('sudo /etc/init.d/mysql start')

def create_app():
    app.run(debug=True, host='127.0.0.1', port=7000)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Default index page which will show database stats: size, last entry.
    :return:
    """
    if requests.method == 'POST':
        print("post")
    else:
        print("get")
    return render_template("index.html")


@app.route("/create-table/<string:table_name>")
def api_create_table(table_name: str): # -> json:
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    logging.debug('api_create_table')

    a = sql_class.DataBase('main')
    output = a.add_table(table_name)
    print("api_create_table: ", output)
    return output


@app.route("/add-data/<string:table_name>/<string:input_data>")
def api_add_data(table_name: str, input_data: str): # -> json:
    """
    This takes data from any source, containing any data, and adds it to a known table.
    requires input_data to be in the following format.
    device-id : ip address
    table_name : weather
    data (list): "20221209 23", 12.3, ...
    table_name : test
    data (list): "column_a", "column_b" ,...
    :param (str) input_data:
    :return (json) output_data:
    """
    logging.debug("api_add_data: " + table_name + " : " + input_data)

    new_list = []
    if table_name.lower() == 'weather':
        new_list = input_data.split(',')
    elif table_name.lower() == 'test1':
        new_list = input_data.split('-')
    else:
        print("api_add_data new list:", table_name)

    a = sql_class.DataBase('main')
    return a.add_data_to_table(table_name, new_list)


@app.route("/get/<string:get_what>")
def api_get_data(get_what: str):
    """
    Get data from a specific table.
    :return: json
    """
    logging.debug("api_add_data: {}".format(get_what))

    a = sql_class.DataBase('main')
    output = a.get_data_from_table(get_what)
    return output

@app.route("/get-all-table")
def api_get_table_names(): # -> json:
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    output = functions.enact_mysql_command('GET-DATA', 'all', '')
    return output

@app.route("/get-column/<string:get_what>")
def api_get_column_data(get_what: str):
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    logging.debug("api_get_all_data: {}".format(get_what))

    a = sql_class.DataBase('main')
    return a.get_data_from_table(a.get_database_name(), 'column', get_what)

if __name__ == '__main__':
    config = functions.get_config()
    total_path = config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=total_path, level=config.get_logging_level())

    create_app()
