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
    import src.functions as functions
    import src.incoming_data_class
    import src.injection_class
    import src.sql_class as sql_class
    import src.class_file as class_file
    import json
    import jinja2
    import os
    import handle_weather_data
    import route_details
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

    swagger_template = {
        'swagger': '2.0',
        'info': {
            'title': 'My Flask App API',
            'description': 'This is the API documentation for the Flask app',
            'version': '1.0.0'
        },
        'host': 'localhost:6005',
        'basePath': '/',
        'schemes': ['http'],
    }

    # Define the route to serve Swagger UI files
    @app.route('/swagger-ui/<path:path>')
    def send_swagger_ui(path):
        return send_from_directory('swagger-ui', path)

    # Update the route to return the Swagger UI HTML
    @app.route('/swagger-ui')
    def swagger_ui():
        return render_template('index.html')

    @app.route('/stuff')
    def get_swagger():
        return route_details.get_swagger_function()


    @app.route("/get/<table_name>/<string:get_column>")
    def api_get_data(table_name: str, get_column: str) -> json:
        return route_details.get_data(table_name, get_column)

    @app.route("/get-all-table")
    @swag_from({
        'responses': {
            200: {
                'description': 'Returns a list of all table names',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            }
        }
    })
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

    @app.route('/', methods=['GET', 'POST'])
    @swag_from({
        'responses': {
            200: {
                'description': 'Default index page',
                'schema': {
                    'type': 'object'
                }
            }
        }
    })
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
        return route_details.add_data(deviceid, table_name, input_data, request)

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

    swagger_config = {
        'headers': [],
        'specs': [
            {
                'endpoint': 'apispec_1',
                'route': '/swagger.json',
                'rule_filter': lambda rule: True,  # all in!
                'model_filter': lambda tag: True,  # all in!
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/apidocs/'
    }
    #print("swagger_config:", swagger_config)
    #print("type(swagger_config):", type(swagger_config))

    swagger = Swagger(app, template=swagger_template, config=swagger_config)
    return swagger_template, swagger_config


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
        logging.debug("List of endpoints:", get_endpoints())
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
