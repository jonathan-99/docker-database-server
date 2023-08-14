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
    import src.sql_class
    import json
    import jinja2
    import os
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

    output = functions.enact_mysql_command('ADDTABLE', table_name, '')
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
    return functions.enact_mysql_command('ADDDATA', table_name, new_list)


@app.route("/get/<string:get_what>")
def api_get_data(get_what: str):
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    print("api_get_data /get/:", get_what)
    temp_output = functions.enact_mysql_command('GET-DATA', str(get_what).lower(), '')
    if 'error' in str(temp_output).lower():
        logging.debug('Getting data from all. ' + temp_output)
        return temp_output
    else:
        multi_o = {}
        temp_list = str(temp_output['send_sql() return']['sql output']).replace('"', '').replace(',', '').replace('[', '').replace(']', '').split(' ')
        for item in temp_list:
            output = functions.enact_mysql_command('GET-COLUMN', item, '')
            multi_o.update(output)
            print("output: ", output, ': ', multi_o)
        print("/get/: ", multi_o)
        multi_output = {"/get/", multi_o}
        logging.debug('Getting data from all. ' + str(output))
        print("print here: ", multi_output)
    return multi_output

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
    temp = []
    temp = get_what.split('-')
    output = functions.enact_mysql_command('GET-DATA', 'column', temp)
    logging.debug("api_get_all_data: " + output)
    return jsonify(output)

if __name__ == '__main__':
    config = functions.get_config()
    total_path = config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=total_path, level=config.get_logging_level())

    create_app()
