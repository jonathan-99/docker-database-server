#!/usr/bin/env python3

"""
This file is for enacting the details of app.py
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
    from flask import send_from_directory
    import src.functions as functions
    import src.incoming_data_class
    import src.injection_class
    import src.sql_class as sql_class
    import src.class_file as class_file
    import json
    import os
    import handle_weather_data
    import route_details
except Exception as e:
    print("importing error: ", e)


def send_swagger_ui(path):
    """
    /swagger-ui/<path:path>
    """
    return send_from_directory('swagger-ui', path)

    # Update the route to return the Swagger UI HTML

def swagger_ui():
    """
    /swagger-ui
    """
    return render_template('index.html')


def get_swagger():
    """
    /stuff
    """
    return route_details.get_swagger_function()


def api_get_data(table_name: str, get_column: str) -> json:
    """
    /get/<table_name>/<string:get_column>
    """
    return route_details.get_data(table_name, get_column)



def get_table_names():
    """
    /get-all-table
    Simple api to get all data from database through functions.py
    :return:
    """
    logging.debug("Api_api_get_table_names()")
    try:
        a = sql_class.DataBase('main')
        output = a.get_table_names()
        return jsonify(output)
    except FileNotFoundError as file_err:
        logging.error(f'Error in api_get_table_names() - {file_err}')
        return jsonify({"error": "Database file not found"}), 500
    except Exception as err:
        logging.error(f'Error in api_get_table_names() - {err}')
        return jsonify({"error": "Internal Server Error"}), 500


def index():
    """
    ('/', methods=['GET', 'POST'])
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
    except Exception as error_object:
        logging.error(f"Error processing index request: {error_object}")
        return "Internal Server Error", 500


def process_json():
    """
    /add-weather-data', methods=['POST']
    """
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


def api_create_table(table_name: str) -> json:
    """
    /create-table/<string:table_name>
    Simple api to get all data from database through functions.py
    :return:
    """
    logging.debug('api_create_table')

    a = sql_class.DataBase('main')
    output = a.add_table(table_name)
    print("api_create_table: ", output)
    return output


def api_add_data(deviceid: str, table_name: str, input_data: str, input_request: request) -> bool:
    """
    /add-data/<string:device_name>/<string:table_name>/<string:input_data>
    """
    return route_details.add_data(deviceid, table_name, input_data, input_request)


def get_column_headers(table_name: str) -> json:
    """
    /get/column-headers-from-this/<table_name>
    Get column headers from a specified table.
    """
    logging.debug("api_get_column_headers")

    a = sql_class.DataBase('main')
    output = a.get_column_names_from_table(table_name)
    # this might return a comma separated value that needs to be handled.
    return output



if __name__ == '__main__':
    try:
        print("here in app-routes")
    except Exception as e:
        logging.error(f"Error initializing app: {e}")
