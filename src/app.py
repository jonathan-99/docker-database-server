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
    from flask import Flask, jsonify, request
    from flask import render_template
    import src.functions as functions
    import src.incoming_data_class
    import src.injection_class
    import src.sql_class as sql_class
    import src.class_file as class_file
    import json
    import jinja2
    import os
    import handle_weather_data
    from src.swagger_api import setup_swagger
except Exception as e:
    print("importing error: ", e)

app = flask.Flask(__name__, template_folder='../templates')
# os.system('sudo /etc/init.d/mysql start')
setup_swagger(app)


def create_app(port_numb=5000) -> None:
    try:
        app.run(debug=True, host='127.0.0.1', port=port_numb)
    except Exception as err:
        logging.error(f"Error running Flask app: {err}")
        print(f'create_app() - {err}')


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Default index page which will show database stats: size, last entry.
    :return:
    """
    try:
        if request.method == 'POST':
            print("POST request received")
        elif request.method == 'GET':
            print("GET request received")
        else:
            print("Unsupported request method")
        return render_template("index.html")
    except Exception as erro:
        logging.error(f"Error processing index request: {erro}")
        return "Internal Server Error", 500


@app.route('/add-weather-data', methods=['POST'])
def process_json():
    try:
        data = request.json
        source_ip = request.remote_addr

        logging.debug(f'process_json() - POST from  {source_ip} - {datetime.datetime.now()}')

        if data:
            return_data = handle_weather_data.manage_weather_data(data, source_ip)
            print(f'process_json() - here {return_data}')
            return jsonify({"message": "Received correct JSON data", "data": data, "source_ip": source_ip}), 200
        else:
            return jsonify({"message": "Received wrong JSON data", "data": data, "source_ip": source_ip}), 200

    except Exception as err:
        logging.error(f"Error processing JSON data: {err}")
        return jsonify({"error": "Invalid JSON data"}), 400


@app.route("/create-table/<string:table_name>")
def api_create_table(table_name: str) -> json:
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    logging.debug('api_create_table')

    a = sql_class.DataBase('main')
    output = a.add_table(table_name)
    print("api_create_table: ", output)
    return output


@app.route("/add-data/<string:device_name>/<string:table_name>/<string:input_data>")
def api_add_data(deviceid: str, table_name: str, input_data: str) -> bool:
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


@app.route("/get/column-headers-from-this/<table_name>")
def api_get_column_headers(table_name: str) -> json:
    """
    Get column headers from a specified table.
    """
    logging.debug("api_get_column_headers")

    a = sql_class.DataBase('main')
    output = a.get_column_names_from_table(table_name)
    # this might return a comma separated value that needs to be handled.
    return output


@app.route("/get/<table_name>/<string:get_column>")
def api_get_data(table_name: str, get_column: str) -> json:
    """
    Get data from a specific table and column.
    :return: json
    """
    logging.debug("api_add_data: {}".format(get_column))

    input_list = get_column.split()

    a = sql_class.DataBase('main')
    output = a.get_data_from_table(table_name, input_list)
    return output


@app.route("/get-all-table")
def api_get_table_names():  # -> json:
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    logging.debug("Api_api_get_table_names()")
    try:
        a = sql_class.DataBase('main')
        output = a.get_table_names()
        return output
    except Exception as err:
        logging.error(f'Error in api_get_table_names() - {err}')


if __name__ == '__main__':
    try:
        c = class_file.ConfigData()
        total_path = c.get_logging_path() + c.get_log_filename()
        print(f'total_path - {total_path}')
        logging.basicConfig(filename=total_path, level=c.get_logging_level())
        print(f'main() - {c.show_all()}')
        create_app(6005)
    except Exception as e:
        logging.error(f"Error initializing app: {e}")
