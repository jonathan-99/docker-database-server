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
    import handle_weather_data
except Exception as e:
    print("importing error: ", e)

app = flask.Flask(__name__, template_folder='../templates')
# os.system('sudo /etc/init.d/mysql start')
# setup_swagger(app)

def setup_swagger(app):
    app.json_encoder = LazyJSONEncoder

    swagger_template = dict(
        info={
            'title': LazyString(lambda: 'My first Swagger UI document'),
            'version': LazyString(lambda: '0.1'),
            'description': LazyString(
                lambda: 'This documements Hello World functionality after executing GET.'),
        },
        host=LazyString(lambda: request.host)
    )

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": '/apidocs',
                "route": '/stuff',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

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

@swag_from("swagger.yml", methods=['GET'])
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

@swag_from("swagger.yml", methods=['GET'])
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

# Swagger documentation route
#@app.route('/stuff')
#def get_swagger():
#    swag = Swagger(app)
#    swag['info']['version'] = "3.0.0"
#    swag['info']['title'] = "My API"
#    return jsonify(swag)


@app.route('/stuff')
def get_swagger():
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": '/apidocs',
                "route": '/stuff',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    return swagger_config

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
        s_template, s_config = setup_swagger(app)
        swagger = Swagger(app, template=s_template, config=s_config)

        # Ensure all endpoints are printed before running the app
        print("List of endpoints:", get_endpoints())
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
