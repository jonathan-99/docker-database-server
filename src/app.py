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
    from flask import send_from_directory
    from flasgger import Swagger, LazyJSONEncoder, LazyString, swag_from
    from flask_swagger_ui import get_swaggerui_blueprint
    import src.functions as functions
    import src.incoming_data_class
    import src.injection_class
    import src.sql_class as sql_class
    import src.class_file as class_file
    import json
    import jinja2
    import os
    import src.handle_weather_data
except Exception as e:
    print("importing error: ", e)

app = flask.Flask(__name__, template_folder='../templates')
# Configure root logger to log to console with DEBUG level
logging.basicConfig(level=logging.DEBUG)
# os.system('sudo /etc/init.d/mysql start')
# setup_swagger(app)

def setup_swagger(app):
    """
    Reference for yml editor - https://editor.swagger.io/
    """
    app.json_encoder = LazyJSONEncoder

    swagger_template = dict(
        info={
            'swagger': '2.0',
            'title': 'My first Swagger UI document',
            'version': '0.1',
            'description': 'This document Hello World functionality after executing GET.'
        }
    )

    # Define the route to serve Swagger UI files
    @app.route('/swagger_ui/<path:path>')
    def send_swagger_ui(path):
        return send_from_directory('swagger_ui', path)

    # Update the route to return the Swagger UI HTML
    @app.route('/swagger_ui')
    def swagger_ui():
        return render_template('index.html')

    def rule_filter():
        return True

    def model_filter():
        return True

    @app.route('/stuff')
    def get_swagger():
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

    swagger_config = get_swagger()
    #print("swagger_config:", swagger_config)
    #print("type(swagger_config):", type(swagger_config))

    return swagger_template, swagger_config




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
            handle_weather_data.refactor_incoming_json_into_weather_model(data)

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

@swag_from("swagger.json", methods=['GET'])
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

@swag_from("swagger.yaml", methods=['GET'])
@app.route("/get-all-table")
def api_get_table_names():
    """
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


# Function to get the list of endpoints
def get_endpoints():
    endpoints = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            endpoints.append(rule.endpoint)
    return endpoints


def create_app(port_numb=5000) -> None:
    try:
        app.run(debug=True, host='127.0.0.1', port=port_numb)
    except Exception as err:
        logging.error(f"Error running Flask app: {err}")
        print(f'create_app() - {err}')

def setup_app():
    try:
        c = class_file.ConfigData()
        total_path = c.get_logging_path() + c.get_log_filename()
        logging.basicConfig(filename=total_path, level=c.get_logging_level())
        logging.debug(f'main() - {c.show_all()}')

        # Before running the app, set up Swagger
        swagger_template, swagger_config = setup_swagger(app)
        swagger = Swagger(app, template=swagger_template, config=swagger_config)

        # Ensure all endpoints are printed before running the app
        logging.debug(f"List of endpoints: {get_endpoints()}")
    except Exception as e:
        logging.error(f"Error initializing app: {e}")

def run_app(port_numb=5000):
    try:
        create_app(port_numb)
    except Exception as err:
        logging.error(f"Error running Flask app: {err}")
        print(f'create_app() - {err}')

if __name__ == '__main__':
    try:
        setup_app()
        run_app(6005)
    except Exception as e:
        logging.error(f"Error initializing app: {e}")
