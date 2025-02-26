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
    from flask import Flask, jsonify, request, render_template, send_from_directory
    from flask.json.provider import DefaultJSONProvider
    from flasgger import Swagger, LazyJSONEncoder, swag_from
    import src.functions as functions
    import src.incoming_data_class
    import src.injection_class
    import src.sql_class as sql_class
    import src.class_file as class_file
    import json
    import jinja2
    import uuid
    import handle_weather_data
    import route_details
    import src.app_routes as app_routes
except Exception as e:
    print("importing error: ", e)


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            # Handle objects that cannot be serialized by converting them to string
            return str(obj)

app = flask.Flask(__name__, template_folder='../templates')
# Set a custom JSON encoder (this adds the json_encoder attribute)
app.json_encoder = CustomJSONProvider(app)

# Configure root logger to log to console with DEBUG level
logging.basicConfig(level=logging.DEBUG)
# os.system('sudo /etc/init.d/mysql start')
# setup_swagger(app)

# Define Swagger setup function
def setup_swagger(inner_app):
    """
    Reference for yml editor - https://editor.swagger.io/
    """

    # Assign the LazyJSONEncoder via the custom provider
    app.json = CustomJSONProvider(inner_app)

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
    def route_get_column_details(table_name: str, get_column: str) -> json:
        output = app_routes.api_get_data(table_name, get_column)
        return output

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
            },
            400: {
                'description': 'Bad Request - The request could not be understood or was missing required parameters.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Bad Request'
                        },
                        'message': {
                            'type': 'string',
                            'example': 'Invalid input'
                        },
                        'status': {
                            'type': 'integer',
                            'example': 400
                        }
                    }
                }
            },
            500: {
                'description': 'Internal Server Error - Something went wrong on the server.',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Internal Server Error'
                        },
                        'message': {
                            'type': 'string',
                            'example': 'An unexpected error occurred'
                        },
                        'status': {
                            'type': 'integer',
                            'example': 500
                        }
                    }
                }
            }
        }
    })
    def route_get_table_names():
        """
        Simple api to get all data from database through functions.py
        :return:
        """
        app_routes.get_table_names()

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
    def route_index():
        """
        Default index page which will show database stats: size, last entry.
        :return:
        """
        return app_routes.index()

    @app.route('/add-weather-data', methods=['POST'])
    def route_process_json():
        traceid = str(uuid.uuid4())
        response, status_code = app_routes.process_json(traceid)  # Pass trace ID down
        response.headers['X-Trace-Id'] = traceid  # Add trace ID to response headers
        return response, status_code

    @app.route("/create-table/<string:table_name>")
    def route_create_table(table_name: str) -> json:
        """
        Simple api to get all data from database through functions.py
        :return:
        """
        return app_routes.api_create_table(table_name)

    @app.route("/add-data/<string:device_name>/<string:table_name>/<string:input_data>")
    def route_add_data(deviceid: str, table_name: str, input_data: str) -> bool:
        return app_routes.api_add_data(deviceid, table_name, input_data, request)

    @app.route("/get/column-headers-from-this/<table_name>")
    def route_get_column_headers(table_name: str) -> json:
        """
        Get column headers from a specified table.
        """
        output = app_routes.get_column_headers(table_name)
        # this might return a comma separated value that needs to be handled.
        return output
    """
    # Define the route to serve Swagger JSON
    @app.route('/swagger.json')
    def swagger_json():
        return jsonify(swagger_template)  # Assuming swagger_template is defined with the spec
    """

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
        logging.debug("List of endpoints:" + str(get_endpoints()))
    except Exception as setup_app_error:
        logging.error(f"Error initializing app: {setup_app_error}")

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
